import base64
import zlib
import time
import csv
import json

inputfile=input('Enter Compressed File Name: ')

readFile=open(inputfile+'.txt','r').read()
readFile=readFile.encode('utf-8')
readFile=zlib.decompress(base64.b64decode(readFile))
readFile=readFile.decode('utf-8')

output=open(inputfile+'.json','a')
output.write(readFile)
output.close()

f=open(inputfile+'.json')
data=json.load(f)

f.close()

new_data = []

for i in data:
   flat = {}
   names = i.keys()
   for n in names:
      try:
         if len(i[n].keys()) > 0:
            for ii in i[n].keys():
               flat[n+"_"+ii] = i[n][ii]
      except:
         flat[n] = i[n]
   new_data.append(flat)  

f = open(inputfile+'.csv', "a")
writer = csv.DictWriter(f, new_data[0].keys(), lineterminator='\n')
writer.writeheader()
for row in new_data:
   writer.writerow(row)
f.close()


