from flask import Blueprint, request, jsonify
from datetime import date, datetime
from app.services import add_anime , load_animes, delete, get_by_id ,update_anime
class FieldError(Exception):

    
    def __init__(self, data):
        
        data = list(data)
        problem = [ i for i in data if i not in ["anime","season","released_date"] ]
        
        self.message = {
            "available_keys": [
                "anime", "released_date","season",
                ],
            "Wrong_keys_sended": [*problem]          
        }
        super().__init__(self.message)


from flask import Blueprint
bp_animes = Blueprint('animes', __name__, url_prefix='/api')


@bp_animes.route('/animes',methods = ['POST','GET'])
def get_create():
    
    typeMethod = request.method
    
    if typeMethod == 'POST':
        
        data = request.get_json()
        find_anime = 'anime' in data
        find_season = 'seasons' in data
        find_release = 'released_date' in data

        try :
            if  find_anime and find_season and find_release  :
            
                add_to_db = add_anime(data)  
                
                if len(add_to_db) == 0 :
                    
                    return {"error":"anime is already exists"},409
                
                return jsonify(add_to_db),201
            
            raise FieldError(data)
        
    
        except FieldError as err :
            
            return jsonify(err.message),422
    else :
        load = load_animes()
        
        return jsonify(load)
     
@bp_animes.route('/animes/<int:anime_id>',methods = ['GET'])
def filter(anime_id):
    
    query = get_by_id(anime_id)

    data = query['data']
    
    if len(data) == 0 : 
        return {"error":"Not Found"},404
    return str(query)   
    
@bp_animes.route('/animes/<int:anime_id>',methods = ['DELETE'])
def delete(anime_id):

    query = delete(anime_id)
    
    if query:
        return '',204
    return {"error":"Not Found"}
    
@bp_animes.route('/animes/<int:anime_id>',methods = ['PATCH'])
def update(anime_id):
    
    data = request.get_json()
  
    try :
        lista = list(data)
        quantity = len(lista)
        is_valid = [x for x in lista if x in ["anime","released_date","seasons"]]
        
        if len(is_valid) == quantity :
            reply =  update_anime(anime_id,data) 
            if reply :
                return reply,200
            return {"error":"Not Found"},404
            
        raise FieldError(data)
        
    
    except FieldError as err :
        
        return jsonify(err.message),422    
    
    
    
    
    