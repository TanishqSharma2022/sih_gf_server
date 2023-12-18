import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re
import supabase
import ast
import numpy as np
import pandas as pd
from supabase import create_client, Client
url: str = 'https://mabfnfptjihwtnyenelo.supabase.co'
key: str = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im1hYmZuZnB0amlod3RueWVuZWxvIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcwMjYzNTU3OSwiZXhwIjoyMDE4MjExNTc5fQ.U2yzKQs4NrgRdMjc6B6TQOA33KXM_jyfaj4C8PRpD5c'
supabase: Client = create_client(url, key)

r = supabase.table('job_listings').select("*").execute()
r=str(r)
r=r[6:-12]
dict = ast.literal_eval(r)
r=pd.DataFrame(dict)
def cleaning(txt):
    cleaned_txt = re.sub(r'[^a-zA-Z0-9\s]','',txt)
    tokens = nltk.word_tokenize(cleaned_txt.lower())
    stemming = [ps.stem(word) for word in tokens if word not in stopwords.words('english')]
    return " ".join(stemming)
ps=PorterStemmer()
r['new_col'] = r['job_title']+" " +r['job_description']
r['new_col'] = r['new_col'].astype(str).apply(lambda x:cleaning(x))
with open('company.csv', 'w') as f:
    f.truncate(0)
r.to_csv('company.csv', index=False)
df2 = pd.read_csv('company.csv')
print(df2)
u=supabase.table('sih').select("*").execute()
u=str(u)
u=u[6:-12]
d = ast.literal_eval(u)
u=pd.DataFrame.from_dict(d,orient='index')
u=u.transpose()
with open('user.csv', 'w') as f:
    f.truncate(0)
u.to_csv('user.csv', index=False)
df= pd.read_csv('user.csv')
print(df)