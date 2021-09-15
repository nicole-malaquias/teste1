from flask import Blueprint, jsonify
from app.services import get_by_id


bp_animes = Blueprint('animes/<int:anime_id>', __name__, url_prefix='/api')


@bp_animes.route('/animes/<int:anime_id>',methods = ['GET'])
def filter(anime_id):
    
    query = get_by_id(anime_id)
    if len(query) == 0 :
        return jsonify(query),404
    return str(query)