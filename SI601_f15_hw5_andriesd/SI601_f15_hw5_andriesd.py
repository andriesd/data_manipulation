#!/usr/bin/python
'''
spark-submit --master yarn-client --queue si601f15 --num-executors 2 --executor-memory 1g --executor-cores 2 SI601_f15_hw5_andriesd.py bigram_counts_spark_desired_output.txt si601f15hw5_output_andriesd
'''
import sys
from pyspark import SparkContext
import simplejson as json

inputdir = sys.argv[1]
outputdir = sys.argv[2]

sc = SparkContext(appName="BigramProbabilities")
input = sc.textFile(inputdir)
#input = sc.textFile("hdfs:///user/andriesd/bigram_counts_spark_desired_output.txt")
def restore_tuples(tup):
    lst = tup[1]
    words = []
    counts = []
    for word in lst[::2]:
        words.append(word)
    for count in lst[1::2]:
        count = float(count)
        counts.append(count)
    word_counts = zip(words, counts)
    return (tup[0], word_counts, sum(counts))

def tuples_to_lists(tup):
    lst = tup[1]
    new = []
    for i in lst:
        x = list(i)
        new.append(x)
    return (tup[0], new, tup[2])

def divisions(tup):
    lst = tup[1]
    for i in lst:
        i[1] = i[1]/tup[2]
    return (tup[0], lst)
    

elements = input.map(lambda count: count.replace('\t',' ').split(' ')).map(lambda x: (x[0],[x[1], x[2]])) \
                .reduceByKey(lambda a, b: a + b) \
                .map(restore_tuples).map(tuples_to_lists).map(divisions) \
                .mapValues(lambda lst: sorted(lst, key=lambda x: x[1], reverse=True)) \
                .sortBy(lambda x: x[0], ascending = True)

elements.map(lambda x : x[0] + '\t' + json.dumps(x[1])).repartition(1).saveAsTextFile(outputdir)
                
                



