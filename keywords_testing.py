import nltk

stopwords_list2 = ['a','able','about','across','after','all','almost','also','am','among',
                   'an','and','any','are','as','at','be','because','been','but','by','can',
                   'cannot','could','dear','did','do','does','done','either','else','ever','every',
                   'for','from','get','goes','got','had','has','have','he','her','hers','him','his',
                   'how','however','i','if','in','into','is','it','its','just','least','let',
                   'like','likely','may','me','might','most','must','my','neither','no','nor',
                   'not','of','off','often','on','only','or','other','our','own','rather','said',
                   'say','says','she','should','since','so','some','than','that','the','their',
                   'them','then','there','these','they','this','tis','to','too','twas','us',
                   'wants','was','we','were','what','when','where','which','while','who',
                   'whom','why','will','with','would','yes','yet','you','your']

str = ['Bill Gates goes to White House and he enters through house of gates which were white']
str2 = ['Bill Gates is a millionare. He was invited at White House by president Obama']
str_lower = [x.lower() for x in str[0].split()]
str2_lower = [x.lower() for x in str2[0].split()]

join = []

from nltk.corpus import stopwords
str_filtered = [w for w in str_lower if w not in stopwords.words('english')]
str_filtered = [w for w in  str_filtered if w not in stopwords_list2]
str2_filtered = [w for w in str2_lower if w not in stopwords.words('english')]
str2_filtered = [w for w in  str2_filtered if w not in stopwords_list2]

from nltk import bigrams
join.extend(str_filtered)
join.extend(str2_filtered)

str_bg = bigrams(join)

# counting words frequency

from collections import Counter
cnt_uni = Counter(join)
cnt_bi = Counter(str_bg)

print str
print "\n"
print str2
print "\n"
print join
print "\n"
print "******Keywords******\n"
print cnt_uni;
print "*****BiGrams******\n"
print cnt_bi;
