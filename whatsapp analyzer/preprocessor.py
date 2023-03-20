import re
import pandas as pd
import time
def connvert(a):
    time_obj = time.strptime(a, ' %I:%M\u202f%p')
    time_24h = time.strftime('%H:%M',time_obj)
    return time_24h
def date_convert(date_str):
    date_obj = time.strptime(date_str, '%d/%m/%y')
    full_date_str = time.strftime('%Y-%m-%d',date_obj)
    return full_date_str
def preprocessing(data):
    pattern='\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}'
    message=re.split(pattern,data)
    message=message[1:]
    date=re.findall(pattern,data)
    df=pd.DataFrame({'Date':date,'Messages':message})
    df['Time range']=df['Messages'].apply(lambda x : x[:3])
    df['Messages']=df['Messages'].apply(lambda x :x[5:])
    df['Time range']=df['Time range'].apply(lambda x:str.upper(x))
    df['Datee']=df['Date'].apply(lambda x:x.split(',')[0])
    df['Time']=df['Date'].apply(lambda x:x.split(',')[1])
    df['Time']=df['Time'].astype(str)
    df['Time range']=df['Time range'].astype(str)
    df['Time']=df['Time']+df['Time range']
    df['Time range']=df['Time'].apply(lambda x:connvert(x))
    df['Datee']=df['Datee'].apply(lambda x:date_convert(x))
    df['Date']=df['Datee']+" "+df['Time range']
    df=df.drop(['Time range','Datee','Time'],axis=1)
    users=[]
    messages=[]
    for message in df['Messages']:
        entry=re.split('([\w\W]+?):\s',message)
        try:
            if entry[1]:
                users.append(entry[1])
                messages.append(entry[2])
        except :
            users.append('notification')
            messages.append(entry[0])
    df['User']=users
    df['Messages']=messages
    df['year']=pd.to_datetime(df['Date']).dt.year
    df['month']=pd.to_datetime(df['Date']).dt.month_name()
    df['day']=pd.to_datetime(df['Date']).dt.day
    df['hour']=pd.to_datetime(df['Date']).dt.hour
    df['minute']=pd.to_datetime(df['Date']).dt.minute
    return df

