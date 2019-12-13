#!/usr/bin/python3
# -*- coding: utf-8 -*-

#
# Process (extract, filter, merge) Vossantos in an org mode file.
#
# Usage: Without any arguments, extracts all Vossanto canidates from
# the given org file.
#
# Author: rja
#
# Changes:
# 2019-12-13 (rja)
# - refactored iteration over parts from array to dict
# - changed handling of command line parameters for selecting columns
# - fixed source phrase and modifier extraction
# - added JSON export
# - reorganised help messages
# - added generation of unique id (useful for JSON)
# 2019-12-13 (ms)
# - moved file to parent dir
# - updated sourcephrase and modifier extraction (see extract_sourcephrase / extract_modifier) -> generalization from theof
# - stripped original line that is added to "parts"
# 2019-02-15 (rja)
# - added "-g" option to output original line and "-H" to print year headings
# - bumped version from 0.0.6 to 0.7.0 for semantic versioning
# 2018-10-24 (rja)
# - added option "--ignore-source-ids" to ignore candidates where the
#   source id is contained in the given file
# 2018-10-08 (rja)
# - added option "-c" to output classification (True/False) and renamned
#   existing "-c" to "-C"
# 2018-09-11 (rja)
# - normalising "None" to "" in output
# 2018-08-22 (rja)
# - added extraction of status that explains false positives
# 2018-08-21 (rja)
# - added extraction of source phrase as it appears in the text
# - key uses source phrase instead of source label and ignores modifier markup ('/')
# - key now uses all characters from sentence (not just the first 40)
# 2018-08-16 (rja)
# - added date extraction
# 2018-08-15 (rja)
# - improved modifier extraction
# 2018-08-09 (rja)
# - added option -o to output modifier
# 2018-03-02 (rja)
# - added option -U to include article URLs from file
# - added option -u to extract article URLs
# - annotated line regexp
# 2017-05-17 (rja)
# - simplified file parameters to support reading from STDIN
# 2017-05-14 (rja)
# - added options for selection
# 2017-05-13 (rja)
# - renamed from mergeorg.py and extended for extraction and filtering
# - migrated to Python3
# 2017-05-11 (rja)
# - initial version

import re
import argparse
import sys
import json
from collections import OrderedDict, Counter

version = "0.8.3"

# 1. [[https://www.wikidata.org/wiki/Q83484][Anthony Quinn]] (1987/01/02/0000232) ''I sometimes feel like *the Anthony Quinn of* my set.''
line_re_str = """
^                     # beginning of string
(?P<newmark>> )?      # new candidates are marked with "> "line
(?P<id>[0-9]+)\.      # all candidates are numbered
[ !]+                 # space and/or !
\+?                   # modifier for false positive
\[\[.+/               # start of Wikidata URL
(?P<wdid>[^/]+)       # Wikidata id
\]\[                  # separators
(?P<wdlabel>.+)       # Wikidata label
\]\]                  # end of Wikidata URL
\                     # space
\(                    # beginning of file id
(?P<article>          # beginning of full article part
(\[\[)?               # opening markup for article URL
(?P<aurl>http.+?)?    # article URL
(\]\[)?               # separators for article URL
(?P<fid>              # full file id
(?P<year>\\d{4})      # year
/                     # separator
(?P<month>\\d{2})     # month
/                     # separator
(?P<day>\\d{2})       # day
/                     # separator
(?P<aid>\\d+)         # article id
)                     # end of full file id
(\]\])?               # closing markup for article URL
)                     # end of full article part
\)                    # end of file id
\                     # space
(?P<sentence>.+?[^+]) # sentence
(?P<truefalse>\+)?    # false positive indicator
(\ \(                 # beginning of status token explaining false positives
(?P<status>[WD]+)     # a combination of characters
\))?                  # end of (optional) token
$                     # end of string
"""
re_line = re.compile(line_re_str, re.VERBOSE)

# to extract the modifier (enclosed in /.../) from the sentence
re_modifier = re.compile("\\* ['\"]*/(.+?)/([^0-9A-Za-z]|$)")

# to extract the exact source phrase (enclosed in * ... *) from the sentence
re_sourcephrase = re.compile("\\*\w+ (.+?) \w+\\*")

# to remove markup from the sentences
re_clean = re.compile(r"[*/.\s]")

# remove line breaks and tabs from text
re_ws = re.compile('[\n\t\r]+')


