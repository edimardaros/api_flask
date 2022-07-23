from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
  {
    'hotel_id': 'alpha',
    'nome': 'Alpha Hotel',
    'estrelas': 4.3,
    'diaria': 420.34,
    'cidade': 'Rio de Janeiro'
  },
  {
    'hotel_id': 'bravo',
    'nome': 'Bravo Hotel',
    'estrelas': 3.3,
    'diaria': 320.11,
    'cidade': 'Criciuma'
  },
  {
    'hotel_id': 'charlie',
    'nome': 'Charlie Hotel',
    'estrelas': 4.8,
    'diaria': 497.99,
    'cidade': 'Criciuma'
  }
]

class Hoteis(Resource):
  def get(self):
    return {'hoteis': hoteis}

class Hotel(Resource):

  argumentos = reqparse.RequestParser()
  argumentos.add_argument('nome')
  argumentos.add_argument('estrelas')
  argumentos.add_argument('diaria')
  argumentos.add_argument('cidade')

  def get(self, hotel_id):
    hotel = Hotel.find_hotel(hotel_id)
    if hotel:
      return hotel
    return {'message': 'Hotel not found'}, 404
  
  def post(self, hotel_id):
    if HotelModel.find_hotel(hotel_id):
      return {"message": "Hotel Id '{}' already exists.".format(hotel_id)}, 400 # Bad Request

    dados = Hotel.argumentos.parse_args()
    hotel = HotelModel(hotel_id, **dados)
    hotel.save_hotel()
    return hotel.json()

    

  def put(self, hotel_id):
    
    dados = Hotel.argumentos.parse_args()
    hotel_objeto = HotelModel(hotel_id, **dados)
    novo_hotel = hotel_objeto.json()
    hotel = Hotel.find_hotel(hotel_id)
    if hotel:
      hotel.update(novo_hotel)
      return novo_hotel, 200
    hoteis.append(novo_hotel)
    return novo_hotel, 201 # 201 created

  def delete(self, hotel_id):
    global hoteis # evitar erro UnboundLocalError: local variable 'hoteis' referenced before assignment
    hoteis = [hotel for hotel in hoteis if hotel['hotel_id'] != hotel_id]
    return {'message': 'Hotel Deleted'}
