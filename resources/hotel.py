from multiprocessing import connection
from pkg_resources import require
from flask_restful import Resource, reqparse
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

def normalize_path_params(cidade=None,
                          estrelas_min=0,
                          estrelas_max=0,
                          diaria_min=0,
                          diaria_max=10000,
                          limit=50,
                          offset=0, **dados):
  if cidade:
    return {
      'estrelas_min' : estrelas_min,
      'estelas_max': estrelas_max,
      'diaria_min' : diaria_min,
      'diaria_max' : diaria_max,
      'cidade': cidade,
      'limit': limit,
      'offset':offset
    }
  return {
    'estrelas_min' : estrelas_min,
      'estelas_max': estrelas_max,
      'diaria_min' : diaria_min,
      'diaria_max' : diaria_max,
      'limit': limit,
      'offset':offset
  }


# path /hoteis?cidade=Criciuma&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=srt)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
  def get(self):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursos()

    dados = path_params.parse_args()
    # dados = {'limit': 50, 'diaria_min': None}
    # dados['limit']
    dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
    parametros = normalize_path_params(**dados_validos)

    if parametros.get('cidade'):
      consulta = "SELECT * FROM hoteis \
      WHERE (estrelas >= ? and estrelas <= ?)\
        AND (diaria >= ? and diaria <= ?)\
          LIMIT ? OFFSET ?"

    return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

  argumentos = reqparse.RequestParser()
  argumentos.add_argument('nome', type=str, required=True, help="The field 'name' is required.")
  argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' is required.")
  argumentos.add_argument('diaria')
  argumentos.add_argument('cidade')

  def get(self, hotel_id):
    hotel = HotelModel.find_hotel(hotel_id)
    if hotel:
      return hotel.json()
    return {'message': 'Hotel not found'}, 404
  
  @jwt_required()
  def post(self, hotel_id):
    if HotelModel.find_hotel(hotel_id):
      return {"message": "Hotel Id '{}' already exists.".format(hotel_id)}, 400 # Bad Request

    dados = Hotel.argumentos.parse_args()
    hotel = HotelModel(hotel_id, **dados)
    try:
      hotel.save_hotel()
    except:
      return {'message': 'An internal error ocurred while trying to save'}, 500 # Internal server error
    return hotel.json()

    
  @jwt_required()
  def put(self, hotel_id):
    
    dados = Hotel.argumentos.parse_args()
    
    hotel_encontrado = HotelModel.find_hotel(hotel_id)
    if hotel_encontrado:
      hotel_encontrado.update_hotel(**dados)
      hotel_encontrado.save_hotel()
      return hotel_encontrado.json(), 200
    
    hotel = HotelModel(hotel_id, **dados)
    try:
      hotel.save_hotel()
    except:
      return {'message': 'An internal error ocurred while trying to save'}, 500 # Internal server error
    return hotel.json(), 201 # 201 created

  @jwt_required()
  def delete(self, hotel_id):
    hotel = HotelModel.find_hotel(hotel_id)
    if hotel:
      try:
        hotel.delete_hotel()
      except:
        return {'message': 'An internal error ocurred while trying to save'}, 500 # Internal server error

      return {'message': 'Hotel Deleted'}
    return {'message': 'Hotel not found'}, 404