# reads the file into which the other file shall be merged
# all non-vossanto lines are returned in lines,
# all following (vossanto) lines are indexed in index using
# a key generated by match_line
def read_file(flines):
    lines = []
    index = None
    for line in flines:
        # different handling for lines before and after the heading
        if line.startswith("* results"):
            index = dict()
            lines.append(line)
        else:
            if index is not None:
                # index lines after heading "* results"
                parts = match_line(line)
                if parts:
                    year, key = get_key(parts)
                    if year not in index:
                        index[year] = dict()
                    index[year][key] = line
            else:
                # store lines before heading "* results"
                lines.append(line)
    return lines, index

# Read a TSV file with two columns into a dict.
# The first column is used as key and the second column as value.
# Lines starting with # are ignored.
def read_dict(flines, sep='\t', comment='#'):
    d = dict()
    for line in flines:
        if not line.startswith(comment):
            key, val = line.strip().split(sep)
            d[key] = val
    return d

def gen_truefalse(candidates, true_positive, false_positive):
    for cand in candidates:
        if true_positive == false_positive or true_positive == cand["classification"] or false_positive != cand["classification"]:
            yield cand


# Skip all candidates whose source's id is contained in sourcefile.
# Sourcefile must contain one Wikidata id per line, followed by their name.
# Lines starting with # are ignored.
def gen_filter_sources(candidates, sourcefile):
    if sourcefile:
        sources = read_dict(sourcefile)
        for cand in candidates:
            if cand["sourceId"] not in sources:
                yield cand
    else:
        for cand in candidates:
            yield cand

def gen_candidates(lines):
    for line in lines:
        parts = match_line(line)
        if parts:
            yield parts

# remove control characters
def gen_rm_ctrl(parts):
    for part in parts:
        yield [re_ws.sub(' ', part[p]).strip() for p in part]

# generates a key for a Vossanto
def get_key(parts):
    return parts["year"], "|".join([parts["year"], parts["aId"], parts["sourcePhrase"], re_clean.sub('', parts["sentence"])])

def select_parts(parts, fields):
    if len(fields) > 0 and not "ALL" in fields:
        ids = Counter()
        for part in parts:
            result = OrderedDict()

            for key in fields:
                if key in part:
                    result[key] = part[key]
                elif key == "id":
                    # generate (hopefully unique) id
                    result["id"] = part["aId"] + "_" + str(ids[part["aId"]])
                    ids[part["aId"]] += 1
            yield result
    else:
        # when nothing has been selected, return everything
        for part in parts:
            yield part

# checks if the line is a Vossanto line
def match_line(line):
    # detect the Vossanto lines
    match = re_line.match(line.strip())
    if match:
        d = match.groupdict()

        # prepare some values
        trueVoss = d["truefalse"] != "+"
        sourcePhrase = extract_sourcephrase(d["sentence"], trueVoss)
        modifier = extract_modifier(d["sentence"], trueVoss)

        return {
            "year"           : d["year"],
            "date"           : d["year"] + "-" + d["month"] + "-" + d["day"],
            "aId"            : d["aid"],
            "fId"            : d["fid"],
            "sourceId"       : d["wdid"],
            "sourceLabel"    : d["wdlabel"],
            "sourcePhrase"   : sourcePhrase,
            "modifier"       : modifier,
            "text"           : d["sentence"],
            "wikidata"       : "[[https://www.wikidata.org/wiki/" + d["wdid"] + "][" + d["wdlabel"] + "]]",
            "aUrl"           : d["aurl"],
            "classification" : trueVoss,
            "line"           : line.strip(),
            "newVoss"        : d["newmark"], # FIXME: where is this used?
            "status"         : d["status"] # FIXME: where is this used?
        }

    return None

# extract the modifier (enclosed in /.../) from the sentence
def extract_modifier(sentence, trueVoss):
    # ignore non-Vossantos
    if trueVoss:
        match = re_modifier.search(sentence)
        if match:
            return match.group(1)
    return ""

# extract the source phrase (enclosed in *the ... of*) from the sentence
def extract_sourcephrase(sentence, trueVoss):
    if trueVoss:
        match = re_sourcephrase.search(sentence)
        if match:
            return match.group(1)
    return ""


# given a line, either adds the URL for the article or (if already existent), changes it
def set_article_url(line, urls):
    # detect Vossanto line
    match = re_line.match(line.strip())
    if match:
        d = match.groupdict()
        fid = d["fid"]
        if fid not in urls:
            print("WARN: URL for", fid, "not found", file=sys.stderr)
        else:
            url = urls[fid]
            # implement
            article = d["article"]
            return line.replace(article, "[[" + url + "][" + fid + "]]")
    else:
        print("WARN: line did not match", line[:50], file=sys.stderr)

