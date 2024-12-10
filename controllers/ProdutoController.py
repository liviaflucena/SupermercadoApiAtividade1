from flask import Blueprint, request, jsonify
import sqlite3
from models.Produtos import Produto

produto_blueprint = Blueprint('produto', __name__)

def findAll():
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM produtos")
        resultset = cursor.fetchall()
        
        items = []
        for item in resultset:
            obj = Produto(*item)
            items.append(obj.toJson())
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()
    
    return jsonify(items), 200

def findById(id):
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            item = Produto(*resultset)
            return jsonify(item.toJson()), 200
        else:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        connection.close()

def insert():
    try:
        item_data = request.json
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()

        columns = ', '.join(item_data.keys())
        placeholders = ', '.join('?' * len(item_data))
        cursor.execute(f"INSERT INTO produtos ({columns}) VALUES ({placeholders})", tuple(item_data.values()))

        connection.commit()
        item_data['id'] = cursor.lastrowid
        connection.close()

        return jsonify(item_data), 200
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def update(id):
    try:
        item_data = request.json
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            updates = ', '.join([f"{key} = ?" for key in item_data.keys()])
            cursor.execute(f"UPDATE produtos SET {updates} WHERE id = ?", (*item_data.values(), id))
            connection.commit()
            connection.close()

            item_data['id'] = id
            return jsonify(item_data), 200
        else:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def delete(id):
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
            connection.commit()
            connection.close()
            return jsonify({'mensagem': 'Produto removido com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Produto não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# Rotas do blueprint

@produto_blueprint.route('/', methods=['GET'])
def getAllProdutos():
    return findAll()

@produto_blueprint.route('/<int:id>', methods=['GET'])
def getProdutoById(id):
    return findById(id)

@produto_blueprint.route('/', methods=['POST'])
def createProduto():
    return insert()

@produto_blueprint.route('/<int:id>', methods=['PUT'])
def updateProduto(id):
    return update(id)

@produto_blueprint.route('/<int:id>', methods=['DELETE'])
def deleteProduto(id):
    return delete(id)
