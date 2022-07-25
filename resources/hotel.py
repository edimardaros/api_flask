from multiprocessing import connection
import string
from pkg_resources import require
from flask_restful import Resource, reqparse
from resources.filtros import normalize_path_params, consulta_com_cidade, consulta_sem_cidade
from models.hotel import HotelModel
from flask_jwt_extended import jwt_required
import sqlite3

# path /hoteis?cidade=Criciuma&estrelas_min=4&diaria_max=400
path_params = reqparse.RequestParser()
path_params.add_argument('cidade', type=str)
path_params.add_argument('estrelas_min', type=float)
path_params.add_argument('estrelas_max', type=float)
path_params.add_argument('diaria_min', type=float)
path_params.add_argument('diaria_max', type=float)
path_params.add_argument('limit', type=float)
path_params.add_argument('offset', type=float)


class Hoteis(Resource):
  def get(self):
    connection = sqlite3.connect('banco.db')
    cursor = connection.cursor()

    dados = path_params.parse_args()
    # dados = {'limit': 50, 'diaria_min': None}
    # dados['limit']
    dados_validos = {chave:dados[chave] for chave in dados if dados[chave] is not None}
    parametros = normalize_path_params(**dados_validos)

    if not parametros.get('cidade'):
      tupla = tuple([parametros[chave] for chave in parametros])
      resultado = cursor.execute(consulta_sem_cidade, tupla)
    else:
      tupla = tuple([parametros[chave] for chave in parametros])
      resultado = cursor.execute(consulta_com_cidade, tupla)

    hoteis = []
    for linha in resultado:
      hoteis.append({
        'hotel_id' : linha[0],
        'nome' : linha[1],
        'estrelas' : linha[2],
        'diaria' : linha[3],
        'cidade' : linha[4],
        'site_id': linha[5]
      })
    return {'hoteis': hoteis}
    # return {'hoteis': [hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):

  argumentos = reqparse.RequestParser()
  argumentos.add_argument('nome', type=str, required=True, help="The field 'name' is required.")
  argumentos.add_argument('estrelas', type=float, required=True, help="The field 'estrelas' is required.")
  argumentos.add_argument('diaria')
  argumentos.add_argument('cidade')
  argumentos.add_argument('site_id', type=int, required=True, help="The field 'site_id' is required.")

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
