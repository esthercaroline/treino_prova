from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
from flask_pymongo import PyMongo
from credentials_file import *
app = Flask("Lanchonete da teté")




app.config["MONGO_URI"] = f"mongodb+srv://{credentials['user_mongo']}:{credentials['password_mongo']}@{settings['host']}/{settings['database']}?retryWrites=true&w=majority"
mongo = PyMongo(app)


@app.route('/cardapio', methods=['GET'])
def lista_cardapio():
    try:
        filter_ = {}
        projection_ = {}
        cardapio = list(mongo.cardapio.comidas.find(filter_, projection_))
        if not cardapio:
            return jsonify({"erro": "Nenhum prato encontrado"}), 404
        for comida in cardapio:
            comida["_id"] = str(comida["_id"])
        return {"Cardápio": comida}, 200
    except Exception as e: 
        return {'erro': f'{e}'}


@app.route('/cardapio', methods=['POST'])
def cadastra_prato():
    try: 
            
        data_dict = {
            "nome": request.form.get('nome'),
            "descricao": request.form.get('descricao'),
            "tipo": request.form.get('tipo'),
            "preco": request.form.get('preco')
        }

        if not all(k in data_dict for k in ("nome", "descricao", "tipo",  "preco")):
            return jsonify({"erro": "Campos obrigatórios faltando!"}), 400
        
        if isinstance(data_dict):
            cardapio_id = mongo.db.comidas.insert_one(data_dict)
            return {"_id": str(cardapio_id.inserted_id)}, 201
        else:
            return jsonify({"erro": "Dados inválidos"}), 400

    except Exception as e: 
        return {'erro': f'{e}'}

@app.route('/cardapio/<string:prato_id>', methods=['GET'])
def get_prato_by_id(prato_id):
    try:
        filter_ = {"_id": ObjectId(prato_id)}
        projection_ = {}
        prato = mongo.cardapio.comidas.find_one(filter_, projection_)
        if not prato:
            return jsonify({"erro": "Prato não encontrado"}), 404
        prato["_id"] = str(prato["_id"])
        return {"Prato": prato}, 200
    except Exception as e: 
        return {'erro': f'{e}'}


@app.route('/cardapio/nome/<string:nome_prato>', methods=['GET'])
def get_prato_by_nome(nome_prato):
    try:
        filter_ = {"nome": nome_prato}
        projection_ = {}
        pratos = list(mongo.cardapio.comidas.find(filter_, projection_))
        if not pratos:
            return jsonify({"erro": "Prato não encontrado"}), 404
        for prato in pratos:
            prato["_id"] = str(prato["_id"])
        return {"Pratos": pratos}, 200
    except Exception as e: 
        return {'erro': f'{e}'}


if __name__ == '__main__':
    app.run(debug=True, threaded=True)