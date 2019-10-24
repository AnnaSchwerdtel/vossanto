# -*- coding: utf-8 -*-

#
# Reads files from the NYT corpus. Supports reading from a TAR archive.
#

import sys

# remove current directory from search path to avoid org.py is loaded
# as a module
sys.path = sys.path[1:]
import re
import xml.etree.ElementTree as ET
import tarfile
import argparse
import os
import csv
import codecs
import nltk
from nltk.tokenize import sent_tokenize

version = "0.0.4"

# convert all output into a byte string to be safe when redirecting
# UTF8Writer = codecs.getwriter('utf8')
# sys.stdout = UTF8Writer(sys.stdout)

# remove line breaks and tabs from text
re_ws = re.compile("[\n\t\r]+")

# different regex pattern to choose from (can be extend easily here)
re_theof = {
    # 1: the ... of: all unicode characters and .-,'
    1: re.compile("(\\bthe\\s+([\\w.,'-]+\\s+){1,10}?of\\b)", re.UNICODE),
    # 2: the ... among: all unicode characters and .-,'
    2: re.compile("(\\bthe\\s+([\\w.,'-]+\\s+){1,10}?among\\b)", re.UNICODE),
    # 3: the ... for: all unicode characters and .-,'
    3: re.compile("(\\bthe\\s+([\\w.,'-]+\\s+){1,10}?for\\b)", re.UNICODE),
    4: re.compile("(\\ba\\s+([\\w.,'-]+\\s+){1,10}?of\\b)", re.UNICODE),
    5: re.compile("(\\ba\\s+([\\w.,'-]+\\s+){1,10}?among\\b)", re.UNICODE),
    6: re.compile("(\\ba\\s+([\\w.,'-]+\\s+){1,10}?for\\b)", re.UNICODE),
    7: re.compile("(\\ban\\s+([\\w.,'-]+\\s+){1,10}?of\\b)", re.UNICODE),
    8: re.compile("(\\ban\\s+([\\w.,'-]+\\s+){1,10}?among\\b)", re.UNICODE),
    9: re.compile("(\\ban\\s+([\\w.,'-]+\\s+){1,10}?for\\b)", re.UNICODE),
}


# generate a list of files from various input
def gen_files(path):
    if os.path.splitext(path)[1] == ".xml":
        # XML input: just one file
        yield open(path, "rt"), path
    elif os.path.isdir(path):
        # read all files in the directory
        for fname in os.listdir(path):
            fname = path + "/" + fname
            if os.path.isfile(fname):
                yield open(fname, "rt"), fname
    else:
        # read TAR file
        tar = tarfile.open(path, "r:gz")
        for tarinfo in tar:
            if tarinfo.isreg():
                yield tar.extractfile(tarinfo), tarinfo.name


# convert NYT XML to text
def xml2str(f):
    tree = ET.parse(f)
    root = tree.getroot()

    # path to the heading
    #
    # ./body/body.head/hedline vs. ./body/body.head/
    # ./body/body.head/ and ./body/body.head/hedline include only the
    # heading itself, not the first introductory sentence which we get
    # with ./body/body.head
    heading = root.findall("./body/body.head")
    head = ""
    for block in heading:
        head += ET.tostring(block, encoding="utf-8", method="text").decode("utf-8")

    # path to the main text block
    content = root.findall("./body/body.content/")
    body = ""
    for block in content:
        if block.attrib["class"] == "full_text":
            # strip XML
            body += "\n" + ET.tostring(block, encoding="utf-8", method="text").decode(
                "utf-8"
            )
    return head + "\n\n" + body


# convert a list of XML files into texts
def gen_text(files):
    for f, fname in files:
        yield fname, xml2str(f)


# remove control characters
def gen_rm_ctrl(texts):
    for cols in texts:
        # yield [re_ws.sub(' ', col) for col in cols]
        res = []
        for col in cols:
            if isinstance(col, int):
                res.append(col)
            else:
                res.append(re_ws.sub(" ", col))
        yield res


# extract sentences for texts
def gen_sentences(texts):
    for fname, text in texts:
        # split at line breaks, since the XML preserved paragraphs
        for line in text.splitlines():
            for sentence in sent_tokenize(line):
                yield fname, sentence


# apply the regex
def gen_regex(texts, regex, groupid=0):
    for fname, text in texts:
        for m in regex.finditer(text):
            # also return the start position of the matches
            yield fname, m.group(groupid), m.start(groupid), text


# limit length of text around match
def gen_limit(texts, chars=sys.maxsize):
    for fname, match, index, text in texts:
        # reduce text to chars characters before and after match
        yield fname, match, index, text[
            max(0, index - chars) : min(index + len(match) + chars, len(text))
        ]


def print_matches(matches, sep="\t"):
    for fname, match, index, text in matches:
        print(fname, match, text, sep=sep)


def write_matches(matches, file):
    with open(file, "w") as tsvfile:
        writer = csv.writer(tsvfile, delimiter="\t", quoting=csv.QUOTE_ALL)
        for fname, match, index, text in matches:
            writer.writerow([fname, match, text])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Find Vossantos in the NYT corpus.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("input", type=str, help="input TAR/XML file or directory")
    parser.add_argument(
        "-o", "--output", type=str, help="output tsv file", default=None
    )
    parser.add_argument(
        "-r", "--regex", type=int, metavar="R", help="select regex", default=1
    )
    parser.add_argument(
        "-s", "--sep", type=str, metavar="S", help="column separator", default="\t"
    )
    parser.add_argument(
        "-c",
        "--chars",
        type=int,
        metavar="C",
        default=None,
        help="disable sentence tokenisation and instead print C characters before and after a match",
    )
    parser.add_argument(
        "-v", "--version", action="version", version="%(prog)s " + version
    )

    args = parser.parse_args()

    files = gen_files(args.input)
    texts = gen_text(files)

    if args.chars is not None:
        # avoid sentence tokenisation using NLTK
        texts = gen_rm_ctrl(texts)
        match = gen_regex(texts, re_theof[args.regex])
        match = gen_limit(match, args.chars)
    else:
        sents = gen_sentences(texts)
        match = gen_regex(sents, re_theof[args.regex])
        match = gen_rm_ctrl(match)
    write_matches(match, args.output)
    print_matches(match, args.sep)
