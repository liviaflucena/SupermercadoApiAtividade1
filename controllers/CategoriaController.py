from flask import Blueprint, request, jsonify
import sqlite3
from models.Categorias import Categoria

categoria_blueprint = Blueprint('categoria', __name__)

def findAll():
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM categorias")
        resultset = cursor.fetchall()
        
        items = []
        for item in resultset:
            obj = Categoria(*item)
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
        cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            item = Categoria(*resultset)
            return jsonify(item.toJson()), 200
        else:
            return jsonify({'mensagem': 'Categoria não encontrada'}), 404
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
        cursor.execute(f"INSERT INTO categorias ({columns}) VALUES ({placeholders})", tuple(item_data.values()))

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

        cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            updates = ', '.join([f"{key} = ?" for key in item_data.keys()])
            cursor.execute(f"UPDATE categorias SET {updates} WHERE id = ?", (*item_data.values(), id))
            connection.commit()
            connection.close()

            item_data['id'] = id
            return jsonify(item_data), 200
        else:
            return jsonify({'mensagem': 'Categoria não encontrada'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def delete(id):
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM categorias WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            cursor.execute("DELETE FROM categorias WHERE id = ?", (id,))
            connection.commit()
            connection.close()
            return jsonify({'mensagem': 'Categoria removida com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Categoria não encontrada'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# Rotas do blueprint

@categoria_blueprint.route('/', methods=['GET'])
def getAllCategorias():
    return findAll()

@categoria_blueprint.route('/<int:id>', methods=['GET'])
def getCategoriaById(id):
    return findById(id)

@categoria_blueprint.route('/', methods=['POST'])
def createCategoria():
    return insert()

@categoria_blueprint.route('/<int:id>', methods=['PUT'])
def updateCategoria(id):
    return update(id)

@categoria_blueprint.route('/<int:id>', methods=['DELETE'])
def deleteCategoria(id):
    return delete(id)
