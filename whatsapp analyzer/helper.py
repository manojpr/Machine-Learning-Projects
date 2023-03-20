from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words=list(stop_words)
stop_words.extend(['ok','hmmm','yea','la','d','ah','low','okay','seri','haan','wait','send','come','like','know','what','said','sheri','enna','yeah',"cant't","i'll","call","that's","fine","even","much","want","call","said"])


def fetch_stats(selected_user,df):
    if selected_user!='All':
        df=df[df['User']==selected_user]
    
    number_of_message=df.shape[0]

    extractor=URLExtract()
    words=[]
    links=[]
    for message in df['Messages']:
        words.extend(message.split())
        links.extend(extractor.find_urls(message))
    words=len(words)
    links=len(links)
    media=df[df['Messages']=='<Media omitted>\n'].shape[0]

    return number_of_message,words,media,links

def most_busy(df):
    x=df['User'].value_counts().head()
    df=round((df['User'].value_counts()/df.shape[0])*100,2).reset_index().rename(
        columns={'index':'name','User':'percent'})
    return x,df

def most_common(df,user=None):
    words=[]
    temp=df[df['User']!='notification']
    if user:
        temp=temp[temp['User']==user]
    temp=temp[temp['Messages']!='<Media omitted>\n']
    for message in temp['Messages']:
        for word in message.lower().split():
            if word not in stop_words and len(word)>3:
                words.append(word)
    rdf=pd.DataFrame(Counter(words).most_common(20))
    rdf.columns=['words','count']
    return rdf
def emoji_func(df):
    emojis=[]
    for message in df['Messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI])
    return emoji.UNICODE_EMOJI

def frequency(df,selected_user=None):
    if selected_user:
        df=df[df['User']==selected_user]
    df['month_num']=pd.to_datetime(df['Date']).dt.month
    timeline=df.groupby(['year','month_num','month']).count()['Messages'].reset_index()
    timeline['time']=timeline['month'].astype(str)+"-"+timeline['year'].astype(str)
    return timeline

def monthly_freq(df,selected_user=None):
    if selected_user:
        df=df[df['User']==selected_user]
    timeline=df.groupby(['month']).count()['Messages'].reset_index()
    timeline=timeline.sort_values(by='Messages',ascending=False)
    return timeline
def day_freq(df,selected_user=None):
    if selected_user:
        df=df[df['User']==selected_user]
    temp=df.copy()
    temp['Day_name']=pd.to_datetime(temp['Date']).dt.day_name()
    temp=temp.groupby(['Day_name']).count()['Messages'].reset_index()
    temp=temp.sort_values(by='Messages',ascending=False)
    return temp