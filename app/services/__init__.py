import os 
from dotenv import load_dotenv
import psycopg2

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')


conn = psycopg2.connect(host="localhost", database=DB_NAME,
                            user=USER, password=PASSWORD)

cur = conn.cursor()


def create_database() :
    
    cur.execute("""
            create table if not exists animes (
            id BIGSERIAL primary key ,
            anime varchar(100) not null unique,
            released_date date not null , 
            seasons integer not null
            );
            """)
    conn.commit()
    cur.close()
    conn.close()


def add_anime(data):
    
    anime = data['anime'].title()
    season = data['season']
    released_date = data['released_date']
    
    query = f"SELECT anime FROM animes WHERE anime like '{anime}'"
    cur.execute(query)
    registros = list(cur.fetchall())
    
    if len(registros) > 0 :
        conn.commit()
        cur.close()
        conn.close()
        return []
        
    document = (anime, released_date, season)
    insert = 'insert into animes (anime,released_date,seasons) values (%s,%s,%s);'
    cur.execute(insert,document)
    
    conn.commit()
    cur.close()
    conn.close()
    
    return list(document)

def load_animes():
    
    query = f"SELECT * FROM animes"
    cur.execute(query)
    registros = list(cur.fetchall())
    
    if len(registros) > 0 :
        conn.commit()
        cur.close()
        conn.close()
        
        return registros
    
    conn.commit()
    cur.close()
    conn.close()
        
    return {"data":[]}


def get_by_id(id):
    
    query = f"SELECT * FROM animes WHERE animes.id = {id}"
    cur.execute(query)
    reply = cur.fetchall()
    
    if len(list(reply)) > 0 :
        
        transform_data = reply[0][2].strftime('%d/%m/%Y')
        new_reply = {"data":[{"id":reply[0][0],"anime":reply[0][1],"released_date":transform_data,"season":reply[0][3]}]}
        
        cur.close()
        conn.close()
        return new_reply
    
    cur.close()
    conn.close()
    return {"data":[]}