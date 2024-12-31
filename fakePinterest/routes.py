#rotas do site(links)
from flask import render_template, url_for, redirect
from fakePinterest import app, database, bcrypt
from fakePinterest.models import Usuario, Foto
from flask_login import login_required, login_user, logout_user, current_user
from fakePinterest.forms import FormLogin, FormCriarConta, FormFoto
import os
from werkzeug.utils import secure_filename

#Homepage do site
@app.route("/", methods=["GET", "POST"])
def homepage():
    form_login = FormLogin()
    if form_login.validate_on_submit(): #Verificar se todos os campos foram preenchidos e são validos e se o botão de confirmação foi clicado
        usuario = Usuario.query.filter_by(email=form_login.email.data).first() #Verifica se o email e senha digitados consta na base de dados e faz o login     
        if usuario and bcrypt.check_password_hash(usuario.senha.encode("utf-8"), form_login.senha.data):
            login_user(usuario)
            return redirect(url_for("perfil", id_usuario=usuario.id))   #Redirecion para a pagina do perfil do usuario
    return render_template("homepage.html", form=form_login)

#Pagina de cadastro
@app.route("/criarconta", methods=["GET", "POST"])
def criarconta():
    form_criarconta= FormCriarConta()
    if form_criarconta.validate_on_submit():

        senha = bcrypt.generate_password_hash(form_criarconta.senha.data).decode("utf-8")   # Método para criptografar a senha digitada pelo usuario

        usuario = Usuario(username=form_criarconta.username.data, #Cria o usuário
                          senha=senha,
                          email=form_criarconta.email.data)
        
        database.session.add(usuario)       #Salva no banco de dados
        database.session.commit()
        
        login_user(usuario, remember=True)
        return redirect(url_for("perfil", id_usuario=usuario.id))
    return render_template("criarconta.html", form=form_criarconta)

#Pagina do perfil do usuário
@app.route("/perfil/<id_usuario>", methods=["GET", "POST"])     
@login_required                         #Pagina só pode ser acessada por usuário logado
def perfil(id_usuario):
    if int(id_usuario) == int(current_user.id): #Se o usuario é o dono do perfil
        form_foto=FormFoto()        #Habilita a classe Formfoto(Postar foto) na pagina de perfil
        if form_foto.validate_on_submit():
            arquivo = form_foto.foto.data
            nome_seguro = secure_filename(arquivo.filename)              #Transforma o nome do arquivo em um nome seguro
            caminho = os.path.join(os.path.abspath(os.path.dirname(__file__)), #Caminho da pasta do projeto onde será salvo o arquivo
                              app.config["UPLOAD_FOLDER"],
                              nome_seguro)
            arquivo.save(caminho) #Salva o arquivo na pasta post
            foto = Foto(imagem= nome_seguro , id_usuario=current_user.id) #"Cria" a foto
            database.session.add(foto) #Registra no banco de dados
            database.session.commit()
        return render_template("perfil.html", usuario=current_user, form=form_foto)
    else:
        usuario = Usuario.query.get(int(id_usuario)) #Se o usuario é um visitante
        return render_template("perfil.html", usuario=usuario, form=None)

#Pagina de logout
@app.route("/Logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))

#Pagina de feed
@app.route("/feed")
@login_required
def feed():
    fotos= Foto.query.order_by(Foto.data_criacao.desc()).all() #Pega todas as fotos do banco de dados
    return render_template("feed.html", fotos=fotos)