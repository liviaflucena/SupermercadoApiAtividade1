from flask import Blueprint, request, jsonify
import sqlite3
from models.Setores import Setor

setor_blueprint = Blueprint('setor', __name__)

def findAll():
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM setores")
        resultset = cursor.fetchall()
        
        items = []
        for item in resultset:
            obj = Setor(*item)
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
        cursor.execute("SELECT * FROM setores WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            item = Setor(*resultset)
            return jsonify(item.toJson()), 200
        else:
            return jsonify({'mensagem': 'Setor não encontrado'}), 404
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
        cursor.execute(f"INSERT INTO setores ({columns}) VALUES ({placeholders})", tuple(item_data.values()))

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

        cursor.execute("SELECT * FROM setores WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            updates = ', '.join([f"{key} = ?" for key in item_data.keys()])
            cursor.execute(f"UPDATE setores SET {updates} WHERE id = ?", (*item_data.values(), id))
            connection.commit()
            connection.close()

            item_data['id'] = id
            return jsonify(item_data), 200
        else:
            return jsonify({'mensagem': 'Setor não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def delete(id):
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM setores WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            cursor.execute("DELETE FROM setores WHERE id = ?", (id,))
            connection.commit()
            connection.close()
            return jsonify({'mensagem': 'Setor removido com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Setor não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# Rotas do blueprint

@setor_blueprint.route('/', methods=['GET'])
def getAllSetores():
    return findAll()

@setor_blueprint.route('/<int:id>', methods=['GET'])
def getSetorById(id):
    return findById(id)

@setor_blueprint.route('/', methods=['POST'])
def createSetor():
    return insert()

@setor_blueprint.route('/<int:id>', methods=['PUT'])
def updateSetor(id):
    return update(id)

@setor_blueprint.route('/<int:id>', methods=['DELETE'])
def deleteSetor(id):
    return delete(id)
