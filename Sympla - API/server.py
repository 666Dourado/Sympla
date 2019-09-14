from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

from model import modelo

app = Flask(__name__)
api = Api(app)


class EventoById(Resource):
    def get(self, id):
        model = modelo()
        evento = model.recuperaUmEvento(id)

        result = {
                'ulr': evento[0],
                'nome_evento': evento[1],
                'local': evento[2],
                'cidade': evento[3],
                'estado': evento[4],
                'data_inicio': str(evento[5]),
                'data_fim': str(evento[6]),
                'qnt_lotes': str(evento[7]),
                'max_valoringresso': str(evento[8]),
                'data_create': str(evento[9]),
                'tipo_evento': evento[10]
            }
        return jsonify(result)


api.add_resource(EventoById, '/evento/<id>') 

if __name__ == '__main__':
    app.run()