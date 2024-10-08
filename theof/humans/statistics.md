Some More Statistics
====================

An "executable" version of this file is [statistics.org](statistics.org).

Temporal Distribution
---------------------

Let us check how Vossian Antonomasia (VA) is spread across the whole corpus:

``` bash
echo "year articles cand wd wd+bl found true prec"
for year in $(seq 1987 2007); do
    echo $year \
     $(grep ^$year ../articles.tsv | cut -d' ' -f2) \
     $(zcat ../theof_${year}.tsv.gz | wc -l) \
     $(cat ../theof_${year}_wd.tsv | wc -l) \
     $(cat ../theof_${year}_wda_bl.tsv | wc -l) \
     $(../org.py -y ../README.org | grep ${year} | wc -l) \
         $(../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -y -c -b ../README.org | grep ${year} | awk -F'\t' '{if ($2 == "D" || $3 == "True") print;}' | wc -l)
done
```

|  year     |  articles |  cand     |  wd    |  wd+bl |  found |  true |  prec | ppm    |
| :-------- |  -------: | --------: | -----: | -----: | -----: | ----: | ----: | -----:	|
|  1987     |  106104   |  641432   |  5236  |  131   |  129   |  95   |  73.6 |  0.90	|
|  1988     |  104541   |  637132   |  5074  |  143   |  141   |  88   |  62.4 |  0.84	|
|  1989     |  102818   |  625894   |  4922  |  151   |  148   |  104  |  70.3 |  1.01	|
|  1990     |  98812    |  614164   |  4890  |  142   |  140   |  105  |  75.0 |  1.06	|
|  1991     |  85135    |  512582   |  4189  |  154   |  154   |  103  |  66.9 |  1.21	|
|  1992     |  82685    |  493808   |  4442  |  152   |  152   |  103  |  67.8 |  1.25	|
|  1993     |  79200    |  480883   |  4338  |  167   |  167   |  121  |  72.5 |  1.53	|
|  1994     |  74925    |  464278   |  4038  |  164   |  164   |  112  |  68.3 |  1.49	|
|  1995     |  85392    |  500404   |  4636  |  162   |  162   |  124  |  76.5 |  1.45	|
|  1996     |  79077    |  497688   |  4250  |  186   |  186   |  133  |  71.5 |  1.68	|
|  1997     |  85396    |  515759   |  4561  |  173   |  173   |  134  |  77.5 |  1.57	|
|  1998     |  89163    |  571010   |  5333  |  243   |  243   |  180  |  74.1 |  2.02	|
|  1999     |  91074    |  585464   |  5375  |  189   |  189   |  136  |  72.0 |  1.49	|
|  2000     |  94258    |  602240   |  4750  |  231   |  231   |  172  |  74.5 |  1.82	|
|  2001     |  96282    |  587644   |  4512  |  210   |  209   |  163  |  78.0 |  1.69	|
|  2002     |  97258    |  597289   |  4992  |  231   |  229   |  177  |  77.3 |  1.82	|
|  2003     |  94235    |  590890   |  4749  |  219   |  216   |  165  |  76.4 |  1.75	|
|  2004     |  91362    |  571894   |  4702  |  192   |  191   |  153  |  80.1 |  1.67	|
|  2005     |  90004    |  562027   |  4680  |  208   |  207   |  162  |  78.3 |  1.80	|
|  2006     |  87052    |  561203   |  4786  |  221   |  221   |  169  |  76.5 |  1.94	|
|  2007     |  39953    |  260778   |  2276  |  101   |  101   |  76   |  75.2 |  1.90	|
|  **sum**  |  1854726  |  11474463 |  96731 |  3770  |  3753  |  2775 |  73.9 |  1.50	|
|  **mean** |  88320    |  546403   |  4606  |  180   |  179   |  132  |  73.7 |  1.49  |

The table shows the temporal distribution of the number of candidate
phrases (cand) after matching against Wikidata (wd) and a blacklist
(wd+bl), and after the manual inspection (true). 

Let us plot some of the columns:

``` gnuplot
reset
set datafile separator "\t"

set xlabel "year"
set ylabel "frequency"
set grid linetype 1 linecolor 0
set yrange [0:*]
set y2range [0:100]
set y2label 'precision'
set y2tics
set key bottom right
set style fill solid 1

set term svg enhanced size 800,600 dynamic fname "Noto Sans, Helvetica Neue, Helvetica, Arial, sans-serif" fsize 16
#set out "nyt_vossantos_over_time.svg"
plot data using 1:6 with linespoints pt 6 title 'candidates',\
     data using 1:7 with linespoints pt 7 title 'VA',\
     data using 1:8 with lines            title 'precision' axes x1y2

# for arxiv paper
set term pdf enhanced lw 2
set out "nyt_vossantos_over_time.pdf"
replot

# for DSH paper
set term png enhanced size 2835,2126 font "Arial,40" lw 4
# set term png enhanced size 800,600 font "Arial,16" lw  2
set out "nyt_vossantos_over_time.png"
plot data using 1:6 with linespoints pt 6 ps 7 lc "black" title 'candidates',\
     data using 1:7 with linespoints pt 7 ps 7 lc "black" title 'VA',\
     data using 1:8 with lines                 lc "black" title 'precision' axes x1y2


# ---- relative values

set term svg enhanced size 800,600 dynamic fname "Noto Sans, Helvetica Neue, Helvetica, Arial, sans-serif" fsize 16
set out "nyt_vossantos_over_time_rel.svg"
set ylabel "frequency (per mille)"
set format y "%2.1f"

plot data using 1:($6/$2*1000) with linespoints pt 6 title 'candidates',\
     data using 1:($7/$2*1000) with linespoints pt 7 title 'VA',\
     data using 1:8            with lines            title 'precision' axes x1y2

# for arxiv paper
set term pdf enhanced lw 2
set out "nyt_vossantos_over_time_rel.pdf"
replot

set term png enhanced size 2835,2126 font "Arial,40" lw 4
# set term png enhanced size 800,600 font "Arial,16" lw  2
set out "nyt_vossantos_over_time_rel.png"
plot data using 1:($6/$2*1000) with linespoints pt 6 ps 7 lc "black" title 'candidates',\
     data using 1:($7/$2*1000) with linespoints pt 7 ps 7 lc "black" title 'VA',\
     data using 1:8            with lines                 lc "black" title 'precision' axes x1y2
```

