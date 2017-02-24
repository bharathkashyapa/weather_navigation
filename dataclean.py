import csv,random
#['Date','Time','Condition','Temperature','Humidity','WindSpeed','WindGust','WindDirection','Visibility','Precipitation','Dew','Pressure','Fog','Rain']
def find_average(datas,which_rows,column):
    sum_average=0
    for i in which_rows:
        sum_average+=datas[i][column]
    return sum_average/len(which_rows)

data=[]
with open('alldata_before_edit.csv','rb') as csvfile:
    rows=csv.reader(csvfile)
    for i in rows:
        data.append(i)


# data contains all parameters as a list
count_of_empty_rain=0
for i in data:
    if(i[2]==''):
        count_of_empty_rain+=1
#print data[4]
#print count_of_empty_rain
c=0
for i in range(1,len(data)-1):
    if (data[i]=='' and data[i-1][2]==data[i+1][2]):
        c=c+1
#print c
for i in range(1,len(data)-1):
    if data[i][2]=='':
        data[i][2]=random.choice([data[i-1][2],data[i+1][2]])
raindict=dict()
#rainfogknown=dict()
fogdict={}
fogUnknowndict={}
#dictionary to measure type of rainfall data
for i in data:
    if i[2] not in raindict.keys():
        raindict[i[2]]=1
        if i[8]!='' and i[8]!='-9999':
            #rainfogknown[i[2]]=1
            #print i[8]
            fogdict[i[2]]=float(i[8])
        else:
            fogUnknowndict[i[2]]=1
    else:
        raindict[i[2]]+=1
        if i[8]!='' and i[8]!='-9999':
            #rainfogknown[i[2]] += 1
            if i[2] not in fogdict.keys():
                fogdict[i[2]] = float(i[8])
            else:
                fogdict[i[2]]+=float(i[8])
        else:
            if i[2] not in fogUnknowndict.keys():
                fogUnknowndict[i[2]] = 1
            else:
                fogUnknowndict[i[2]]+=1
fog_rain_known={}
for i in data:
    if i[8] != '' and i[8] != '-9999':
        if i[2] not in fog_rain_known.keys():
            fog_rain_known[i[2]]=1
        else:
            fog_rain_known[i[2]]+=1
print raindict
for i in fogdict.keys():
    fogdict[i]=fogdict[i]/float(fog_rain_known[i])
#print fogdict
#print fogUnknowndict
#print fog_rain_known

for i in data:
    if i[8]=='' or i[8]=='-9999':
        i[8]=fogdict[i[2]]
print data[50]

# TODO:
# format the fog values
# convert required strings into integers
