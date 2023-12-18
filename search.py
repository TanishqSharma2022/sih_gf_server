import psycopg2
import pandas as pd

def get_connection():
	try:
		return psycopg2.connect(
			database="postgres",
			user="postgres",
			password="LENMwwPkbxc4U9rD",
			host="db.mabfnfptjihwtnyenelo.supabase.co",
			port=5432,
		)
	except:
		return False
# def get_recommendations(search_words):
conn = get_connection()

if conn:
	print("Connection to the PostgreSQL established successfully.")
else:
	print("Connection to the PostgreSQL encountered and error.")
def get_recommendations(search_words):
	curr = conn.cursor()
	v=search_words
	query="select job_title,job_description,ts_rank(to_tsvector(job_title || ' ' || coalesce(job_description, '')), websearch_to_tsquery(%(v)s)) as rank from job_listings where to_tsvector(job_title || ' ' || coalesce(job_description, '')) @@ websearch_to_tsquery(%(v)s) order by rank desc;"
	df=pd.read_sql_query(query,con=conn, params={"v":v})
	# print(df)
	job_titles = df['job_title'].tolist()
	return df.to_dict(orient='records')
# search_words = 'technology'
# get_recommendations(search_words)
