from flask_restful import Resource
from models.store import StoreModel


class Store(Resource):
    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': 'Store schon vorhanden'}, 400
        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {'message': 'Store konnte nicht angelegt werden'}, 500
        return store.json(), 201

    def delete(self, name):
        store= StoreModel.find_by_name(name)
        if store:
            try:
                store.delete()
            except:
                return {'message': 'Store konnte nicht gelöscht werden'}, 500
        return {'message': 'Store wurde gelöscht '}


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.query.all()]}
