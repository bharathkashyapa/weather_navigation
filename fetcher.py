#http://api.wunderground.com/api/31b154971c978858/history_20130101/q/AU/Sydney.json
import csv
import pickle
import json
import requests,time
from datetime import date, timedelta as td
d1 = date(2010, 1, 1)
d2 = date(2010, 12, 31)
main_list=[]
'''
with open('data.csv', 'rb') as csvfile:
    mwriter = csv.reader(csvfile)
    for row in mwriter:
        main_list.append(row)
#main_list=main_list.reverse()
#print main_list'''
delta = d2 - d1
date_dict=dict()
for i in range(delta.days + 1):
    date_dict[i+1]=((d1 + td(days=i)).strftime('%Y%m%d'))
with open('data_status.pickle', 'rb') as handle:
    data_status = pickle.load(handle)
#print data_status
#['Date','Time','Condition','Temperature','Humidity','Wind Speed','Wind Gust','Wind Direction','Visibility','Precipitation','Dew','Pressure','Fog','Rain']

no_of_days=len(date_dict)
key_list=['31b154971c978858','c019d5235a00421f','f0220f1bc59dc68c','9676b3b01bf95412','d8811401133ab074']

def request_build(key,date):
    return "http://api.wunderground.com/api/"+key+"/history_"+date+"/q/AU/Sydney.json"
def fetch_data(request_string):
    content=requests.get(request_string)
    return content.json(),content.status_code
def set_done_status(day_of_year):
    data_status[day_of_year]=1
def write_into_list(data):
    date=data["history"]["date"]["mon"].encode('ascii')+'/'+data["history"]["date"]["mday"].encode('ascii')+'/'+data["history"]["date"]["year"].encode('ascii') # mm-dd-yyyy format
    for i in range(len(data["history"]["observations"])):
        time=data["history"]["observations"][i]["date"]["hour"]+":"+data["history"]["observations"][i]["date"]["min"].encode('ascii') #time in hh:mm military format
        condition=data["history"]["observations"][i]["conds"].encode('ascii') #Weather condition as a string
        temperature=data["history"]["observations"][i]["tempm"].encode('ascii') # temperature in C
        humidity=data["history"]["observations"][i]["hum"].encode('ascii') # humidity (%)
        wind_speed=data["history"]["observations"][i]["wspdm"].encode('ascii') # windspeed in kph
        wind_gust=data["history"]["observations"][i]["wgustm"].encode('ascii') # wind gust in kph
        wind_direction=data["history"]["observations"][i]["wdird"].encode('ascii') # wind direction degrees
        visibility=data["history"]["observations"][i]["vism"].encode('ascii') # visibility in km
        precipitation=data["history"]["observations"][i]["precipm"].encode('ascii') # precipitation in mm
        dew=data["history"]["observations"][i]["dewptm"].encode('ascii') #dew in C
        pressure=data["history"]["observations"][i]["pressurem"].encode('ascii') #pressure in bar
        fog=data["history"]["observations"][i]["fog"].encode('ascii')   #in binary
        rain=data["history"]["observations"][i]["rain"].encode('ascii')    # in binary
        ll=[date,time,condition,temperature,humidity,wind_speed,wind_gust,wind_direction,visibility,precipitation,dew,pressure,fog,rain]
        main_list.append(ll)
def fetch(n,x):
    if n<=x:
        print "done"
        exit
    else:    
            key=key_list[n%5]
            date=date_dict[n]
            request_string=request_build(key,date)
            content,status=fetch_data(request_string)
            #print content["history"]["observations"][0]["date"]["pretty"]
            if status==200 and (content["history"]["date"]["year"]+content["history"]["date"]["mon"]+content["history"]["date"]["mday"])==date:
                write_into_list(content)
                set_done_status(n)
                print date+'done'
            time.sleep(2.5)
            n=n-1
            fetch(n,x)

        
fetch(365,0)
with open('data_2010.csv', 'wb') as csvfile:
    mwriter = csv.writer(csvfile)
    for i in range(0,len(main_list)):
        mwriter.writerow(main_list[len(main_list)-i-1])
csvfile.close()

with open('data_status.pickle', 'ab+') as handle:
    pickle.dump(data_status, handle)
