import csv
import m3u8
from m3u8 import M3U8

# this could also be an absolute filename
m3u8_obj = m3u8.load('http://tvdomel.com:8880/get.php?username=XXXX&password=YYYY&type=m3u&output=ts')  
#print m3u8_obj.segments

outputTV = M3U8()
outputAll = M3U8()

orderTV = []
orderAll = []
configMap = {}
segmentMap = {}

with open('config.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        orderTV.append(row[4])
        configMap[row[4]] = row

for x in m3u8_obj.segments:
    if (".ts" in x.uri):
        if x.title not in orderTV: 
            orderTV.append(x.title)
            orderAll.append(x.title)
    else:
        orderAll.append(x.title)


for x in m3u8_obj.segments:
    idTitle = x.title 
    if idTitle in configMap:
        x.title = configMap[idTitle][0]
        x.tvgLogo = configMap[idTitle][1]
    segmentMap[idTitle] = x

tvgId = 1
for idTitle in orderTV:
    segment = segmentMap[idTitle]
    segment.tvgId = tvgId
    tvgId += 1
    outputTV.add_segment(segment)

outputTV.dump("output_tv.m3u8")

for idTitle in orderAll:
    segment = segmentMap[idTitle]
    segment.tvgId = tvgId
    tvgId += 1
    outputAll.add_segment(segment)

outputAll.dump("output_all.m3u8")