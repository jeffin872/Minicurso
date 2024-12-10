#Importações
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

#Instanciação do flask e do banco de dados
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#Modelos
class Minicurso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    
    #Criando uma relação de um para muitos, entre o minicurso e os participantes
    participantes = db.relationship('Participante', backref='minicurso')

class Participante(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    minicurso_id = db.Column(db.Integer, db.ForeignKey('minicurso.id'), nullable=False)

# Inicializa o banco de dados uma unica vez 
with app.app_context():
    db.create_all()

# Página inicial (redireciona para os minicursos por padrão)
@app.route('/')
def home():
    return redirect(url_for('listar_minicursos'))

# Página de participantes
@app.route('/participantes', methods=['GET'])
def listar_participantes():
    participantes = Participante.query.all()
    minicursos = Minicurso.query.all()
    return render_template('participantes.html', participantes=participantes, minicursos=minicursos)

# Página de minicursos
@app.route('/minicursos', methods=['GET'])
def listar_minicursos():
    minicursos = Minicurso.query.all()
    return render_template('minicursos.html', minicursos=minicursos)

# Rota para adicionar participante
@app.route('/adicionar_participante', methods=['POST'])
def adicionar_participante():
    nome = request.form['name']
    idade = int(request.form['age'])
    telefone = request.form['phone']
    minicurso_id = int(request.form['minicurso_id'])

    # Verificação de minicurso
    minicurso = Minicurso.query.get(minicurso_id)
    if not minicurso:
        return render_template('erro.html', mensagem="Minicurso não encontrado!")

    #Adicionando no banco de dados
    participante = Participante(name=nome, age=idade, phone=telefone, minicurso_id=minicurso_id)
    db.session.add(participante)
    db.session.commit()
    return redirect(url_for('listar_participantes'))

# Rota para remover participante
@app.route('/remover_participante/<int:id>', methods=['POST'])
def remover_participante(id):
    participante = Participante.query.get(id)
    
    #verificação se o participante existe, se sim deleta do banco
    if participante:
        db.session.delete(participante)
        db.session.commit()
    return redirect(url_for('listar_participantes'))

# Rota para adicionar minicurso
@app.route('/adicionar_minicurso', methods=['POST'])
def adicionar_minicurso():
    
    #Verificações se o titulo está vázio ou já é existente no banco
    titulo = request.form['title']
    if titulo.strip() == "":
        return render_template('erro.html', mensagem="Título do minicurso não pode estar vazio!")
    
    minicursoexistente = Minicurso.query.filter_by(title=titulo).first()
    if minicursoexistente:
        return render_template('erro.html', mensagem="Título do minicurso já existe!")
    
    
    #Adicionando no banco de dados
    minicurso = Minicurso(title=titulo)
    db.session.add(minicurso)
    db.session.commit()
    
    #Aqui ele redireciona para a função listar_minicursos, o 'url_for' faz a 'tradução' da 
    # função listar_mincursos para a rota /minicurso na url do navegador. Em resumo ele recarrega a página
    return redirect(url_for('listar_minicursos'))

# Rota para remover minicurso
@app.route('/remover_minicurso/<int:id>', methods=['POST'])
def remover_minicurso(id):
    minicurso = Minicurso.query.get(id)
    if minicurso:
        # Remover participantes relacionados primeiro
        Participante.query.filter_by(minicurso_id=id).delete()
        db.session.delete(minicurso)
        db.session.commit()
    return redirect(url_for('listar_minicursos'))

#Rota para alterar os participantes
@app.route('/alterar_participante', methods=['POST'])
def alterar_participante():
    #Pegar os atributos dos participantes do front e inicializar as variaveis no back
    participant_id = int(request.form['participant_id'])
    name = request.form['name']
    age = int(request.form['age'])
    phone = request.form['phone']
    minicurso_id = int(request.form['minicurso_id'])

    # Busca o participante no banco de dados
    participante = Participante.query.get(participant_id)
    if not participante:
        return render_template('erro.html', mensagem="Participante não encontrado!")

    # Salvando as alterações no banco de dados
    participante.name = name
    participante.age = age
    participante.phone = phone
    participante.minicurso_id = minicurso_id
    db.session.commit()

    return redirect(url_for('listar_participantes'))

if __name__ == '__main__':
    app.run(debug=True)
