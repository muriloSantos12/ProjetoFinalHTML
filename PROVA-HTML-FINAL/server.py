import flask
import mysql.connector
from flask_login import login_required,logout_user,LoginManager, login_user, current_user, UserMixin
import bcrypt
import datetime

#Defindo Flask
app = flask.Flask(__name__, template_folder = 'templates', static_folder = 'static', static_url_path = '') 


login = LoginManager(app)
login.login_view ='/' #Quando o usuário acessar o site ele e não estiver logado,  vai cair direto na pagina principal de login
app.permanent_session_lifetime = datetime.timedelta(seconds=900)  #Colocando um tempo na sessão do usúario, caso passe o tempo estipulado ele terá que logar dnv
#app.config['SECRET KEY'] = 'SewnigEMogGNIAMGSAGOmgo2'  #Senha de criptografia dos cookies 
key_criptografia = b'x243262243132244850716f3166375753696955556b2e36'  #SENHA DE CRIPTOGRAFIA DA SENHA DO USUÁRIO

@login.user_loader
def user_loader(id):
    return User(id)

class User(UserMixin):
    def __init__(self, username):
        self.id = username


#Definindo conexão com o banco de dados
conn = mysql.connector.connect(                    
    host = "bd-grupo-07.mysql.uhserver.com",
    user = "impacta_grupo07",
    password = "O433dln*ecv43",
    database="bd_grupo_07"
)

#Definindo cursor do banco de dados
cursor = conn.cursor()     



#Definindo a rota principal '/'
@app.route('/', methods = ['GET']) 
def home():

    if flask.request.method == 'GET' :

        if current_user.is_authenticated:  #VERIFICA SE O USUÁRIO ESTÁ AUTENTICADO  (current user vai ver se existe um cookie da aplicacao salva no navegador)
            user = current_user.id
            return flask.render_template('home.html')   

        else:
            return flask.render_template('login.html')

    
#Rota de login usuario
@app.route('/login', methods = ['POST']) 
def login_pagina():

    info = flask.request.form.to_dict()

    usuario = str(info['login_usuario'])
    senha = str(info['login_senha'])
    print(senha)

    if (usuario == '') | (senha == ''):
        return flask.render_template('login.html',status_login="Preecha os campos de autenticação")


    else:
        sql_select = f'SELECT USUARIO, SENHA FROM CADASTRO WHERE USUARIO = "{usuario}"'
        cursor.execute(sql_select)
        resultado = cursor.fetchall()

        if len(resultado) == 0:
            return flask.render_template('login.html', status_login = 'Usuário não encontrado')

        else:
            usuario_bd = resultado[0][0]
            senha_bd_cript = resultado[0][1]
            


            if senha_bd_cript == senha:
                #user = current_user.id
                #login_user(User(user))  #Criando cookie no navegador do usuários
                return flask.render_template('home.html')

            else:
                return flask.render_template('login.html', status_login = 'Senha incorreta')
                print(senha_bd_cript)
                


@app.route('/login', methods = ['GET']) 
def carregar_login_pagina():
    return flask.render_template('login.html')





#Rota de cadastro usuário
@app.route('/cadastro', methods = ['POST'])
def cadastro_usuario():

    info = flask.request.form.to_dict()

    usuario_cad = str(info['cadastro_usuario'])
    senha_cad = str(info['cadastro_senha'])
    confsenha_cad = str(info['cadastro_confisenha'])


    if (usuario_cad  == '') | (senha_cad == '') | (confsenha_cad == ''):
        return flask.render_template('login.html',status_login="Preecha os campos de autenticação")

    elif (senha_cad != confsenha_cad):
        return flask.render_template('login.html',status_login="Senhas divergentes, preencha corretamente")
        

    else:
        sql_select = f'SELECT * FROM CADASTRO WHERE USUARIO = "{usuario_cad}"'
        cursor.execute(sql_select)
        resultado = cursor.fetchall()

        if len(resultado) == 0:
                       

            sql_insert = f'INSERT INTO CADASTRO (USUARIO, SENHA) VALUES ("{usuario_cad}", "{senha_cad}")'
            cursor.execute(sql_insert)
            conn.commit()

            return flask.render_template('login.html',status_login= f'Usuário "{usuario_cad}" cadastrado com sucesso!')

            print(senha_cad_cript)

        else:
            return flask.render_template('login.html',status_login="Usuário já cadastrado")



@app.route('/logout', methods= ['GET'])

def sair():
    return flask.render_template('login.html')



 #Definindo a rota de cadastro de produtos '/cadastrar_produto'
@app.route('/cadastrar_produto', methods = ['POST'])                                      
def cadastro():

    info = flask.request.form.to_dict()
    id_cadastrar = info['cadastrar_id']
    nomeprod_cadastrar = info['cadastrar_nomeproduto']
    preço_cadastrar = info['cadastrar_preço']
    categoria_cadastrar = info['cadastrar_categoria']

 
    if ((id_cadastrar =='') | (nomeprod_cadastrar =='') | (preço_cadastrar == '') | (categoria_cadastrar =='')):
        return flask.render_template('home.html', status ='Preencha os campos corretamente')


    else:
            try:
                sql_select = f'SELECT * FROM PRODUTO WHERE ID = "{id_cadastrar}"'
                cursor.execute(sql_select)
                resultado = cursor.fetchall()
                print (resultado)

                if len(resultado) != 0:
                    return flask.render_template('home.html', status = f'Produto com ID "{id_cadastrar}" já cadastrado')

                else:
                    sql_insert = f'INSERT INTO PRODUTO (ID,NOME,PRECO, CATEGORIA) VALUES ({id_cadastrar},"{nomeprod_cadastrar}",{preço_cadastrar},"{categoria_cadastrar}")'
                    cursor.execute(sql_insert)
                    conn.commit()
                    return flask.render_template('home.html', status = f'Produto "{nomeprod_cadastrar}" cadastrado com sucesso!')
            
            except mysql.connector.errors.ProgrammingError:
                return flask.render_template('home.html', status ='Respeite o tipo dos campos e preencha corretamente')
        


