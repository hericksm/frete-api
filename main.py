from fastapi import FastAPI, Request
from pydantic import BaseModel
import requests
import os

app = FastAPI()

GOOGLE_MAPS_API_KEY = os.getenv("AIzaSyDozfZEpygThvFnSZ-VFMat0E6BzGufK7M")
ENDERECO_ORIGEM = "Rua Roberto Crispim dos Santos, 295, Jardim Marilu, Itapecerica da Serra, SP"  # Ex: "Rua Exemplo, 123, Centro, SuaCidade, SP"

# Tabela de frete por raio
TABELA_FRETE = {
    4.0: 5.99,
    4.5: 6.99,
    5.0: 7.99,
    5.5: 8.99,
    6.0: 9.99,
    6.5: 10.99,
    7.0: 11.99,
    7.5: 12.99,
    8.0: 13.99,
    9.0: 14.99,
    10.0: 15.99,
    11.0: 17.99,
    11.5: 18.99,
    12.5: 20.99,
    15.0: 22.99,
}

class FreteRequest(BaseModel):
    endereco_cliente: str

@app.post("/calcular_frete")
def calcular_frete(request: FreteRequest):
    destino = request.endereco_cliente

    # Chamada à API do Google Maps
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={ENDERECO_ORIGEM}&destinations={destino}&key={GOOGLE_MAPS_API_KEY}"
    response = requests.get(url)
    data = response.json()

    try:
        distancia_metros = data["rows"][0]["elements"][0]["distance"]["value"]
        distancia_km = round(distancia_metros / 1000, 2)

        if distancia_km <= 3.5:
            frete = 0.0
        else:
            frete = None
            for raio, valor in sorted(TABELA_FRETE.items()):
                if distancia_km <= raio:
                    frete = valor
                    break

            if frete is None:
                return {"erro": "Distância fora da área de entrega."}

        return {
            "distancia_km": distancia_km,
            "frete": frete
        }

    except Exception as e:
        return {"erro": f"Erro ao calcular frete: {str(e)}"}
