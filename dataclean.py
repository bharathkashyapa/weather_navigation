import csv,random
data=[]
with open('all_data.csv','rb') as csvfile:
    rows=csv.reader(csvfile)
    for i in rows:
        data.append(i[0].split('\t'))
# data contains all parameters as a list
count_of_empty_rain=0
for i in data:
    if(i[2]==''):
        count_of_empty_rain+=1
#print data[4]
print count_of_empty_rain
c=0
for i in range(1,len(data)-1):
    if (data[i]=='' and data[i-1][2]==data[i+1][2]):
        c=c+1
print c
for i in range(1,len(data)-1):
    if data[i][2]=='':
        data[i][2]=random.choice([data[i-1][2],data[i+1][2]])
raindict=dict()
#dictionary to measure type of rainfall data
for i in data:
    if i[2] not in raindict.keys():
        raindict[i[2]]=1
    else:
        raindict[i[2]]+=1
print raindict
    

