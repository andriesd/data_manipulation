#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import json
import codecs


file_input = codecs.open('yelp_academic_dataset.json', encoding='utf-8')

header = ['name', 'city', 'state', 'stars', 'review_count','main_category']
data = []

for line in file_input:
    dct = json.loads(line)
    business_record = []
    if dct['type'] == 'business':
        business_record.append(dct['name'])
        business_record.append(dct['city'])
        business_record.append(dct['state'])
        business_record.append(str(dct['stars']))
        business_record.append(str(dct['review_count']))
        if dct['categories'] == []:
            business_record.append('NA')
        else:
            business_record.append(dct['categories'][0])
    else:
        continue
    data.append(business_record)

output = open('businessdata_andriesd.tsv', 'w')
output.write(unicode('\t'.join(header) + '\n'))
for line in data:
    line = '\t'.join(line) + '\n'
    output.write(unicode(line).encode('utf-8'))

output.close()


