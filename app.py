from flask import Flask, Blueprint, render_template, request 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
bp = Blueprint('app', __name__)

user = 'pqbkacfp'
password = 'L7-SaWQJYvQONxhO5mEJuIHd0enRuB5h'
host = 'tuffi.db.elephantsql.com'
database = 'pqbkacfp'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user}:{password}@{host}/{database}'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'frase super secreta'

db = SQLAlchemy(app)

# DEFINIÇÃO DA CLASSE E MODELAGEM DO DATA BASE DE ACORDO COM O DBEAVER
class Alimentos(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  nome = db.Column(db.String(100), nullable=False)
  cidade = db.Column(db.String(100), nullable=False)
  telefone = db.Column(db.String(20), nullable=False)
  alimento =  db.Column(db.String(20), nullable=False)
  estado = db.Column(db.String(100), nullable=False)

#CONSTRUÇÃO DA CLASSE ALIMENTOS
  def __init__(self, nome, cidade, telefone, alimento, estado):
    self.nome = nome
    self.cidade = cidade
    self.telefone = telefone
    self.alimento = alimento
    self.estado = estado


#FUNÇÕES DA CLASSE ALIMENTOS

  #FUNÇÃO DE SELECT ALL
  @staticmethod
  def listar_doacoes():
    return Alimentos.query.all()

  #FUNÇÃO DE INSERT
  def save(self):
    db.session.add(self)
    db.session.commit()

  #FUNÇÃO DE DELETE
  def excluir(self):
    db.session.delete(self)
    db.session.commit()

  #FUNÇÃO DE UPDATE
  def editar(self, new_data):
    self.nome = new_data.nome
    self.cidade = new_data.cidade
    self.telefone = new_data.telefone
    self.alimento = new_data.alimento
    self.estado = new_data.estado    
    self.save()

  #FUNÇÃO DE SELECT BY
  @staticmethod
  def ver_alimento(alimento_id):
    return Alimentos.query.get(alimento_id)
   


#ROTAS #ROTAS #ROTAS #ROTAS #ROTAS #ROTAS #ROTAS #ROTAS #ROTAS #ROTAS #ROTAS #ROTAS 

#ROTA INDEX
@bp.route('/')
def index():
  return render_template('index.html')

#ROTA DOACOES
@bp.route('/doacoes')
def listar_doacoes():
  listaDeAlimentos = Alimentos.listar_doacoes()
  return render_template('doacoes.html', listaDeAlimentos = listaDeAlimentos)

#ROTA DOAR
@bp.route('/doar', methods=('GET', 'POST'))
def doar():
  cadastrar = None

  if request.method == 'POST':
    form=request.form
  
    alimento = Alimentos(form['nome'], form['cidade'], form['telefone'], form['alimento'], form['estado'])
    alimento.save()
    cadastrar = alimento.id
  return render_template('doar.html', cadastrar=cadastrar)


#ROTA EDITAR
@bp.route('/editar/<alimento_id>', methods=('GET', 'POST'))
def editar(alimento_id):
  sucesso = None
  alimento = Alimentos.ver_alimento(alimento_id)

  if request.method == 'POST':
    form=request.form
    new_data = Alimentos(form['nome'], form['cidade'], form['telefone'], form['alimento'], form['estado'])
    alimento.editar(new_data)
    sucesso = True
  return render_template('editar.html', alimento=alimento, sucesso=sucesso)


#ROTA EXCLUIR
@bp.route('/excluir/<alimento_id>', methods=('GET', 'POST'))
def excluir(alimento_id):
  sucesso = None
  alimento = Alimentos.ver_alimento(alimento_id)

  if request.method == 'POST':   
    alimento.excluir()
    sucesso = True
  return render_template('excluir.html', alimento=alimento, sucesso=sucesso)




app.register_blueprint(bp)

if __name__ == '__main__':
  app.run(debug=True)