# inserts a vossanto line into the index
def insert(index, line, string_new = '> '):
    # extract key for this line
    parts = match_line(line)
    if not parts:
        # print warning only if not a year heading
        if not re.match("^\*{2,3} [0-9]{4}$", line.strip()):
            print("WARN: line did not match", line[:50], file=sys.stderr)
        return
    # add new Vossanto
    year, key = get_key(parts)
    if key not in index[year]:
        index[year][key] = string_new + line

# convert value to string, taking care of None
def part_to_string(p):
    if p is None:
        return ""
    return str(p)

# print CSV/TSV lines
def print_csv(parts, sep):
    for part in parts:
        print(sep.join([part_to_string(part[p]) for p in part]))

# print JSON lines
def print_json(parts):
    print("[")
    first = True
    for part in parts:
        if first:
            first = False
        else:
            print(",", end='')
        print(json.dumps(part))
    print("]")

# prints heading for each year
# must be called before select_parts, such that year information is available
# works by interleaving printing with the iteration through yield
def print_heading(parts):
    # to detect changing years (to print a heading)
    prev_year = None
    for part in parts:
        year = part["year"]
        if year != prev_year:
            print("\n**", year)
        prev_year = year
        # this enables us print the heading between the final print statements
        yield part

def parse_fields(s):
    return s.split(",")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manipulate Vossantos in org files.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('file', type=argparse.FileType('r', encoding='utf-8'), nargs='?', default=sys.stdin, help='org mode file to process')

    # filtering options
    filtering = parser.add_argument_group('filter arguments')
    filtering.add_argument('-T', '--true', action="store_true", help="output only true Vossantos")
    filtering.add_argument('-F', '--false', action="store_true", help="output only false positives")
    filtering.add_argument('--ignore-source-ids', type=argparse.FileType('r', encoding='utf-8'), metavar="FILE", help='ignore candidates with a source id contained in FILE')

    # output format options
    output = parser.add_argument_group('output arguments')
    output.add_argument('-f', '--fields', type=parse_fields, metavar="FDS", default="ALL",
                        help="fields to be included (supported values: ALL, aUrl, aId, classification, date, fId, id, line, modifier, newVoss, sourceId, sourceLabel, sourcePhrase, status, text, wikidata, year)")
    output.add_argument('-o', '--output', type=str, metavar="FMT", help="output format", default="csv", choices=["csv", "json"])
    output.add_argument('-s', '--sep', type=str, metavar="SEP", help="output separator for csv", default='\t')
    output.add_argument('-n', '--new', type=str, metavar="S", help="string to mark new entries", default='> ')
    output.add_argument('-c', '--clean', action="store_true", help="clean whitespace")
    output.add_argument('-H', '--heading', action="store_true", help="print year heading (only csv)")

    # special options
    special = parser.add_argument_group('special arguments')
    special.add_argument('-m', '--merge', type=argparse.FileType('r', encoding='utf-8'), metavar="FILE", help='file to merge')
    special.add_argument('-u', '--urls', type=argparse.FileType('r', encoding='utf-8'), metavar="FILE", help='file with article URLs')
    special.add_argument('-v', '--version', action="version", version="%(prog)s " + version)

    args = parser.parse_args()

    if args.merge:
        # read file into which the other file shall be merged
        lines, index = read_file(args.file)

        # read new file and insert Vossantos
        for line in args.merge:
            insert(index, line, args.new)
        # print first (unchanged) part of original file
        for line in lines:
            print(line, end='')

        # print Vossanto lines
        for year in sorted(index):
            print()
            print("**", year)
            for line in sorted(index[year]):
                print(index[year][line], end='')
    elif args.urls:
        # read URL file
        urls = read_dict(args.include_urls)
        # read file
        lines, index = read_file(args.file)
        # print first (unchanged) part of original file
        for line in lines:
            print(line, end='')
        # print Vossanto lines
        for year in sorted(index):
            print()
            print("**", year)
            for line in sorted(index[year]):
                # add URL to line
                print(set_article_url(index[year][line], urls), end='')
    else:
        # default: extract Vossantos
        parts = gen_candidates(args.file)
        parts = gen_truefalse(parts, args.true, args.false)
        parts = gen_filter_sources(parts, args.ignore_source_ids)
        if args.heading:
            # interleaving the headings works by yielding the parts in a loop
            parts = print_heading(parts)
        parts = select_parts(parts, args.fields)
        if args.clean:
            parts = gen_rm_ctrl(parts)
        if args.output == "json":
            print_json(parts)
        else:
            print_csv(parts, args.separator)
