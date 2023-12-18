import pandas as pd
from sqlalchemy import create_engine

def get_connection():
    try:
        return create_engine(
            "postgresql://postgres:LENMwwPkbxc4U9rD@db.mabfnfptjihwtnyenelo.supabase.co:5432/postgres"
        )
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_recommendations(search_words):
    engine = get_connection()

    if engine:
        print("Connection to the PostgreSQL established successfully.")
        try:
            query = """
                SELECT job_title, job_description,
                ts_rank(to_tsvector(job_title || ' ' || coalesce(job_description, '')),
                        websearch_to_tsquery(:v)) as rank
                FROM job_listings
                WHERE to_tsvector(job_title || ' ' || coalesce(job_description, '')) @@
                      websearch_to_tsquery(:v)
                ORDER BY rank DESC;
            """
            df = pd.read_sql_query(query, con=engine, params={"v": search_words})
            return df.to_dict(orient='records')
        except Exception as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            print("Connection to the PostgreSQL closed.")
    else:
        print("Connection to the PostgreSQL encountered an error.")
        return None

# Example usage
search_words = 'technology, python, web development'
recommendations = get_recommendations(search_words)

if recommendations:
    print(recommendations)
else:
    print("Failed to fetch recommendations.")