Absolute frequency: ![Absolute Frequency](nyt_vossantos_over_time.svg
"Absolute number of VA candidates and true VA extracted per year.  The
right vertical axis measures the resulting precision (percentage of
true VA among the candidates)")

Relative frequency: ![Relative
Frequency](nyt_vossantos_over_time_rel.svg "Relative frequency of VA
candidates and true VA extracted per year.  The right vertical axis
measures the resulting precision (percentage of true VA among the
candidates)")

Top-40 VA Sources
-----------------

Let us count the most frequent sources for Vossian Antonomasia:

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T ../README.org | sort | uniq -c | sort -nr | head -n40
```

|  count |  source                                                           |
|  ----: | :------------------------------------------------------------	 |
|  68    |  [Michael Jordan](https://www.wikidata.org/wiki/Q41421)			 |
|  58    |  [Rodney Dangerfield](https://www.wikidata.org/wiki/Q436386)		 |
|  36    |  [Babe Ruth](https://www.wikidata.org/wiki/Q213812)				 |
|  32    |  [Elvis Presley](https://www.wikidata.org/wiki/Q303)				 |
|  31    |  [Johnny Appleseed](https://www.wikidata.org/wiki/Q369675)		 |
|  23    |  [Bill Gates](https://www.wikidata.org/wiki/Q5284)				 |
|  21    |  [Pablo Picasso](https://www.wikidata.org/wiki/Q5593)			 |
|  21    |  [Michelangelo](https://www.wikidata.org/wiki/Q5592)				 |
|  21    |  [Donald Trump](https://www.wikidata.org/wiki/Q22686)			 |
|  21    |  [Jackie Robinson](https://www.wikidata.org/wiki/Q221048)		 |
|  21    |  [Madonna](https://www.wikidata.org/wiki/Q1744)					 |
|  20    |  [P. T. Barnum](https://www.wikidata.org/wiki/Q223766)			 |
|  20    |  [Tiger Woods](https://www.wikidata.org/wiki/Q10993)				 |
|  18    |  [Martha Stewart](https://www.wikidata.org/wiki/Q234606)			 |
|  16    |  [Henry Ford](https://www.wikidata.org/wiki/Q8768)				 |
|  16    |  [William Shakespeare](https://www.wikidata.org/wiki/Q692)		 |
|  16    |  [Wolfgang Amadeus Mozart](https://www.wikidata.org/wiki/Q254)	 |
|  15    |  [Adolf Hitler](https://www.wikidata.org/wiki/Q352)				 |
|  14    |  [Greta Garbo](https://www.wikidata.org/wiki/Q5443)				 |
|  14    |  [John Wayne](https://www.wikidata.org/wiki/Q40531)				 |
|  14    |  [Mother Teresa](https://www.wikidata.org/wiki/Q30547)			 |
|  13    |  [Napoleon](https://www.wikidata.org/wiki/Q517)					 |
|  13    |  [Ralph Nader](https://www.wikidata.org/wiki/Q193156)			 |
|  12    |  [Leonardo da Vinci](https://www.wikidata.org/wiki/Q762)			 |
|  12    |  [Cal Ripken](https://www.wikidata.org/wiki/Q731168)				 |
|  12    |  [Leo Tolstoy](https://www.wikidata.org/wiki/Q7243)				 |
|  12    |  [Oprah Winfrey](https://www.wikidata.org/wiki/Q55800)			 |
|  12    |  [Rosa Parks](https://www.wikidata.org/wiki/Q41921)				 |
|  12    |  [Susan Lucci](https://www.wikidata.org/wiki/Q242936)			 |
|  11    |  [Walt Disney](https://www.wikidata.org/wiki/Q8704)				 |
|  11    |  [Willie Horton](https://www.wikidata.org/wiki/Q8021572)			 |
|  11    |  [Rembrandt](https://www.wikidata.org/wiki/Q5598)				 |
|  10    |  [Albert Einstein](https://www.wikidata.org/wiki/Q937)			 |
|  10    |  [Thomas Edison](https://www.wikidata.org/wiki/Q8743)			 |
|  10    |  [Mike Tyson](https://www.wikidata.org/wiki/Q79031)				 |
|  10    |  [Julia Child](https://www.wikidata.org/wiki/Q214477)			 |
|  9     |  [Ross Perot](https://www.wikidata.org/wiki/Q313697)				 |
|  9     |  [Dennis Rodman](https://www.wikidata.org/wiki/Q201608)			 |
|  8     |  [James Dean](https://www.wikidata.org/wiki/Q83359)				 |
|  8     |  [Mikhail Gorbachev](https://www.wikidata.org/wiki/Q30487)        |

Top-40 Gallery
--------------

… pulled from Wikidata via Property:P18 (one entity has no image provided in Wikidata):

<a href="https://commons.wikimedia.org/wiki/File:Michael_Jordan.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Michael_Jordan.jpg/169px-Michael_Jordan.jpg" alt="Michael Jordan" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:RodneyDangerfield1978.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/b/bf/RodneyDangerfield1978.jpg" alt="Rodney Dangerfield" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Babe_Ruth_cropped.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/c/cb/Babe_Ruth_cropped.jpg" alt="Babe Ruth" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:PresleyPromo1954PhotoOnly.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/2/2d/PresleyPromo1954PhotoOnly.jpg" alt="Elvis Presley" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Johnny_Appleseed_1.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Johnny_Appleseed_1.jpg/146px-Johnny_Appleseed_1.jpg" alt="Johnny Appleseed" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Bill_Gates_2018.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Bill_Gates_2018.jpg/191px-Bill_Gates_2018.jpg" alt="Bill Gates" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Pablo_picasso_1_(cuadrado).jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/a/a9/Pablo_picasso_1_%28cuadrado%29.jpg" alt="Pablo Picasso" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Miguel_%C3%81ngel,_por_Daniele_da_Volterra_(detalle).jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/Miguel_%C3%81ngel%2C_por_Daniele_da_Volterra_%28detalle%29.jpg/207px-Miguel_%C3%81ngel%2C_por_Daniele_da_Volterra_%28detalle%29.jpg" alt="Michelangelo" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Donald_Trump_official_portrait_(cropped).jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Donald_Trump_official_portrait_%28cropped%29.jpg/174px-Donald_Trump_official_portrait_%28cropped%29.jpg" alt="Donald Trump" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Jrobinson.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/42/Jrobinson.jpg/303px-Jrobinson.jpg" alt="Jackie Robinson" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Madonna_Rebel_Heart_Tour_2015_-_Stockholm_(23051472299)_(cropped_2).jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Madonna_Rebel_Heart_Tour_2015_-_Stockholm_%2823051472299%29_%28cropped_2%29.jpg/191px-Madonna_Rebel_Heart_Tour_2015_-_Stockholm_%2823051472299%29_%28cropped_2%29.jpg" alt="Madonna" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Phineas_Taylor_Barnum_portrait.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/d/df/Phineas_Taylor_Barnum_portrait.jpg" alt="P. T. Barnum" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:TigerWoodsOct2011.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0b/TigerWoodsOct2011.jpg/250px-TigerWoodsOct2011.jpg" alt="Tiger Woods" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Martha_Stewart_2011_Shankbone.JPG"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/68/Martha_Stewart_2011_Shankbone.JPG/160px-Martha_Stewart_2011_Shankbone.JPG" alt="Martha Stewart" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Henry_ford_1919.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/Henry_ford_1919.jpg/188px-Henry_ford_1919.jpg" alt="Henry Ford" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Shakespeare.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Shakespeare.jpg/187px-Shakespeare.jpg" alt="William Shakespeare" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Mozart-small.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cf/Mozart-small.jpg/202px-Mozart-small.jpg" alt="Wolfgang Amadeus Mozart" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Hitler_portrait_crop.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/e/e1/Hitler_portrait_crop.jpg" alt="Adolf Hitler" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Garbo-Anna_Karenina-036.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Garbo-Anna_Karenina-036.jpg/183px-Garbo-Anna_Karenina-036.jpg" alt="Greta Garbo" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:John_Wayne_portrait.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/4/40/John_Wayne_portrait.jpg" alt="John Wayne" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:MotherTeresa_090.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/MotherTeresa_090.jpg/180px-MotherTeresa_090.jpg" alt="Mother Teresa" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project_2.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project_2.jpg/144px-Jacques-Louis_David_-_The_Emperor_Napoleon_in_His_Study_at_the_Tuileries_-_Google_Art_Project_2.jpg" alt="Napoleon" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Ralph_nader_portrait.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/8/8e/Ralph_nader_portrait.jpg" alt="Ralph Nader" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Leonardo_da_Vinci_-_presumed_self-portrait_-_WGA12798.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Leonardo_da_Vinci_-_presumed_self-portrait_-_WGA12798.jpg/154px-Leonardo_da_Vinci_-_presumed_self-portrait_-_WGA12798.jpg" alt="Leonardo da Vinci" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Cal_Ripken.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Cal_Ripken.jpg/179px-Cal_Ripken.jpg" alt="Cal Ripken" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Leo_Tolstoy,_portrait.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Leo_Tolstoy%2C_portrait.jpg/176px-Leo_Tolstoy%2C_portrait.jpg" alt="Leo Tolstoy" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Oprah_in_2014.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bf/Oprah_in_2014.jpg/181px-Oprah_in_2014.jpg" alt="Oprah Winfrey" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Rosaparks.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c4/Rosaparks.jpg/198px-Rosaparks.jpg" alt="Rosa Parks" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Susan_Lucci_Heart_Truth_2009.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/6/62/Susan_Lucci_Heart_Truth_2009.jpg/124px-Susan_Lucci_Heart_Truth_2009.jpg" alt="Susan Lucci" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Walt_Disney_1946.JPG"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/df/Walt_Disney_1946.JPG/160px-Walt_Disney_1946.JPG" alt="Walt Disney" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Rembrandt_van_Rijn_-_Self-Portrait_-_Google_Art_Project.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Rembrandt_van_Rijn_-_Self-Portrait_-_Google_Art_Project.jpg/185px-Rembrandt_van_Rijn_-_Self-Portrait_-_Google_Art_Project.jpg" alt="Rembrandt" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Albert_Einstein_Head.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Albert_Einstein_Head.jpg/180px-Albert_Einstein_Head.jpg" alt="Albert Einstein" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Thomas_Edison2-crop.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/40/Thomas_Edison2-crop.jpg/192px-Thomas_Edison2-crop.jpg" alt="Thomas Edison" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Mike_Tyson_Portrait.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f2/Mike_Tyson_Portrait.jpg/160px-Mike_Tyson_Portrait.jpg" alt="Mike Tyson" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Julia_Child_restore.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/f/fe/Julia_Child_restore.jpg" alt="Julia Child" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:RossPerotColor.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/RossPerotColor.jpg/180px-RossPerotColor.jpg" alt="Ross Perot" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:Dennis_Rodman_ToPo.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Dennis_Rodman_ToPo.jpg/159px-Dennis_Rodman_ToPo.jpg" alt="Dennis Rodman" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:James_Dean_in_East_of_Eden_trailer_2.jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/a/a4/James_Dean_in_East_of_Eden_trailer_2.jpg" alt="James Dean" height="140" /></a>
<a href="https://commons.wikimedia.org/wiki/File:RIAN_archive_850809_General_Secretary_of_the_CPSU_CC_M._Gorbachev_(crop).jpg"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/5/57/RIAN_archive_850809_General_Secretary_of_the_CPSU_CC_M._Gorbachev_%28crop%29.jpg/190px-RIAN_archive_850809_General_Secretary_of_the_CPSU_CC_M._Gorbachev_%28crop%29.jpg" alt="Mikhail Gorbachev" height="140" /></a>

Categories
----------

### online

Extract the categories of articles:

``` bash
export PYTHONIOENCODING=utf-8
for year in $(seq 1987 2007); do
    ./nyt.py --category ../nyt_corpus_${year}.tar.gz \
        | sed -e "s/^nyt_corpus_//" -e "s/\.har\//\//" -e "s/\.xml\t/\t/" \
        | sort >> nyt_categories.tsv
done
```

Compute frequency distribution over all articles:

``` bash
cut -d$'\t' -f2 nyt_categories.tsv | sort -S1G | uniq -c \
   | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
                                          > nyt_categories_distrib.tsv
```

Check the number of and the top categories:

``` bash
echo articles $(wc -l < nyt_categories.tsv)
echo categories $(wc -l < nyt_categories_distrib.tsv)
echo ""
sort -nrk2 nyt_categories_distrib.tsv | head
```

|  articles   | 1854726  |
|  categories | 1580	 |
|  :--------- | -------: |
|  Business   | 291982	 |
|  Sports     | 160888	 |
|  Opinion    | 134428	 |
|  U.S.       | 89389	 |
|  Arts       | 88460	 |
|  World      | 79786	 |
|  Style      | 65071	 |
|  Obituaries | 19430	 |
|  Magazine   | 11464	 |
|  Travel     | 10440    |

Collect the categories of the articles:

``` bash
echo "VA" $(../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T ../README.org | wc -l) articles $(wc -l < ../nyt_categories.tsv)
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T -f ../README.org | join ../nyt_categories.tsv - | sed "s/ /\t/" | awk -F'\t' '{print $2}' \
    | sort | uniq -c \
    | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
    | join -t$'\t' -o1.2,1.1,2.2 - ../nyt_categories_distrib.tsv \
    | sort -nr | head -n20
```

|  VA        |  2646   | category                | articles  | 1854726  |
|  --------: | ------: | :---------------------- | --------: | -------: |
|  336       |  12.7%  | Sports                  | 160888    | 8.7%		|
|  334       |  12.6%  | Arts                    | 88460     | 4.8%		|
|  290       |  11.0%  | New York and Region     | 221897    | 12.0%	|
|  237       |  9.0%   | Arts; Books             | 35475     | 1.9%		|
|  158       |  6.0%   | Movies; Arts            | 27759     | 1.5%		|
|  109       |  4.1%   | Business                | 291982    | 15.7%	|
|  102       |  3.9%   | Opinion                 | 134428    | 7.2%		|
|  96        |  3.6%   | U.S.                    | 89389     | 4.8%		|
|  95        |  3.6%   | Magazine                | 11464     | 0.6%		|
|  62        |  2.3%   | Style                   | 65071     | 3.5%		|
|  61        |  2.3%   | Arts; Theater           | 13283     | 0.7%		|
|  46        |  1.7%   | World                   | 79786     | 4.3%		|
|  39        |  1.5%   | Home and Garden; Style  | 13978     | 0.8%		|
|  32        |  1.2%   | Travel                  | 10440     | 0.6%		|
|  31        |  1.2%   | Technology; Business    | 23283     | 1.3%		|
|  27        |  1.0%   |                         | 42157     | 2.3%		|
|  25        |  0.9%   | Week in Review          | 17107     | 0.9%		|
|  25        |  0.9%   | Home and Garden         | 5546      | 0.3%		|
|  17        |  0.6%   | World; Washington       | 24817     | 1.3%		|
|  17        |  0.6%   | Style; Magazine         | 1519      | 0.1%     |

### desks

Extract the desks of the articles:

``` bash
export PYTHONIOENCODING=utf-8
for year in $(seq 1987 2007); do
    ./nyt.py --desk ../nyt_corpus_${year}.tar.gz \
        | sed -e "s/^nyt_corpus_//" -e "s/\.har\//\//" -e "s/\.xml\t/\t/" \
        | sort >> nyt_desks.tsv
done
```

Compute frequency distribution over all articles:

``` bash
cut -d$'\t' -f2 nyt_desks.tsv | sort -S1G | uniq -c \
   | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
                                          > nyt_desks_distrib.tsv
```

Check the number of and the top categories:

``` bash
echo articles $(wc -l < nyt_desks.tsv)
echo categories $(wc -l < nyt_desks_distrib.tsv)
echo ""
sort -t$'\t' -nrk2 nyt_desks_distrib.tsv | head
```

|  articles                |  1854727   |
|  categories              |  398		|
|  :---------------------- |  --------:	|
|  Metropolitan Desk       |  237896	|
|  Financial Desk          |  206958	|
|  Sports Desk             |  174823	|
|  National Desk           |  143489	|
|  Editorial Desk          |  131762	|
|  Foreign Desk            |  129732	|
|  Classified              |  129660	|
|  Business/Financial Desk |  112951	|
|  Society Desk            |  44032		|
|  Cultural Desk           |  40342     |

Collect the desks of the articles:

``` bash
echo "VA" $(./org.py -T README.org | wc -l) articles $(wc -l < nyt_desks.tsv)
./org.py -T -f README.org | join nyt_desks.tsv - | sed "s/ /\t/" | awk -F'\t' '{print $2}' \
    | sort | uniq -c \
    | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
    | join -t$'\t' -o1.2,1.1,2.2 - nyt_desks_distrib.tsv \
    | sort -nr | head -n20
```

|  VA        |  2764  | desk                    |  articles |  1854727 |
| ---------: |  ----: | :---------------------- |  -------: | -------: |
|  133       |  4.8%  | Sports Desk             |  174823   |  9.4%	   |
|  77        |  2.8%  | Cultural Desk           |  40342    |  2.2%	   |
|  68        |  2.5%  | Book Review Desk        |  32737    |  1.8%	   |
|  61        |  2.2%  | National Desk           |  143489   |  7.7%	   |
|  54        |  2.0%  | Financial Desk          |  206958   |  11.2%   |
|  51        |  1.8%  | Metropolitan Desk       |  237896   |  12.8%   |
|  46        |  1.7%  | Weekend Desk            |  18814    |  1.0%	   |
|  38        |  1.4%  | Arts & Leisure Desk     |  6742     |  0.4%	   |
|  35        |  1.3%  | Editorial Desk          |  131762   |  7.1%	   |
|  31        |  1.1%  | Foreign Desk            |  129732   |  7.0%	   |
|  31        |  1.1%  | Arts and Leisure Desk   |  27765    |  1.5%	   |
|  25        |  0.9%  | Magazine Desk           |  25433    |  1.4%	   |
|  25        |  0.9%  | Long Island Weekly Desk |  20453    |  1.1%	   |
|  22        |  0.8%  | Living Desk             |  6843     |  0.4%	   |
|  19        |  0.7%  | Home Desk               |  8391     |  0.5%	   |
|  15        |  0.5%  | Week in Review Desk     |  21897    |  1.2%	   |
|  14        |  0.5%  | Style Desk              |  21569    |  1.2%	   |
|  13        |  0.5%  | Styles of The Times     |  2794     |  0.2%	   |
|  12        |  0.4%  |                         |  6288     |  0.3%	   |
|  9         |  0.3%  | Travel Desk             |  23277    |  1.3%    |

Sidenote: There are many errors in the specification of desks.

Authors
-------

Extract the authors of articles:

``` bash
export PYTHONIOENCODING=utf-8
for year in $(seq 1987 2007); do
    ./nyt.py --author ../nyt_corpus_${year}.tar.gz \
        | sed -e "s/^nyt_corpus_//" -e "s/\.har\//\//" -e "s/\.xml\t/\t/" \
        | sort >> nyt_authors.tsv
done
```

Compute frequency distribution over all articles:

``` bash
cut -d$'\t' -f2 nyt_authors.tsv | sort -S1G | uniq -c \
   | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
                                          > nyt_authors_distrib.tsv
```

Check the number of and the top authors:

``` bash
echo articles $(wc -l < nyt_authors.tsv)
echo categories $(wc -l < nyt_authors_distrib.tsv)
echo ""
sort -t$'\t' -nrk2 nyt_authors_distrib.tsv | head
```

| articles            | 1854726 |
| categories          | 30691	 |
| :------------------ | ------: |
|                     | 961052  |
| Elliott, Stuart     | 6296	 |
| Holden, Stephen     | 5098	 |
| Chass, Murray       | 4544	 |
| Pareles, Jon        | 4090	 |
| Brozan, Nadine      | 3741	 |
| Fabricant, Florence | 3659	 |
| Kozinn, Allan       | 3654	 |
| Curry, Jack         | 3654	 |
| Truscott, Alan      | 3646    | 

**requires clean-up!**

Collect the authors of the articles:

``` bash
echo "VA" $(../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T ../README.org | wc -l) articles $(wc -l < ../nyt_authors.tsv)
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T -f ../README.org | join ../nyt_authors.tsv - | sed "s/ /\t/" | awk -F'\t' '{print $2}' \
    | sort | uniq -c \
    | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
    | join -t$'\t' -o1.2,1.1,2.2 - ../nyt_authors_distrib.tsv \
    | sort -nr | head -n20
```

| VA        | 2646  |  author                 | articles |  1854726   |
| --------: | ----: | :---------------------- | -------: | ---------: |
| 411       | 15.5% |                         | 961052   |  51.8%	  |
| 30        | 1.1%  |  Holden, Stephen        | 5098     |  0.3%	  |
| 29        | 1.1%  |  Maslin, Janet          | 2874     |  0.2%	  |
| 26        | 1.0%  |  Vecsey, George         | 2739     |  0.1%	  |
| 23        | 0.9%  |  Sandomir, Richard      | 3140     |  0.2%	  |
| 22        | 0.8%  |  Ketcham, Diane         | 717      |  0.0%	  |
| 20        | 0.8%  |  Kisselgoff, Anna       | 2661     |  0.1%	  |
| 19        | 0.7%  |  Dowd, Maureen          | 1647     |  0.1%	  |
| 19        | 0.7%  |  Berkow, Ira            | 1704     |  0.1%	  |
| 18        | 0.7%  |  Kimmelman, Michael     | 1515     |  0.1%	  |
| 17        | 0.6%  |  Brown, Patricia Leigh  | 568      |  0.0%	  |
| 16        | 0.6%  |  Pareles, Jon           | 4090     |  0.2%	  |
| 16        | 0.6%  |  Chass, Murray          | 4544     |  0.2%	  |
| 15        | 0.6%  |  Smith, Roberta         | 2497     |  0.1%	  |
| 15        | 0.6%  |  Lipsyte, Robert        | 817      |  0.0%	  |
| 15        | 0.6%  |  Grimes, William        | 1368     |  0.1%	  |
| 15        | 0.6%  |  Barron, James          | 2188     |  0.1%	  |
| 15        | 0.6%  |  Anderson, Dave         | 2735     |  0.1%	  |
| 14        | 0.5%  |  Stanley, Alessandra    | 1437     |  0.1%	  |
| 14        | 0.5%  |  Haberman, Clyde        |  2492    |   0.1%     |

### List of All VA Coined by the Two Top-Scoring Authors

#### [Stephen Holden](https://en.wikipedia.org/wiki/Stephen_Holden)

``` bash
# extract list of articles
for article in $(../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T -f ../README.org \
       | join ../nyt_authors.tsv - | grep "Holden, Stephen" | cut -d' ' -f1 ); do
  grep "$article" ../README.org
done
```

- [Scott Joplin](https://www.wikidata.org/wiki/Q191499)
  ([1987/01/20/0005135](http://www.nytimes.com/1987/01/20/arts/music-bolcom-and-morris.html))
  High points of the show included the obscure Cole Porter bonbons,
  ''Two Little Babes In the Wood'' and ''Nobody's Chasing Me,'' Eubie
  Blake and Noble Sissle's ''I'm Just Wild About Harry'' (performed
  both as a waltz and as a one-step to show how a simple time change
  can alter a song's character), and piano compositions by Ernesto
  Nazareth, ''**the Scott Joplin of** *Brazil*,'' that blended ragtime
  and tango.
- [Irving Berlin](https://www.wikidata.org/wiki/Q128746)
  ([1987/02/08/0011525](http://www.nytimes.com/1987/02/08/theater/me-and-my-girl-on-disk-captures-giddy-lilt-of-show.html))
  Noel Gay was not, as some have claimed, **the Irving Berlin of**
  *England*.
- [Joe DiMaggio](https://www.wikidata.org/wiki/Q297142)
  ([1987/05/16/0040728](http://www.nytimes.com/1987/05/16/theater/the-stage-in-revival-wish-you-were-here.html))
  **the Joe DiMaggio of** *love*,'' he fantasizes while flexing a
  bicep that refuses to bulge
- [George Jessel](https://www.wikidata.org/wiki/Q506146)
  ([1987/05/27/0044042](http://www.nytimes.com/1987/05/27/arts/stage-political-comedy.html))
  Compared to the younger smoothies, Mr. Altman, who called himself
  ''**the George Jessel of** *intellectuals*,'' addressed the audience
  from the standpoint of an embattled, aging hipster commenting
  amusingly on everything from the relationship between food and
  language to condom advertising.
- [Evel Knievel](https://www.wikidata.org/wiki/Q345231)
  ([1988/02/05/0116272](http://www.nytimes.com/1988/02/05/theater/avant-garde-antics-for-fearless-audiences.html))
  ''Lear,'' directed by Lee Breuer and featuring Ruth Maleczech as the
  aged king and Greg Mehrten as a drag-queen Fool, has created some
  excited word of mouth since early work-in-progress performances
  began at the George Street Playhouse in New Brunswick, N.J. Other
  high points of the marathon are likely to be Karen Finley performing
  an excerpt from her scabrously obscene monologue ''The Constant
  State of Desire,'' the Alien Comic (Tom Murrin) dressed as an
  electrified lemon tree, and an appearance by David Leslie, **the
  Evel Knievel of** *performance artists*.
- [Jimi Hendrix](https://www.wikidata.org/wiki/Q5928)
  ([1988/05/11/0144027](http://www.nytimes.com/1988/05/11/arts/the-pop-life-112088.html))
  Yomo Toro, who has been called ''**the Jimi Hendrix of** *the
  cuatro*,'' will appear at Sounds of Brazil (204 Varick Street)
  tomorrow for two shows.
- [Ed Sullivan](https://www.wikidata.org/wiki/Q83807)
  ([1988/05/12/0144329](http://www.nytimes.com/1988/05/12/arts/review-comedy-spoofing-old-time-tv.html))
  Mike, an invented character who is the comic alter ego of the
  performance artist Michael Smith, is busy becoming **the Ed Sullivan
  of** *the downtown performance world*.
- [Clint Eastwood](https://www.wikidata.org/wiki/Q43203)
  ([1989/01/16/0214485](http://www.nytimes.com/1989/01/16/theater/review-theater-macho-memories.html)) Mr.
  O'Keefe, a playwright and actor whose surreal family drama ''All
  Night Long'' was produced in 1984 in New York at Second Stage, might
  be described as **the Clint Eastwood of** *performance artists*.
- [James Dean](https://www.wikidata.org/wiki/Q83359)
  ([1989/03/17/0232294](http://www.nytimes.com/1989/03/17/movies/angry-youth-in-festival-of-new-films.html))
  ''Let's Get Lost,'' the second feature by the successful fashion
  photographer Bruce Weber, focuses on the life and times of Chet
  Baker, the jazz trumpeter and heroin addict who has been called
  **the James Dean of** *jazz*.
- [James Dean](https://www.wikidata.org/wiki/Q83359)
  ([1989/04/02/0236730](http://www.nytimes.com/1989/04/02/movies/pop-view-lost-in-the-bohemian-fog.html))
  Handsome and talented but imperiously self-destructive, the man who
  has been called ''**the James Dean of** *jazz*'' was a connoisseur
  of fast cars, women and drugs.
- [Bob Marley](https://www.wikidata.org/wiki/Q409)
  ([1989/11/22/0303163](http://www.nytimes.com/1989/11/22/arts/the-pop-life-717289.html))
  One of the anthology's strongest cuts, ''Ayiti Pa Fore'' (''Haiti Is
  Not a Forest') was recorded in 1988 and features Manno Charlemagne,
  a singer and songwriter who is regarded as **the Bob Marley of**
  *Haiti*.
- [Lenny Bruce](https://www.wikidata.org/wiki/Q460876)
  ([1989/12/13/0308717](http://www.nytimes.com/1989/12/13/arts/the-pop-life-290089.html))
  Many of his Israeli songs are collaborations with Jonathan Geffen,
  an journalist and writer whom he described ''as **the Lenny Bruce
  of** *our time there*.''
- [Spike Jones](https://www.wikidata.org/wiki/Q622636)
  ([1990/08/29/0380281](http://www.nytimes.com/1990/08/29/movies/pop-life.html))
  In ''Don Henley Must Die,'' one of the year's funniest pop songs,
  Mojo Nixon, a performer who might be described as **the Spike Jones
  of** *rock-and-roll*, demands the electric chair for the former
  Eagle as punishment for his being ''pretentious'' and ''whining like
  a wounded beagle.''
- [Nelson Riddle](https://www.wikidata.org/wiki/Q961851)
  ([1990/11/26/0404159](http://www.nytimes.com/1990/11/26/arts/review-music-harry-connick-jr-on-piano-drums-etc.html))
  "Buried in Blue," which ends the second act, is one of several
  numbers in the show in which the band is joined by strings, arranged
  and conducted by Marc Shaiman, the gifted young arranger and
  composer who is becoming **the Nelson Riddle of** *his generation*.
- [Stephen Sondheim](https://www.wikidata.org/wiki/Q153579)
  ([1991/02/06/0420740](http://www.nytimes.com/1991/02/06/arts/the-pop-life-927091.html))
  In the elegant precision and savage acuity of lyrics for songs like
  "Blizzard of Lies," "The Wheelers and the Dealers," "My Attorney
  Bernie," "Can't Take You Nowhere" and "I'm Hip," to name several of
  the roughly 100 songs he's written, Mr. Frishberg might be described
  as **the Stephen Sondheim of** *jazz songwriting*.
- [Neil Simon](https://www.wikidata.org/wiki/Q315808)
  ([1991/05/28/0448667](http://www.nytimes.com/1991/05/28/obituaries/tom-eyen-50-prolific-playwright-specializing-in-off-off-broadway.html))
  A pioneer of the Off Off Broadway experimental theater movement in
  the 1960's, Mr. Eyen was called **the Neil Simon of** *Off Off
  Broadway* at one point when he had four plays
  running simultaneously.
- [Charles Bronson](https://www.wikidata.org/wiki/Q36105)
  ([1992/02/29/0510431](http://www.nytimes.com/1992/02/29/theater/review-theater-a-loved-wife-her-illness-and-her-last-gift-a-tear.html))
  And even his wife becomes "**the Charles Bronson of** *organic
  gardening*."
- [Bob Dylan](https://www.wikidata.org/wiki/Q392)
  ([1992/09/11/0555702](http://www.nytimes.com/1992/09/11/arts/critic-s-notebook-for-adult-pop-music-a-quiet-sonic-boom.html))
  Although the 50-year-old Brazilian singer and songwriter has been
  called **the Bob Dylan of** *Brazil*, he is more than that.
- [Nelson Riddle](https://www.wikidata.org/wiki/Q961851)
  ([1992/09/11/0555702](http://www.nytimes.com/1992/09/11/arts/critic-s-notebook-for-adult-pop-music-a-quiet-sonic-boom.html))
  They have been lavishly arranged by Ray Santos, **the Nelson Riddle
  of** *Latin American pop*.
- [Elvis Presley](https://www.wikidata.org/wiki/Q303)
  ([1992/09/30/0559861](http://www.nytimes.com/1992/09/30/movies/review-film-festival-independence-in-africa-and-death-in-high-places.html))
  He is remembered as the "**the Elvis Presley of** *African
  politics*" and called a lion, a giant and a prophet.
- [Vanilla Ice](https://www.wikidata.org/wiki/Q313578)
  ([1992/12/27/0579154](http://www.nytimes.com/1992/12/27/arts/the-year-in-the-arts-pop-jazz-1992-a-lonely-couch-a-dash-of-sex-so-why-the-yawns.html))
  -- Billy Ray Cyrus could be **the Vanilla Ice of** *country*.
- [Jimi Hendrix](https://www.wikidata.org/wiki/Q5928)
  ([1993/03/26/0598111](http://www.nytimes.com/1993/03/26/arts/sounds-around-town-554993.html))
  Sugar Blue, who has been called **the Jimi Hendrix of** *the
  harmonica*, has played with everyone from Willie Dixon to the
  Rolling Stones.
- [Pete Seeger](https://www.wikidata.org/wiki/Q244441)
  ([1994/01/07/0660595](http://www.nytimes.com/1994/01/07/arts/sounds-around-town-803332.html))
  Ladino, one of the three major Jewish languages, has produced a rich
  and extensive repertory of Judeo-Spanish songs, many of which have
  been collected by Joseph Elias, who is regarded as **the Pete Seeger
  of** *Ladino music*.
- [Donald Trump](https://www.wikidata.org/wiki/Q22686)
  ([1994/03/04/0672349](http://www.nytimes.com/1994/03/04/movies/review-film-antihero-and-rich-girl-amok-on-a-freeway.html))
  Unbeknownst to Jack until it's too late, his hostage, Natalie Voss
  (Kristy Swanson), happens to be the only daughter of a
  publicity-hungry billionaire (Ray Wise) known as "**the Donald Trump
  of** *California*."
- [Pieter Brueghel the Elder](https://www.wikidata.org/wiki/Q43270)
  ([1994/09/27/0714747](https://www.nytimes.com/1994/09/27/movies/anger-and-obsession-the-life-of-robert-crumb.html))
  The art critic Robert Hughes calls Mr. Crumb "**the Bruegel of**
  *the 20th century*."
- [James Dean](https://www.wikidata.org/wiki/Q83359)
  ([1996/01/25/0825448](http://www.nytimes.com/1996/01/25/movies/on-how-to-suffer-and-the-reasons.html)) Mr.
  Cybulski's performance, full of cynical bravado, established him as
  **the James Dean of** *Poland*.
- [Jim Morrison](https://www.wikidata.org/wiki/Q44301)
  ([1996/01/31/0826617](http://www.nytimes.com/1996/01/31/movies/film-review-repression-a-painter-and-desire.html))
  But "Excess and Punishment," which opens today at the Film Forum,
  makes no attempt to lionize Schiele as **the Jim Morrison of**
  *Austrian Expressionists*.
- [Patrick Swayze](https://www.wikidata.org/wiki/Q49004)
  ([1998/05/22/1018818](http://www.nytimes.com/1998/05/22/movies/film-review-some-enchanted-evening-man-sees-true-love-across-a-crowded-nation.html))
  If Mr. Fraser continues to take such roles, he could become the 90's
  answer to **the Patrick Swayze of** ''*Dirty Dancing*.''
- [João Gilberto](https://www.wikidata.org/wiki/Q192359)
  ([2005/03/09/1655600](https://www.nytimes.com/2005/03/09/arts/music/09pass.html))
  Rosa Passos, an ardent disciple of João Gilberto, the Brazilian
  singer, guitarist and bossa nova pioneer, has been called ''**the
  João Gilberto of** *skirts*'' in her native Brazil.
- [James Stewart](https://www.wikidata.org/wiki/Q102462)
  ([2006/11/11/1803780](https://www.nytimes.com/2006/11/11/arts/music/11tayl.html))
  Thus spoke this singer-songwriter, who might be described as **the
  Jimmy Stewart of** *folk rock*, in his first Manhattan concert in
  five years.

#### [Janet Maslin](https://en.wikipedia.org/wiki/Janet_Maslin)

``` bash
# extract list of articles
for article in $(../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T -f ../README.org \
             | join ../nyt_authors.tsv - | grep "Maslin, Janet" | cut -d' ' -f1 ); do
  grep "$article" ../README.org
done
```

- [Bob Hope](https://www.wikidata.org/wiki/Q94081)
  ([1993/04/23/0604282](http://www.nytimes.com/1993/04/23/movies/review-film-dialing-911-don-t-bother.html))
  is loaded with rap-related cameos that work only if you recognize
  the players (Fab 5 Freddy, Kid Capri, Naughty by Nature and **the
  Bob Hope of** *rap cinema*, Ice-T), and have little intrinsic humor
  of their own.
- [Sandy Dennis](https://www.wikidata.org/wiki/Q239691)
  ([1993/09/03/0632371](http://www.nytimes.com/1993/09/03/movies/review-film-a-tour-of-homicidal-america.html)) (Ms.
  Lewis, who has many similar mannerisms, may be fast becoming **the
  Sandy Dennis of** *her generation*.)
- [Adolf Hitler](https://www.wikidata.org/wiki/Q352)
  ([1994/02/04/0666537](https://www.nytimes.com/1994/02/04/movies/critic-s-notebook-when-hollywood-could-be-naughty.html))
  The terrors of the code, as overseen by Joseph Breen (who was
  nicknamed "**the Hitler of** *Hollywood*" in some quarters), went
  beyond the letter of the document and brought about a more
  generalized moral purge.
- [Hulk Hogan](https://www.wikidata.org/wiki/Q44176)
  ([1994/10/25/0720551](http://www.nytimes.com/1994/10/25/books/books-of-the-times-so-libby-should-i-see-the-movie.html))
  Libby's cousin Andrew, an art director who's "so incredibly creative
  that, as my mother says, no one's holding their breath for
  grandchildren," opines that "David Mamet is **the Hulk Hogan of**
  *the American theater* and that his word processor should be tested
  for steroids."
- [Andrew Dice Clay](https://www.wikidata.org/wiki/Q504455)
  ([1995/09/22/0790066](http://www.nytimes.com/1995/09/22/movies/film-review.html)) Mr.
  Ezsterhas, **the Andrew Dice Clay of** *screenwriting*, bludgeons
  the audience with such tirelessly crude thoughts that when a group
  of chimps get loose in the showgirls' dressing room and all they do
  is defecate, the film enjoys a rare moment of good taste.
- [Thomas Jefferson](https://www.wikidata.org/wiki/Q11812)
  ([1996/01/24/0825044](http://www.nytimes.com/1996/01/24/movies/critic-s-notebook-fighting-over-the-new-talent-at-sundance.html))
  Last year's overnight sensation, Edward Burns of "The Brothers
  McMullen," came out of nowhere and now has Jennifer Aniston acting
  in his new film and Robert Redford, **the Thomas Jefferson of**
  *Sundance*, helping as a creative consultant.
- [Elliott Gould](https://www.wikidata.org/wiki/Q314805)
  ([1996/03/08/0835139](http://www.nytimes.com/1996/03/08/movies/film-review-if-they-haven-t-found-love-by-30-they-ll-jump-well-ok.html))
  All coy grins and daffy mugging, Mr. Stiller plays the role as if
  aspiring to become **the Elliott Gould of** *his generation*.
- [Charlie Parker](https://www.wikidata.org/wiki/Q103767)
  ([1996/08/09/0870295](http://www.nytimes.com/1996/08/09/movies/a-postcard-picture-of-a-graffiti-artist.html))
  But for all its admiration, ''Basquiat'' winds up no closer to that
  assessment than to the critic Robert Hughes's more jaundiced one:
  ''Far from being **the Charlie Parker of** *SoHo* (as his promoters
  claimed), he became its Jessica Savitch.''
- [Aesop](https://www.wikidata.org/wiki/Q43423)
  ([1996/08/09/0870300](http://www.nytimes.com/1996/08/09/movies/parables-that-blend-love-and-philosophy.html))
  Eric Rohmer's ''Rendezvous in Paris'' is an oasis of contemplative
  intelligence in the summer movie season, presenting three graceful
  and elegant parables with the moral agility that distinguishes Mr.
  Rohmer as **the Aesop of** *amour*.
- [Diana Vreeland](https://www.wikidata.org/wiki/Q450619)
  ([1997/06/06/0934955](http://www.nytimes.com/1997/06/06/movies/man-wanted-must-have-excellent-penmanship.html))
  The complex aural and visual style of ''The Pillow Book'' involves
  rectangular insets that flash back to Sei Shonagon (a kind of
  Windows 995) and illustrate the imperious little lists that made her
  sound like **the Diana Vreeland of** *10th-century tastes*.
- [Thomas Edison](https://www.wikidata.org/wiki/Q8743)
  ([1997/09/19/0958685](http://www.nytimes.com/1997/09/19/movies/film-review-the-dark-underbelly-of-a-sunny-town.html))
  Danny DeVito embodies this as a gleeful Sid Hudgens (a character
  whom Mr. Hanson has called ''**the Thomas Edison of** *tabloid
  journalism*''), who is the unscrupulous editor of a publication
  called Hush-Hush and winds up linked to many of the other
  characters' nastiest transgressions.
- [John Wayne](https://www.wikidata.org/wiki/Q40531)
  ([1997/09/26/0960422](http://www.nytimes.com/1997/09/26/movies/film-review-where-men-are-manly-and-so-are-bears.html)) Mr.
  Hopkins, whose creative collaboration with Bart goes back to
  ''Legends of the Fall,'' has called him ''**the John Wayne of**
  *bears*.''
- [Annie Oakley](https://www.wikidata.org/wiki/Q230935)
  ([1997/12/24/0982708](http://www.nytimes.com/1997/12/24/movies/film-review-smarter-than-she-is-hah.html))
  Running nearly as long as ''Pulp Fiction'' even though its ambitions
  are more familiar and small, ''Jackie Brown'' has the makings of
  another, chattier ''Get Shorty'' with an added homage to Pam Grier,
  **the Annie Oakley of** *1970's blaxploitation*.
- [Buster Keaton](https://www.wikidata.org/wiki/Q103949)
  ([1998/09/18/1047276](http://www.nytimes.com/1998/09/18/movies/film-review-kicks-swivels-and-wisecracks-on-hollywood-boulevard.html))
  Fortunately, being **the Buster Keaton of** *martial arts*, he makes
  a doleful expression and comedic physical grace take the place of
  small talk.
- [Michelangelo](https://www.wikidata.org/wiki/Q5592)
  ([1998/09/25/1049076](http://www.nytimes.com/1998/09/25/movies/film-festival-review-jostling-and-stumbling-toward-a-fateful-15-minutes.html))
  She goes to a plastic surgeon (Michael Lerner) who's been dubbed
  ''**the Michelangelo of** *Manhattan*'' by Newsweek.
- [Brian Wilson](https://www.wikidata.org/wiki/Q313013)
  ([1998/12/31/1073562](http://www.nytimes.com/1998/12/31/movies/critic-s-notebook-beyond-the-meteors-another-riskier-98.html))
  The enrapturing beauty and peculiar naivete of ''The Thin Red Line''
  heightened the impression of Terrence Malick as **the Brian Wilson
  of** *the film world*.
- [Dante Alighieri](https://www.wikidata.org/wiki/Q1067)
  ([1999/10/22/1147181](http://www.nytimes.com/1999/10/22/movies/film-review-a-scorsese-devil-hunt.html))
  Though his latest film explores one more urban inferno and
  colorfully reaffirms Mr. Scorsese's role as **the Dante of** *the
  Cinema*, creating its air of nocturnal torment took some doing.
- [Albert Einstein](https://www.wikidata.org/wiki/Q937)
  ([2000/12/07/1253134](https://www.nytimes.com/2000/12/07/books/books-of-the-times-tales-with-rivers-of-blood-and-freshets-of-freud.html))
  In this much coarser and more violent, action-heavy story, Mr.
  Deaver presents the villainous Dr. Aaron Matthews, whom a newspaper
  once called ''**the Einstein of** *therapists*'' in the days before
  Hannibal Lecter became his main career influence.
- [Émile Zola](https://www.wikidata.org/wiki/Q504)
  ([2001/03/09/1276449](http://www.nytimes.com/2001/03/09/books/critic-s-notebook-snuggling-up-to-good-and-evil.html))
  George P. Pelecanos arrives with the best possible recommendations
  from other crime writers (e.g., Elmore Leonard likes him), and with
  jacket copy praising him as ''**the Zola of** *Washington, D.C.*''
  But what he really displays here, in great abundance and to
  entertaining effect, is a Tarantino touch.
- [Leonard Cohen](https://www.wikidata.org/wiki/Q1276)
  ([2002/08/22/1417676](http://www.nytimes.com/2002/08/22/books/books-of-the-times-gliding-through-europe-cloaked-in-diffident-charm.html))
  The wry, sexy melancholy of his observations would be seductive
  enough in its own right -- he is **the Leonard Cohen of** *the spy
  genre* -- even without the sharp political acuity that
  accompanies it.
- [Kato Kaelin](https://www.wikidata.org/wiki/Q6377737)
  ([2003/04/07/1478881](http://www.nytimes.com/2003/04/07/books/books-of-the-times-the-real-estate-agents-who-know-all-see-all.html))
  Then he has settled in -- as ''a permanent house guest, **the Kato
  Kaelin of** *the wine country*,'' in the case of Alan Deutschman --
  and tried to figure out what it all means.
- [Hulk Hogan](https://www.wikidata.org/wiki/Q44176)
  ([2003/04/14/1480850](http://www.nytimes.com/2003/04/14/books/books-of-the-times-elegant-magazine-avalanche-of-dirt.html))
  Meanwhile, at 5 feet 10 tall and 115 pounds, Andy is **the Hulk
  Hogan of** *this food-phobic crowd*.
- [Nora Roberts](https://www.wikidata.org/wiki/Q231356)
  ([2003/04/17/1481531](http://www.nytimes.com/2003/04/17/books/critic-s-notebook-murder-they-wrote-and-wrote.html))
  For those who write like clockwork (i.e., Stuart Woods, **the Nora
  Roberts of** *mystery best-sellerdom*), a new book every few months
  is no surprise.
- [Henny Youngman](https://www.wikidata.org/wiki/Q2586583)
  ([2004/03/05/1563840](https://www.nytimes.com/2004/03/05/books/books-of-the-times-a-dizzying-ride-on-the-turntable.html))
  Together Mr. Yetnikoff and Mr. Ritz devise a kind of sitcom
  snappiness that turns Mr. Yetnikoff into **the Henny Youngman of**
  *CBS*.
- [Frank Stallone](https://www.wikidata.org/wiki/Q959153)
  ([2004/09/20/1612886](https://www.nytimes.com/2004/09/20/books/20masl.html))
  He can read the biblical story of Aaron and imagine ''**the Frank
  Stallone of** *ancient Judaism*.''
- [Marlon Brando](https://www.wikidata.org/wiki/Q34012)
  ([2005/11/08/1715899](https://www.nytimes.com/2005/11/08/books/08masl.html))
  He named his daughter Tuesday, after the actress Tuesday Weld, whom
  Sam Shepard once called ''**the Marlon Brando of** *women*.''
- [Jesse James](https://www.wikidata.org/wiki/Q213626)
  ([2005/12/09/1723424](http://www.nytimes.com/2005/12/09/books/arts/crowd-pleasers-light-reading-gone-wild.html))
  How else to explain ''Comma Sense,'' which has a blurb from Ms.
  Truss and claims that the apostrophe is **the Jesse James of**
  *punctuation marks*?
- [Elton John](https://www.wikidata.org/wiki/Q2808)
  ([2006/12/11/1811150](https://www.nytimes.com/2006/12/11/books/11masl.html))
  Though Foujita had a fashion sense that made him look like **the
  Elton John of** *Montparnasse* (he favored earrings, bangs and
  show-stopping homemade costumes), and though he is seen here hand in
  hand with a male Japanese friend during their shared tunic-wearing
  phase, he is viewed by Ms. Birnbaum strictly as a lady-killer.
- [Ernest Hemingway](https://www.wikidata.org/wiki/Q23434)
  ([2007/04/30/1844006](https://www.nytimes.com/2007/04/30/books/30masl.html)) Mr.
  Browne also points out that when he introduced Mr. Zevon to an
  audience as ''**the Ernest Hemingway of** *the twelve-string
  guitar*,'' Mr. Zevon said he was more like Charles Bronson.


### Relative Frequency

The previous table shows the most prolific authors in terms of the
*absolute* number of VA used. Naturally, authors who wrote more articles
had more chances to throw in VA expressions, so let's also compare
the *relative* number of VA used. We compute how many articles per
author we need on average to encounter one VA. The smaller this number,
the more often the author uses VA in their articles. So, '18' would
mean that on average a VA occurs in every 18th article. We will use a
threshold of at least 1000 articles to filter authors who only
occasionally wrote for the NYT.

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T -f ../README.org \
    | join ../nyt_authors.tsv - | sed "s/ /\t/" | awk -F'\t' '{print $2}' \
    | sort | uniq -c \
    | sed -e "s/^ *//" -e "s/ /\t/" | awk -F'\t' '{print $2"\t"$1}' \
    | join -t$'\t' -o1.2,2.2,1.1 - ../nyt_authors_distrib.tsv \
    | awk -F$'\t' '{if ($2 >= 1000) printf "%3.1f\t%i\t%i\t%s\n", $2/$1, $1, $2, $3}' \
    | LC_NUMERIC=en_US.UTF-8 sort -n | head -n20
```

| articles per VA | VA | articles | author              |
| --------------: | -: | -------: | :-----------------  |
|            84.2 | 18 |     1515 | Kimmelman, Michael  |
|            86.7 | 19 |     1647 | Dowd, Maureen       |
|            89.7 | 19 |     1704 | Berkow, Ira         |
|            91.2 | 15 |     1368 | Grimes, William     |
|            99.1 | 29 |     2874 | Maslin, Janet       |
|           102.6 | 14 |     1437 | Stanley, Alessandra |
|           105.3 | 26 |     2739 | Vecsey, George      |
|           111.4 | 11 |     1225 | Strauss, Neil       |
|           112.6 | 10 |     1126 | Scott, A O          |
|           112.9 | 10 |     1129 | Rich, Frank         |
|           113.0 | 12 |     1356 | Apple, R W Jr       |
|           132.5 | 12 |     1590 | Longman, Jere       |
|           133.1 | 20 |     2661 | Kisselgoff, Anna    |
|           136.5 | 23 |     3140 | Sandomir, Richard   |
|           138.6 | 14 |     1940 | Araton, Harvey      |
|           139.5 | 13 |     1814 | Martin, Douglas     |
|           139.9 | 10 |     1399 | Verhovek, Sam Howe  |
|           145.9 | 15 |     2188 | Barron, James       |
|           146.0 |  8 |     1168 | Gates, Anita        |
|           154.6 |  9 |     1391 | Collins, Glenn      |

Modifiers
---------

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -o -T ../README.org | sort | uniq -c | sort -nr | head -n30
```

| count  | modifier          |
| -----: | :---------------- |
| 55     | his day			 |
| 33     | his time			 |
| 29     | Japan			 |
| 16     | tennis			 |
| 16     | his generation	 |
| 16     | baseball			 |
| 15     | China			 |
| 13     | her time			 |
| 13     | her day			 |
| 12     | our time			 |
| 11     | the 1990's		 |
| 10     | the Zulus		 |
| 10     | the 90's			 |
| 10     | politics			 |
| 10     | hockey			 |
| 10     | Brazil			 |
| 10     | basketball		 |
| 10     | ballet			 |
| 9      | jazz				 |
| 9      | fashion			 |
| 8      | today			 |
| 8      | Israel			 |
| 8      | his era			 |
| 8      | hip-hop			 |
| 8      | golf				 |
| 8      | dance			 |


### Time

#### "Today"

Who are the sources for the modifier "… of today"?

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /today/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count  | source                                                            |
| -----: | :---------------------------------------------------------------- |
| 1      | [Shoeless Joe Jackson](https://www.wikidata.org/wiki/Q955322)	  |
| 1      | [Buck Rogers](https://www.wikidata.org/wiki/Q4982930)			  |
| 1      | [Bill McGowan](https://www.wikidata.org/wiki/Q4910116)			  |
| 1      | [William F. Buckley Jr.](https://www.wikidata.org/wiki/Q378098)	  |
| 1      | [Ralph Fiennes](https://www.wikidata.org/wiki/Q28493)			  |
| 1      | [Julie London](https://www.wikidata.org/wiki/Q231255)			  |
| 1      | [Jimmy Osmond](https://www.wikidata.org/wiki/Q1689414)			  |
| 1      | [Harry Cohn](https://www.wikidata.org/wiki/Q1586470)              |

####  "His Day" or "His Time"

Who are the sources for the modifiers "… of his day", "… of his time", and
"… of his generation"?

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /his \(day\|time\|generation\)/" | awk -F'\t' '{print $2}' | sort | uniq -c  | sort -nr  | head
```

| count  | source                                                         |
| -----: | :------------------------------------------------------------- |
| 3      | [Michael Jordan](https://www.wikidata.org/wiki/Q41421)		   |
| 2      | [Mike Tyson](https://www.wikidata.org/wiki/Q79031)			   |
| 2      | [Billy Martin](https://www.wikidata.org/wiki/Q508574)		   |
| 2      | [Dan Quayle](https://www.wikidata.org/wiki/Q49214)			   |
| 2      | [Arnold Schwarzenegger](https://www.wikidata.org/wiki/Q2685)   |
| 2      | [Martha Stewart](https://www.wikidata.org/wiki/Q234606)		   |
| 2      | [Donald Trump](https://www.wikidata.org/wiki/Q22686)		   |
| 2      | [L. Ron Hubbard](https://www.wikidata.org/wiki/Q216896)		   |
| 2      | [Tiger Woods](https://www.wikidata.org/wiki/Q10993)			   |
| 1      | [Lawrence Taylor](https://www.wikidata.org/wiki/Q963129)       |

####  "Her Day"

Who are the sources for the modifier "… of her day"?

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /her day/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count  | source                                                    |
| -----: | :-------------------------------------------------------- |
| 1      | [Hilary Swank](https://www.wikidata.org/wiki/Q93187)	  |
| 1      | [Hillary Clinton](https://www.wikidata.org/wiki/Q6294)	  |
| 1      | [Marilyn Monroe](https://www.wikidata.org/wiki/Q4616)	  |
| 1      | [Judith Krantz](https://www.wikidata.org/wiki/Q452206)	  |
| 1      | [Lucia Pamela](https://www.wikidata.org/wiki/Q3838473)	  |
| 1      | [Elizabeth Taylor](https://www.wikidata.org/wiki/Q34851)  |
| 1      | [Imelda Marcos](https://www.wikidata.org/wiki/Q285536)	  |
| 1      | [Laurie Anderson](https://www.wikidata.org/wiki/Q235066)  |
| 1      | [Nell Gwyn](https://www.wikidata.org/wiki/Q234163)		  |
| 1      | [Annie Leibovitz](https://www.wikidata.org/wiki/Q225283)  |
| 1      | [Tara Reid](https://www.wikidata.org/wiki/Q211082)		  |
| 1      | [Madonna](https://www.wikidata.org/wiki/Q1744)			  |
| 1      | [Maria Callas](https://www.wikidata.org/wiki/Q128297)     |

### Country

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -o -T ../README.org \
      | sort | uniq -c | sort -nr | grep "Japan\|China\|Brazil\|Iran\|Israel\|Mexico\|India\|South Africa\|Spain\|South Korea\|Russia\|Poland\|Pakistan" | head -n13
```

| count |  country       |
| ----: | :------------- |
| 29    |  Japan		 |
| 15    |  China		 |
| 10    |  Brazil		 |
| 8     |  Israel		 |
| 7     |  Iran			 |
| 7     |  India		 |
| 4     |  South Africa	 |
| 4     |  Mexico		 |
| 3     |  Spain		 |
| 3     |  South Korea	 |
| 3     |  Russia		 |
| 3     |  Poland		 |
| 3     |  Pakistan      |

What are the sources for the modifier ... ?

####  "Japan"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
      | grep "of\* /Japan/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count |  source                                                  |
| ----: | :------------------------------------------------------- |
| 5     |  [Walt Disney](https://www.wikidata.org/wiki/Q8704)	   |
| 4     |  [Bill Gates](https://www.wikidata.org/wiki/Q5284)	   |
| 2     |  [Nolan Ryan](https://www.wikidata.org/wiki/Q721948)	   |
| 2     |  [Frank Sinatra](https://www.wikidata.org/wiki/Q40912)   |
| 1     |  [Richard Perle](https://www.wikidata.org/wiki/Q966859)  |
| 1     |  [Thomas Edison](https://www.wikidata.org/wiki/Q8743)	   |
| 1     |  [Cal Ripken](https://www.wikidata.org/wiki/Q731168)	   |
| 1     |  [Walter Johnson](https://www.wikidata.org/wiki/Q722059) |
| 1     |  [Andy Warhol](https://www.wikidata.org/wiki/Q5603)	   |
| 1     |  [Pablo Picasso](https://www.wikidata.org/wiki/Q5593)	   |
| 1     |  [William Wyler](https://www.wikidata.org/wiki/Q51495)   |
| 1     |  [Stephen King](https://www.wikidata.org/wiki/Q39829)	   |
| 1     |  [Brad Pitt](https://www.wikidata.org/wiki/Q35332)	   |
| 1     |  [Richard Avedon](https://www.wikidata.org/wiki/Q305497) |
| 1     |  [P. D. James](https://www.wikidata.org/wiki/Q270648)	   |
| 1     |  [Rem Koolhaas](https://www.wikidata.org/wiki/Q232364)   |
| 1     |  [Steve Jobs](https://www.wikidata.org/wiki/Q19837)	   |
| 1     |  [Ralph Nader](https://www.wikidata.org/wiki/Q193156)	   |
| 1     |  [Madonna](https://www.wikidata.org/wiki/Q1744)		   |
| 1     |  [Jack Kerouac](https://www.wikidata.org/wiki/Q160534)   |

#### "China"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
     | grep "of\* /China/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count  | source                                                       |
| -----: | :----------------------------------------------------------- |
| 4      | [Barbara Walters](https://www.wikidata.org/wiki/Q231417)	 |
| 2      | [Jack Welch](https://www.wikidata.org/wiki/Q355314)			 |
| 1      | [Louis XIV of France](https://www.wikidata.org/wiki/Q7742)	 |
| 1      | [Oskar Schindler](https://www.wikidata.org/wiki/Q60029)		 |
| 1      | [Napoleon](https://www.wikidata.org/wiki/Q517)				 |
| 1      | [Keith Haring](https://www.wikidata.org/wiki/Q485635)		 |
| 1      | [Mikhail Gorbachev](https://www.wikidata.org/wiki/Q30487)	 |
| 1      | [Donald Trump](https://www.wikidata.org/wiki/Q22686)		 |
| 1      | [Larry King](https://www.wikidata.org/wiki/Q213430)			 |
| 1      | [Ted Turner](https://www.wikidata.org/wiki/Q193368)			 |
| 1      | [Madonna](https://www.wikidata.org/wiki/Q1744)               |

#### "Brazil"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
      | grep "of\* /Brazil/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count |  source                                                   |
| ----: |  :-------------------------------------------------------	|
| 1     |  [Giuseppe Verdi](https://www.wikidata.org/wiki/Q7317)	|
| 1     |  [Jil Sander](https://www.wikidata.org/wiki/Q69066)		|
| 1     |  [Walter Reed](https://www.wikidata.org/wiki/Q613136)		|
| 1     |  [Lech Wałęsa](https://www.wikidata.org/wiki/Q444)		|
| 1     |  [Jim Morrison](https://www.wikidata.org/wiki/Q44301)		|
| 1     |  [Bob Dylan](https://www.wikidata.org/wiki/Q392)			|
| 1     |  [Elvis Presley](https://www.wikidata.org/wiki/Q303)		|
| 1     |  [Scott Joplin](https://www.wikidata.org/wiki/Q191499)	|
| 1     |  [Larry Bird](https://www.wikidata.org/wiki/Q190152)		|
| 1     |  [Pablo Escobar](https://www.wikidata.org/wiki/Q187447)   |

### Sports

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -o -T ../README.org \
    | sort | uniq -c | sort -nr | grep "baseball\|basketball\|tennis\|golf\|football\|racing\|soccer\|sailing" | head -n7
```

| count |  sports      |
| ----: | ------------ |
| 16    |  tennis	   |
| 16    |  baseball	   |
| 10    |  basketball  |
| 8     |  golf		   |
| 7     |  football	   |
| 6     |  soccer	   |
| 6     |  racing      |
 
Who are the sources for the modifier ... ?

#### "Tennis"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /tennis/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

|  count  | source                                                     |
| ------: | :--------------------------------------------------------- |
|  2      | [George Foreman](https://www.wikidata.org/wiki/Q213919)	   |
|  1      | [Tim McCarver](https://www.wikidata.org/wiki/Q7803927)	   |
|  1      | [Pete Rose](https://www.wikidata.org/wiki/Q739866)		   |
|  1      | [Nolan Ryan](https://www.wikidata.org/wiki/Q721948)		   |
|  1      | [Crash Davis](https://www.wikidata.org/wiki/Q5182352)	   |
|  1      | [Spike Lee](https://www.wikidata.org/wiki/Q51566)		   |
|  1      | [John Madden](https://www.wikidata.org/wiki/Q51516)		   |
|  1      | [Michael Jordan](https://www.wikidata.org/wiki/Q41421)	   |
|  1      | [John Wayne](https://www.wikidata.org/wiki/Q40531)		   |
|  1      | [George Hamilton](https://www.wikidata.org/wiki/Q359416)   |
|  1      | [Michael Dukakis](https://www.wikidata.org/wiki/Q319099)   |
|  1      | [Jackie Robinson](https://www.wikidata.org/wiki/Q221048)   |
|  1      | [Babe Ruth](https://www.wikidata.org/wiki/Q213812)		   |
|  1      | [Dennis Rodman](https://www.wikidata.org/wiki/Q201608)	   |
|  1      | [Madonna](https://www.wikidata.org/wiki/Q1744)             |

#### "Baseball"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /baseball/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count |  source                                                       |
| ----: | :------------------------------------------------------------	|
| 2     |  [P. T. Barnum](https://www.wikidata.org/wiki/Q223766)		|
| 2     |  [Larry Bird](https://www.wikidata.org/wiki/Q190152)			|
| 1     |  [Clifford Irving](https://www.wikidata.org/wiki/Q960612)		|
| 1     |  [Mike Tyson](https://www.wikidata.org/wiki/Q79031)			|
| 1     |  [Thomas Dooley](https://www.wikidata.org/wiki/Q695751)		|
| 1     |  [Marco Polo](https://www.wikidata.org/wiki/Q6101)			|
| 1     |  [Pablo Picasso](https://www.wikidata.org/wiki/Q5593)			|
| 1     |  [Horatio Alger](https://www.wikidata.org/wiki/Q453251)		|
| 1     |  [Rodney Dangerfield](https://www.wikidata.org/wiki/Q436386)	|
| 1     |  [Michael Jordan](https://www.wikidata.org/wiki/Q41421)		|
| 1     |  [Alan Alda](https://www.wikidata.org/wiki/Q310394)			|
| 1     |  [Brandon Tartikoff](https://www.wikidata.org/wiki/Q2923786)	|
| 1     |  [Howard Hughes](https://www.wikidata.org/wiki/Q189081)		|
| 1     |  [Thomas Jefferson](https://www.wikidata.org/wiki/Q11812)     |

#### "Basketball"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /basketball/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

|  count |  source                                                           |
| -----: | :---------------------------------------------------------------- |
|  2     |  [Babe Ruth](https://www.wikidata.org/wiki/Q213812)				 |
|  1     |  [Joseph Stalin](https://www.wikidata.org/wiki/Q855)				 |
|  1     |  [Martin Luther King, Jr.](https://www.wikidata.org/wiki/Q8027)	 |
|  1     |  [Pol Pot](https://www.wikidata.org/wiki/Q39464)					 |
|  1     |  [Johnny Appleseed](https://www.wikidata.org/wiki/Q369675)		 |
|  1     |  [Adolf Hitler](https://www.wikidata.org/wiki/Q352)				 |
|  1     |  [Bugsy Siegel](https://www.wikidata.org/wiki/Q315487)			 |
|  1     |  [Elvis Presley](https://www.wikidata.org/wiki/Q303)				 |
|  1     |  [Chuck Yeager](https://www.wikidata.org/wiki/Q271939)            |

#### "Golf"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /golf/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

|  count |  source                                                    |
| -----: | :--------------------------------------------------------- |
|  2     |  [Michael Jordan](https://www.wikidata.org/wiki/Q41421)	  |
|  2     |  [Jackie Robinson](https://www.wikidata.org/wiki/Q221048)  |
|  1     |  [J. D. Salinger](https://www.wikidata.org/wiki/Q79904)	  |
|  1     |  [James Brown](https://www.wikidata.org/wiki/Q5950)		  |
|  1     |  [Marlon Brando](https://www.wikidata.org/wiki/Q34012)	  |
|  1     |  [Babe Ruth](https://www.wikidata.org/wiki/Q213812)        |

#### "Football"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /football/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count  | source                                                     |
| -----: | :--------------------------------------------------------- |
| 1      | [Ann Calvello](https://www.wikidata.org/wiki/Q4766303)	  |
| 1      | [Bobby Fischer](https://www.wikidata.org/wiki/Q41314)	  |
| 1      | [Patrick Henry](https://www.wikidata.org/wiki/Q311885)	  |
| 1      | [Susan Lucci](https://www.wikidata.org/wiki/Q242936)		  |
| 1      | [Jackie Robinson](https://www.wikidata.org/wiki/Q221048)	  |
| 1      | [Babe Ruth](https://www.wikidata.org/wiki/Q213812)		  |
| 1      | [Rich Little](https://www.wikidata.org/wiki/Q1341644)      |

#### "Soccer"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /soccer/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count  | source                                                    |
| -----: | :-------------------------------------------------------- |
| 1      | [James Brown](https://www.wikidata.org/wiki/Q5950)		 |
| 1      | [Michael Jordan](https://www.wikidata.org/wiki/Q41421)	 |
| 1      | [Larry Brown](https://www.wikidata.org/wiki/Q380013)		 |
| 1      | [Derek Jeter](https://www.wikidata.org/wiki/Q353511)		 |
| 1      | [Ernie Banks](https://www.wikidata.org/wiki/Q3051017)	 |
| 1      | [Magic Johnson](https://www.wikidata.org/wiki/Q134183)    |

#### "Racing"

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -w -T -t -c ../README.org \
    | grep "of\* /racing/" | awk -F'\t' '{print $2}' | sort | uniq -c | sort -nr
```

| count  | source                                                        |
| -----: | :------------------------------------------------------------ |
| 2      | [Rodney Dangerfield](https://www.wikidata.org/wiki/Q436386)	 |
| 1      | [John Madden](https://www.wikidata.org/wiki/Q51516)			 |
| 1      | [Bobo Holloman](https://www.wikidata.org/wiki/Q4935855)		 |
| 1      | [Lou Gehrig](https://www.wikidata.org/wiki/Q357444)			 |
| 1      | [Wayne Gretzky](https://www.wikidata.org/wiki/Q209518)        |

### Culture

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -T -o ../README.org \
    | sort | uniq -c | sort -nr | grep "dance\|hip-hop\|jazz\|fashion\|weaving\|ballet\|the art world\|wine\|salsa"   | head -n8
```

| count |  modifier       |
| :---- | :-------------- |
| 10    |  ballet		  |
| 9     |  jazz			  |
| 9     |  fashion		  |
| 8     |  hip-hop		  |
| 8     |  dance		  |
| 7     |  the art world  |
| 4     |  wine			  |
| 4     |  salsa          |

### Michael Jordan

``` bash
../org.py -T -l -o ../README.org | awk -F'\t' '{if ($1 == "Michael Jordan") print $2}' \
      | sort -u
```

the Michael Jordan of
- …
- 12th men
- actresses
- Afghanistan
- Australia
- baseball
- BMX racing
- boxing
- Brazilian basketball for the past 20 years
- college coaches
- computer games
- cricket
- cyberspace
- dance
- diving
- dressage horses
- fast food
- figure skating
- foosball
- game shows
- geopolitics
- golf
- Harlem
- her time
- his day
- his sport
- his team
- his time
- hockey
- horse racing
- hunting and fishing
- Indiana
- integrating insurance and health care
- julienne
- jumpers
- language
- Laser sailing
- late-night TV
- management in Digital
- Mexico
- motocross racing in the 1980's
- orange juice
- recording
- Sauternes
- snowboarding
- soccer
- television puppets
- tennis
- the Buffalo team
- the dirt set
- the Eagles
- the game
- the Hudson
- the National Football League
- the South Korean penal system
- the sport
- the White Sox
- this sport
- women's ball
- women's basketball

Some Favourites
---------------

- [Marquis de Sade](https://www.wikidata.org/wiki/Q123867)
  (1993/09/26/0636952) When we introduced Word in October 1983, in its
  first incarnation it was dubbed **the Marquis de Sade of** word
  processors, which was not altogether unfair.
- [Groucho Marx](https://www.wikidata.org/wiki/Q103846)
  (1987/09/27/0077726) But the tide eventually shifted, partly because
  the supreme materialist of physics, Richard Feynman of the
  California Institute of Technology, a man once described as **the
  Groucho Marx of** physics, turned the quest for nuclear substructure
  into a cause celebre.

Complete List of Successfully Extracted VA
==========================================

``` bash
../org.py --ignore-source-ids fictional_humans_in_our_data_set.tsv -g -H -T ../README.org \
      | pandoc -f org -t markdown -o vossantos.md
```

result in [vossantos.md](vossantos.md)
