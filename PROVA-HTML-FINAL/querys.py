import mysql.connector

conn = mysql.connector.connect(                    
    host = "bd-grupo-07.mysql.uhserver.com",
    user = "impacta_grupo07",
    password = "O433dln*ecv43",
    database="bd_grupo_07"
)

cursor = conn.cursor()   



sql_select = f'SELECT USUARIO, SENHA FROM CADASTRO WHERE USUARIO = "admin"'
cursor.execute(sql_select)
resultado = cursor.fetchall()


usuario_bd = resultado[0][0]
senha_bd_cript = resultado[0][1]

print(usuario_bd)
print(senha_bd_cript)