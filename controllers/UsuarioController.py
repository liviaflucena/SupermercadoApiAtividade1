from flask import Blueprint, request, jsonify
import sqlite3
from models.Usuarios import Usuario

usuario_blueprint = Blueprint('usuario', __name__)

def findAll():
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM usuarios")
        resultset = cursor.fetchall()
        
        items = []
        for item in resultset:
            obj = Usuario(*item)
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
        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            item = Usuario(*resultset)
            return jsonify(item.toJson()), 200
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
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
        cursor.execute(f"INSERT INTO usuarios ({columns}) VALUES ({placeholders})", tuple(item_data.values()))

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

        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            updates = ', '.join([f"{key} = ?" for key in item_data.keys()])
            cursor.execute(f"UPDATE usuarios SET {updates} WHERE id = ?", (*item_data.values(), id))
            connection.commit()
            connection.close()

            item_data['id'] = id
            return jsonify(item_data), 200
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

def delete(id):
    try:
        connection = sqlite3.connect('supermercado.db')
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
        resultset = cursor.fetchone()

        if resultset is not None:
            cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))
            connection.commit()
            connection.close()
            return jsonify({'mensagem': 'Usuário removido com sucesso'}), 200
        else:
            return jsonify({'mensagem': 'Usuário não encontrado'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500

# Rotas do blueprint

@usuario_blueprint.route('/', methods=['GET'])
def getAllUsuarios():
    return findAll()

@usuario_blueprint.route('/<int:id>', methods=['GET'])
def getUsuarioById(id):
    return findById(id)

@usuario_blueprint.route('/', methods=['POST'])
def createUsuario():
    return insert()

@usuario_blueprint.route('/<int:id>', methods=['PUT'])
def updateUsuario(id):
    return update(id)

@usuario_blueprint.route('/<int:id>', methods=['DELETE'])
def deleteUsuario(id):
    return delete(id)
