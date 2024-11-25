from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Use as variáveis de ambiente para configurar a URI do PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ.get("POSTGRES_USER")}:{os.environ.get("POSTGRES_PASSWORD")}@db:5432/{os.environ.get("POSTGRES_DB")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo de Produto
class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

# Criação do banco de dados
with app.app_context():
    db.create_all()

# Rotas CRUD
# Criar Produto
@app.route('/produtos', methods=['POST'])
def criar_produto():
    data = request.get_json()
    novo_produto = Produto(nome=data['nome'], preco=data['preco'])
    db.session.add(novo_produto)
    db.session.commit()
    return jsonify({'id': novo_produto.id}), 201

# Ler todos os Produtos
@app.route('/produtos', methods=['GET'])
def listar_produtos():
    produtos = Produto.query.all()
    produtos_list = [{'id': p.id, 'nome': p.nome, 'preco': p.preco} for p in produtos]
    return jsonify(produtos_list), 200

# Ler Produto por ID
@app.route('/produtos/<int:id>', methods=['GET'])
def obter_produto(id):
    produto = Produto.query.get_or_404(id)
    return jsonify({'id': produto.id, 'nome': produto.nome, 'preco': produto.preco}), 200

# Atualizar Produto
@app.route('/produtos/<int:id>', methods=['PUT'])
def atualizar_produto(id):
    data = request.get_json()
    produto = Produto.query.get_or_404(id)
    produto.nome = data['nome']
    produto.preco = data['preco']
    db.session.commit()
    return jsonify({'message': 'Produto atualizado com sucesso'}), 200

# Deletar Produto
@app.route('/produtos/<int:id>', methods=['DELETE'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    db.session.delete(produto)
    db.session.commit()
    return jsonify({'message': 'Produto deletado com sucesso'}), 200

# Rota para renderizar o front-end
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
