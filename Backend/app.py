from flask import Flask, jsonify, request
from flask_cors import CORS

from services import inicializar_datos, obtener_episodios, reservar_capitulo, confirmar_alquiler

app = Flask(__name__)

CORS(app)


with app.app_context():
    inicializar_datos()

# --- RUTAS DE LA API ---

@app.route('/api/episodios', methods=['GET'])
def listar():
    """Devuelve la lista de episodios con sus estados (Disponible/Reservado/Alquilado)."""

    lista = obtener_episodios()
    return jsonify(lista)

@app.route('/api/reservar/<int:id>', methods=['POST'])
def reservar(id):
    """Intenta reservar un episodio por 4 minutos."""
    exito, mensaje = reservar_capitulo(id)
    # Si éxito es True -> 200 OK. Si es False -> 409 Conflict (ya está ocupado)
    codigo_http = 200 if exito else 409
    return jsonify({"exito": exito, "mensaje": mensaje}), codigo_http

@app.route('/api/pagar/<int:id>', methods=['POST'])
def pagar(id):
    """Confirma el pago y extiende el alquiler por 24 horas."""
    body = request.get_json()
    monto = body.get('monto', 0) if body else 0
    

    exito, mensaje = confirmar_alquiler(id, monto)
    
    codigo_http = 200 if exito else 400
    return jsonify({"exito": exito, "mensaje": mensaje}), codigo_http

# --- ARRANQUE ---
if __name__ == '__main__':
 
    app.run(host='0.0.0.0', port=5000, debug=True)
