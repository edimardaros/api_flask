from flask_restful import Resource

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