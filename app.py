from flask import Flask, jsonify
from controllers.UsuarioController import usuario_blueprint
from controllers.CategoriaController import categoria_blueprint
from controllers.ProdutoController import produto_blueprint
from controllers.SetorController import setor_blueprint

app = Flask(__name__)


app.register_blueprint(usuario_blueprint, url_prefix='/usuarios')
app.register_blueprint(categoria_blueprint, url_prefix='/categorias')
app.register_blueprint(produto_blueprint, url_prefix='/produtos')
app.register_blueprint(setor_blueprint, url_prefix='/setores')

@app.route("/")
def homeResource():
    aplicacao = {'versao': '1.0'}
    return jsonify(aplicacao), 200

if __name__ == '__main__':
    app.run(debug=True)
