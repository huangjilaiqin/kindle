
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False

fd = open("data/data.txt", "r")

analyseMap = {}

import nltk
#nltk.download('punkt')

from nltk.tokenize import word_tokenize

data = ""
for line in fd.readlines():
    data += line 
words = word_tokenize(data)
for word in words:
    word = word.strip()
    if word=="":
        continue
    if word not in analyseMap:
        analyseMap[word]=1
        continue
    analyseMap[word]+=1

fd = open("learned.txt","r+", encoding="utf8")
learned = fd.read()

symbols = [",",".","(",")",":","'re","'s","--","$","''","``"]
sortList = sorted(analyseMap.items(), key = lambda kv:(kv[1], kv[0]))
size = len(sortList)
index = size-1
while index>=0:
    index-=1
    item = sortList[index]
    word = item[0]
    if word in symbols:
        continue
    word = word.replace(",","")
    if is_number(word):
        continue
    if learned.find(word.lower())!=-1:
        continue
    if item[1]<20:
        continue

    size = len(word)
    if size>3:
        print("{} {}".format(item[0], item[1]))
exit()

