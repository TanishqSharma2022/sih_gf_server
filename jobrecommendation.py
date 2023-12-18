import pandas as pd
import ast 
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re
import supabase
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from supabase import create_client, Client
ps=PorterStemmer()
url: str = 'https://mabfnfptjihwtnyenelo.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hYmZuZnB0amlod3RueWVuZWxvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMjYzNTU3OSwiZXhwIjoyMDE4MjExNTc5fQ.U2yzKQs4NrgRdMjc6B6TQOA33KXM_jyfaj4C8PRpD5c'
supabase: Client = create_client(url, key)

r = supabase.table('id').select("*").execute()
r=str(r)
r=r[15 :-14]
print(r)
df=pd.read_csv('user.csv')
skills=str(df.iloc[0,7])
skills=str(skills)
skills=skills[2:-2]
df1=pd.read_csv('company.csv')
def cleaning(txt):
    cleaned_txt = re.sub(r'[^a-zA-Z0-9\s]','',txt)
    tokens = nltk.word_tokenize(cleaned_txt.lower())
    stemming = [ps.stem(word) for word in tokens if word not in stopwords.words('english')]
    return stemming
skill=cleaning(skills)
new_row=pd.DataFrame({'id':[" "],'companyname':[" "],'company_description':[" "],'job_title':[" "],'job_description':[" "],'location':[" "],'new_col':skill},index=[len(df1.index)])
df1 = pd.concat([df1,new_row])
skill=str(skill)
skill=skill[1:-1]
tfif = TfidfVectorizer()
matrix = tfif.fit_transform(df1['new_col'])
similarity = cosine_similarity(matrix)
print(similarity)
def recommendation(title):
    idx=len(df1.index)-1
    print(idx)
    distances=sorted(list(enumerate(similarity[idx])),key=lambda x: x[1],reverse=True)[1:20]
    jobs=[]
    jobdes=[]
    for i in distances:
        jobs.append(df1.iloc[i[0]].job_title)
        jobdes.append(df1.iloc[i[0]].job_description)
    return jobs,jobdes

jobs,jobdes=recommendation(skill)
dp=pd.DataFrame()
dp['job_title'] = pd.Series(jobs)
dp['job_description'] = pd.Series(jobdes)
print(dp)



