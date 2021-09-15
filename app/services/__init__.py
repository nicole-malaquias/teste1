import os 
from dotenv import load_dotenv
import psycopg2

USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')


conn = psycopg2.connect(host="localhost", database=DB_NAME,
                            user=USER, password=PASSWORD)

def convert_out(reply):
    transform_data = reply[0][2].strftime('%d/%m/%Y')
    new_reply = {"data":[{"id":reply[0][0],"anime":reply[0][1],"released_date":transform_data,"season":reply[0][3]}]}
    return new_reply

def delete(id):
    is_exists = to_find(id) 
    print(is_exists)
    return is_exists


def create_table() :

    cur = conn.cursor()
    
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
  
def add_anime(data):
    
    create_table()
    cur = conn.cursor()
    anime = data['anime'].title()
    season = data['seasons']
    released_date = data['released_date']
    
    query = f"SELECT anime FROM animes WHERE anime like '{anime}'"
    cur.execute(query)
    registros = list(cur.fetchall())
    
    if len(registros) > 0 :
        conn.commit()
        cur.close()
       
        return []
        
    document = (anime, released_date, season)
    insert = 'insert into animes (anime,released_date,seasons) values (%s,%s,%s);'
    cur.execute(insert,document)
    
    conn.commit()
    cur.close()
   
    return list(document)

def load_animes():
    create_table()
    cur = conn.cursor()
    query = f"SELECT * FROM animes"
    cur.execute(query)
    registros = list(cur.fetchall())
    
    if len(registros) > 0 :
        conn.commit()
        cur.close()

        return registros
    
    conn.commit()
    cur.close()
   
        
    return {"data":[]}

def get_by_id(id):
    create_table()
    cur = conn.cursor()
    
    query = f"SELECT * FROM animes WHERE animes.id = {id}"
    cur.execute(query)
    reply = cur.fetchall()
    
    if len(list(reply)) > 0 :
        converted = convert_out(reply)
        cur.close()
        return converted
    
    cur.close()
    return {"data":[]}

def update_anime(id,data):
    
    is_exists = to_find(id)
    if not is_exists:
        return False
    
    anime = 'anime' in data 
    season = 'seasons' in data 
    released_date = 'released_date' in data 
    
    cur = conn.cursor()
    
    if anime :
        anime = data['anime'].title()
        str = 'anime'
        query = f'update animes set {str} = {anime} where animes.id = {id}'
        cur.execute(query)
        
    if season :
        season = data['seasons']
        str = 'seasons'
        query = f'update animes set {str} = {season} where animes.id = {id}'
        cur.execute(query)
    
    if released_date :
        released_date = data['released_date']
        str = 'released_date'
        query = f'update animes set {str} = {released_date} where animes.id = {id}'
        cur.execute(query)
    
    reply = f'select * from animes where animes.id = {id}'
    cur.execute(reply)
    reply = cur.fetchall()
    converted = convert_out(reply)
    
    cur.close()
    return converted


def to_find(id):
    
    cur = conn.cursor()
    query = f'select * from animes where animes.id = {id}'
    cur.execute(query)
    reply = cur.fetchall()

    return reply
    


