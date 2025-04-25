from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

ENDERECO_LANCHONETE = "Rua Roberto Crispim dos Santos, 295, Jardim Marilu - Itapecerica da Serra - São Paulo"
GOOGLE_MAPS_API_KEY = "AIzaSyDozfZEpygThvFnSZ-VFMat0E6BzGufK7M"
VALOR_POR_KM = 2.0

class FreteRequest(BaseModel):
    endereco_cliente: str

@app.post("/calcular_frete")
def calcular_frete(data: FreteRequest):
    endereco_cliente = data.endereco_cliente

    url = (
        f"https://maps.googleapis.com/maps/api/distancematrix/json"
        f"?origins={ENDERECO_LANCHONETE}&destinations={endereco_cliente}"
        f"&key={GOOGLE_MAPS_API_KEY}&language=pt-BR&units=metric"
    )

    response = requests.get(url)
    data = response.json()

    try:
        distancia_metros = data['rows'][0]['elements'][0]['distance']['value']
        distancia_km = distancia_metros / 1000
        frete = round(distancia_km * VALOR_POR_KM, 2)

        return {
            "distancia_km": round(distancia_km, 2),
            "frete": frete,
            "mensagem": f"A distância até o cliente é de {round(distancia_km, 2)} km. O valor do frete é R$ {frete:.2f}."
        }

    except Exception as e:
        return {
            "erro": "Erro ao calcular o frete.",
            "detalhes": str(e)
        }