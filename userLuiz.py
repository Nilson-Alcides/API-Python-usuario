from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import mysql.connector


# Configuração do MySQL
#db_config = {
 #   "host": "localhost",
  #  "port" : "3306",  # ajuste para a sua porta
   # "user": "root",       # ajuste para o seu usuário
    #"password": "P@ssw0rd", # ajuste para sua senha
    #"database": "userAPI"
#}

app = FastAPI()

def get_connection():
    return mysql.connector.connect(**db_config)


class Usuario(BaseModel):
    id: int | None = None
    nomeUsu: str
    cargo: str
    dataNasc: datetime

@app.get("/usuarios")
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

@app.get("/usuarios/{idUsu}")
def buscar_usuarios(idUsu: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuario WHERE idUsu = %s",(idUsu,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return result
    return {"erro": "Usuário não encontrado"}

@app.post("/usuarios")
def adicionar_usuario(usuario: Usuario):
    conn = get_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO usuarios (nomeUsu, cargo, dataNasc) VALUES (%s, %s, %s)"
    values = (usuario.nomeUsu, usuario.cargo, usuario.dataNasc)
    cursor.execute(sql, values)
    conn.commit()
    new_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return {"mensagem": "Usuário inserido com sucesso", "id": new_id}

@app.put ("/usuarios/{idUsu}")
def atualizar_usuario(idUsu: int, usuario: Usuario):
    conn = get_connection()
    cursor = conn.cursor
    sql = "UPDATE usuario SET nomeUsu = %s, cargo = %s, dataNasc = %s WHERE idUsu = %s"
    values = (usuario.nomeUsu, usuario.cargo, usuario.dataNasc)
    cursor.execute(sql, values)
    conn.commit()
    cursor.close()
    conn.close()
    return {"mensagem": f"Usuário {idUsu} atualizado com sucesso"}

@app.delete("/usuarios/{idUsu}")
def excluir_usuario(idUsu:int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuario WHERE idUsu= %s", (idUsu))
    conn.commit()
    cursor.close()
    conn.close()
    return{"mensagem": f"Usuário {idUsu} excluído com sucesso!"}
