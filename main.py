from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# Classe para validar o endereço do cliente
class Endereco(BaseModel):
    endereco_cliente: str

# Função para calcular a distância usando a Google Maps API
def calcular_distancia(endereco_cliente):
    google_maps_api_key = 'AIzaSyDozfZEpygThvFnSZ-VFMat0E6BzGufK7M'  # Substitua com sua chave de API do Google Maps
    endereco_lanchonete = "Rua Roberto Crispim dos Santos, 295, Jardim Marilu - Itapecerica da Serra - São Paulo"  # Substitua com o endereço da sua lanchonete

    # Monta a URL da API do Google Maps
    url = f'https://maps.googleapis.com/maps/api/distancematrix/json?origins={endereco_lanchonete}&destinations={endereco_cliente}&key={google_maps_api_key}'

    # Faz a requisição à API do Google
    response = requests.get(url)
    data = response.json()

    if data["status"] == "OK":
        distancia_km = data["rows"][0]["elements"][0]["distance"]["text"]
        return distancia_km
    else:
        return "Erro ao calcular a distância."

# Endpoint da API
@app.post("/calcular_frete")
async def calcular_frete(endereco: Endereco):
    distancia = calcular_distancia(endereco.endereco_cliente)
    return {"distancia": distancia}
