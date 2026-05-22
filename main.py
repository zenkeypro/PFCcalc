import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

app = FastAPI()

class DatosProgresion(BaseModel):
    capital_inicial: float
    porcentaje_profit: float
    total_trades: int

@app.get("/")
def leer_interfaz():
    ruta_html = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    return FileResponse(ruta_html)

def calcular_progresion(capital_inicial, porcentaje_profit, total_trades):
    balance_actual = capital_inicial
    historial = [] 
    for i in range(total_trades):
        balance_inicial_trade = balance_actual
        profit_plata = balance_inicial_trade * (porcentaje_profit / 100)
        balance_final_trade = balance_inicial_trade + profit_plata
        balance_actual = balance_final_trade
        historial.append({
            "trade": i + 1,
            "balance_inicial": round(balance_inicial_trade, 2),
            "profit": round(profit_plata, 2),
            "balance_final": round(balance_final_trade, 2)
        })
    return historial

@app.post("/calcular")
def procesar_calculo(datos: DatosProgresion):
    resultado = calcular_progresion(
        capital_inicial=datos.capital_inicial,
        porcentaje_profit=datos.porcentaje_profit,
        total_trades=datos.total_trades
    )
    return {"status": "success", "data": resultado}