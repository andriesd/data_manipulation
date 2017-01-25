# -*- coding: utf-8 -*-
import csv
import urllib2
from bs4 import BeautifulSoup
import re

# Population data from Eurostat
euro_stats = []
populations = []
header = ['Country']
with open('eurostat_table_populations.csv', 'rU') as csvfile:
    input = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in input:
        line = ' '.join(row).split(',')
        if line[-2] == '':
            continue
        elif line[0] == 'geo\\time':
            for year in line:
                if len(year) == 4:
                    header.append(str(year))
        else:
            euro_stats.append(line)

del header[-2:] # drop years 2014, 2015, only interested in 2004-2013
# scrub count data (drop footnotes)
for row in euro_stats:
    population = []
    for value in row:
        if value == '':
            continue
        elif value == '(b)':
            continue
        elif value == '(p)':
            continue
        elif value == '(e)':
            continue
        elif value == '(bp)':
            continue
        elif value == '(ep)':
            continue
        elif value == '(bep)':
            continue
        else:
            population.append(value)
    populations.append(population)

# Immigration data by year from OECD.Stat database
# response = urllib2.urlopen('http://stats.oecd.org/viewhtml.aspx?datasetcode=MIG&lang=en')
# html = response.read()
# soup = BeautifulSoup(html, 'lxml')

# webpage = open('oecd_inflow_data.html', 'w')
# webpage.write(soup.encode('utf8'))
# webpage.close()

# function from StackOverflow
def group(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

migration_inflows = []
html = open('oecd_inflow_data.html', 'r').read()
soup = BeautifulSoup(html, 'lxml')
str = soup.find_all('td')
for part in str:
    data = part.text
    data = data.encode('utf-8')
    # print data
    # print type(data)
    discard = re.match(r'^[(e)]+', data)
    if discard:
        continue
    else:
        migration_inflows.append(data)
# for row in migration_inflows[::16]:
    # print row

immigration_raw = []
for data in group(migration_inflows, 16):
    if data[0] != 'Estimated value':
        immigration_raw.append(data)

immigration_data = []
for row in immigration_raw:
    lst = [row[0]]
    del row[1:6] # delete blank column and values for years 2000-2003
    for i in row[1:]:
        if i != '..':
            i = i.replace('\xc2\xa0','')
            numbers = float(i)
            lst.append(numbers)
    immigration_data.append(lst) # recreate list for formatting purposes (no more code points, no more placeholders)

transfer = []   # separate country name from inflow values in each list to prepare for merging datasets
for i in immigration_data:
    i = (i[0], (i[1:]))
    transfer.append(i)

euro_populations = [] # separate country name from population values in each list for building dictionary
for i in populations:
    i = (i[0], (i[1:]))
    euro_populations.append(i)
   
euro_populations_numbers = []
for i in euro_populations:
    if len(i[1]) > 12:
        continue
    else:
        adjust_for_years = i[1]
        del adjust_for_years[-2:] # drop population counts for 2014, 2015
    num_lst = []
    for num in i[1]:
        if num != ':':
            num = float(int(num))
            num_lst.append(num)
    euro_populations_numbers.append((i[0], num_lst))


europe_dct = dict(euro_populations_numbers)

dct = {}    # combine datasets into new dictionary
for country in transfer:
    if country[0] in europe_dct and len(country[1]) == 10 :
        val = zip(country[1], europe_dct[country[0]])
        dct[country[0]] = val

# calculate immigration rates by year for each country
immigration_rates =[]
for key in dct:
    rates_by_country = []
    rates_by_country.append(key)
    # print len(dct[key]), key, dct[key]
    for tup in dct[key]:
        rate = tup[0]/tup[1] * 1000
        rates_by_country.append(rate)
    immigration_rates.append(rates_by_country)
immigration_rates.sort(key=lambda x:x[1])

output = open('euro_immigration_rates_2004-2013_andriesd.csv', 'w')
csvwriter = csv.writer(output)
csvwriter.writerow(header)
for row in immigration_rates:
    csvwriter.writerow(row)

output.close()

# get average immigration rates for each country for whole ten year period
average_rates = []
for row in immigration_rates:
    country = [row[0]]
    average = sum(row[1:])/len(row[1:])
    country.append(average)
    average_rates.append(country)

output_avgs = open('avg_rate_by_country_andriesd.csv', 'w')
csvwriter = csv.writer(output_avgs)
csvwriter.writerow(['Country', 'Average Annual Immigration Rate from 2004-2013'])
for row in average_rates:
    csvwriter.writerow(row)

output_avgs.close()