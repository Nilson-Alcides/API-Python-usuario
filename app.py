from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Modelo de dados
class Produto(BaseModel):
    id: int
    nome: str
    preco: float

# Lista em memória
produtos = [
    {"id": 1, "nome": "Teclado", "preco": 100},
    {"id": 2, "nome": "Mouse", "preco": 50}
]
# endpoint
@app.get("/produtos")
def listar_produtos():
    return produtos

@app.get("/produtos/{id}")
def buscar_produto(id: int):
    for p in produtos:
        if p["id"] == id:
            return p
    return {"erro": "Produto não encontrado"}

@app.post("/produtos")
def adicionar_produto(produto: Produto):
    produtos.append(produto.dict())
    return produto

@app.put("/produtos/{id}")
def atualizar_produto(id: int, produto: Produto):
    for i, p in enumerate(produtos):
        if p["id"] == id:
            produtos[i] = produto.dict()
            return {"mensagem": f"Produto {id} atualizado com sucesso", "produto": produto}
    return {"erro": "Produto não encontrado"}

@app.delete("/produtos/{id}")
def excluir_produto(id: int):
    for p in produtos:
        if p["id"] == id:
            produtos.remove(p)
            return {"mensagem": f"Produto {id} excluído com sucesso"}
    return {"erro": "Produto não encontrado"}

# API com FastAPI (mais moderna e rápida 🚀)
# Roda API  uvicorn app:app --reload
# http://127.0.0.1:8000/docs (Swagger UI)
# http://127.0.0.1:8000/redoc (Redoc)