#Definindo a rota de consulta de produtos '/consultar_produto'
@app.route('/consultar_produto', methods = ['POST'])                                             
def consultar():

    info = flask.request.form.to_dict()
    id_consulta = info['consulta_id']


    if id_consulta == '':
        return flask.render_template('home.html', status = 'Preencha o campo corretamente')
    
    else:
        sql_select = f'SELECT * FROM PRODUTO WHERE ID = "{id_consulta}"'
        cursor.execute(sql_select)
        resultado = cursor.fetchall()
        print (resultado)


        if len(resultado) == 0:
            return flask.render_template('home.html', status = 'Produto não cadastrado')

        else:
            resultado_id = resultado[0][0]
            resultado_nome = resultado[0][1]
            resultado_preço = resultado[0][2]
            resultado_categoria = resultado[0][3]

            return flask.render_template('home.html', status = 'Produto localizado!', id = resultado_id, nome = resultado_nome, preco = resultado_preço, categoria = resultado_categoria  )
            





#Definindo a rota de alterar produtos '/alterar_produto'
@app.route('/alterar_produto', methods = ['POST'])                                             
def alterar():
    
    info = flask.request.form.to_dict()
    id_alterar = info['alterar_id']
    nome_alterar = info['alterar_nomeproduto']
    preço_alterar = info['alterar_preço']
    categoria_alterar = info['alterar_categoria']

    if ((id_alterar =='') | (nome_alterar =='') | (preço_alterar == '') | (categoria_alterar =='')):
        return flask.render_template('home.html', status='Preencha os campos corretamente')
    

    else:
        try:
            sql_select = f'SELECT * FROM PRODUTO WHERE ID = "{id_alterar}"'
            cursor.execute(sql_select)
            resultado = cursor.fetchall()
            print (resultado)

            if len(resultado) == 0:
                return flask.render_template('home.html', status='Produto não encontrado')

            else:
                
                sql_update = f'UPDATE PRODUTO SET NOME = "{nome_alterar}", PRECO = "{preço_alterar}", CATEGORIA = "{categoria_alterar}" WHERE ID = "{id_alterar}"'
                cursor.execute(sql_update)
                conn.commit()
                return flask.render_template('home.html', status=f'Produto {id_alterar} alterado com sucesso!')

        except mysql.connector.errors.ProgrammingError:
                return flask.render_template('home.html', status ='Respeite o tipo dos campos e preencha corretamente')
                


#Definindo a rota de excluir produtos '/excluir_produto'
@app.route('/excluir_produto', methods = ['POST'])                                                
def excluir():

   
    info = flask.request.form.to_dict()
    id_excluir = info['excluir_id']


    #Se o preenchimento estiver vazio, não realiza nenhuma exclusão e retorna a página com um aviso de preenchimento
    if id_excluir == '':                                                                          
        return flask.render_template('home.html', status ='Preencha o campo corretamente')


    #Se colocar * no campo, verifica se tem algum registro na tabela
    elif id_excluir == '*':                                                                       

        sql_select = f'SELECT * FROM PRODUTO'
        cursor.execute(sql_select)
        resultado = cursor.fetchall()

         #Se colocar * no campo, e não tiver nenhum registro na tabela, retorna a página avisando que não tem nenhum registro na tabela
        if len(resultado) == 0:                                                                       
            return flask.render_template('home.html', status ='Nenhum produto cadastrado na tabela')


        #Se colocar * no campo, e tiver registro na tabela, realiza a exclusão e retorna a página informando que todos produtos foram excluídos
        else:                                                                                     

            sql_delete = f'DELETE FROM PRODUTO '
            cursor.execute(sql_delete)
            conn.commit()
            return flask.render_template('home.html', status ='Produtos excluídos com sucesso!')


    #Se o campo não for vazio e não for *, faz uma query para verificar se tem o ID na tabela
    else:                                                                                        

        sql_select = f'SELECT * FROM PRODUTO WHERE ID = "{id_excluir}"'
        cursor.execute(sql_select)
        resultado = cursor.fetchall()


        #Se não tiver o ID na tabela, retorna a página informando que não tem o ID cadastrado
        if len(resultado) == 0:                                                                   
            return flask.render_template('home.html', status ='Produto não cadastrado')


         #Se tiver o ID na tabela, exclui o registro de acordo com o ID e retorna a página informando da exclusão
        else:                                                                                    
            sql_delete = f'DELETE FROM PRODUTO WHERE ID = "{id_excluir}"'
            cursor.execute(sql_delete)
            conn.commit()
            return flask.render_template('home.html', status =f'Produto {id_excluir} excluído com sucesso!')



if __name__ == "__main__":
    app.run()