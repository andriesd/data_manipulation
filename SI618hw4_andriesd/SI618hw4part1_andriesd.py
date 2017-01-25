import nltk, json
import codecs

stemmer = nltk.PorterStemmer()
word_sentiment = {}

file_input = codecs.open('yelp_20000reviews.json', encoding='utf-8')
sentiment_stems = codecs.open('sentiment_word_list_stemmed.json')

sentiment_dct = json.load(sentiment_stems)

lst = []
for line in file_input:
    dct = json.loads(line)
    lst.append(dct)
    
new_data = []
for data in lst:
    data_group = []
    word_sentiment = {}
    # split each review in dataset into a list
    review = data['text'].split(' ')
    business_id = data['business_id']
    stars = float(data['stars'])
    # produce version of review as list with all words stemmed 
    for word in review:
        word = word.strip()
        word = stemmer.stem(word)
        # look up each stemmed word in sentiment dictionary
        if word in sentiment_dct:
            word_sentiment[word] = sentiment_dct[word]
            word_sentiment[word] = float(word_sentiment[word])
        else:
            word_sentiment[word] = 0.0
    unique_word_count = len(word_sentiment)
    sentiment_score = sum(word_sentiment.itervalues())
    data_group.append(business_id)
    data_group.append((stars, unique_word_count, sentiment_score))
    new_data.append(data_group)

# merge lists in new_data by business_id
# method found on StackOverflow
d = {}
for k, v in new_data:
    d.setdefault(k, [k]).append(v)
b = map(list, d.values())

averages = []
for result in b:
    vals = result[1:]
    # print vals
    lst = []
    lst2 = []
    lst3 = []
    for val in vals:
        lst.append(float(val[1]))
        denom = sum(lst)
    for val in vals:
        numerator = float(val[1])
        multiplier = val[0]
        each_part_weighted = multiplier * numerator/denom
        lst2.append(each_part_weighted) 
        weighted_avg_star = sum(lst2)
        lst3.append(val[2])
        avg_sentiment_score = sum(lst3)/len(lst3)
        val_pairs = [str(weighted_avg_star), str(avg_sentiment_score)]
    averages.append(val_pairs)

print len(averages)

output = open('star_sentimentscore.txt', 'w')
for line in averages:
    line = '\t'.join(line) + '\n'
    output.write(unicode(line).encode('utf-8'))

output.close()   

        

