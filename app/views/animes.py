from flask import Blueprint, request, jsonify
from datetime import date, datetime
from app.services import add_anime , load_animes

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
        find_season = 'season' in data
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
    
    
    

    
    
    
    
    
    
    
    



# Em vez de @app, utilizamos a instancia de blueprint criada, bp_anime
