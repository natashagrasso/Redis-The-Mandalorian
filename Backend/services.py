import json
from config import get_redis_connection

db = get_redis_connection()


KEY_EPISODIOS = "mandalorian:episodios"
PREFIX_RESERVA = "reserva:"
PREFIX_ALQUILER = "alquiler:"

# Datos fijos de los capítulos
DATA_EPISODIOS = [
    {"id": 1, "titulo": "Chapter 1: The Mandalorian", "precio": 100},
    {"id": 2, "titulo": "Chapter 2: The Child", "precio": 100},
    {"id": 3, "titulo": "Chapter 3: The Sin", "precio": 150},
    {"id": 4, "titulo": "Chapter 4: Sanctuary", "precio": 120},
    {"id": 5, "titulo": "Chapter 5: The Gunslinger", "precio": 110},
    {"id": 6, "titulo": "Chapter 6: The Prisoner", "precio": 130},
    {"id": 7, "titulo": "Chapter 7: The Reckoning", "precio": 140},
    {"id": 8, "titulo": "Chapter 8: Redemption", "precio": 150},
]

def inicializar_datos():
    if db and not db.exists(KEY_EPISODIOS):
        db.set(KEY_EPISODIOS, json.dumps(DATA_EPISODIOS))
        print("💾 Datos de episodios cargados en Redis")

def obtener_episodios():
    if not db.exists(KEY_EPISODIOS):
        inicializar_datos()
        
    raw_data = db.get(KEY_EPISODIOS)
    episodios = json.loads(raw_data) if raw_data else []
    
    resultado = []
    for epi in episodios:
        epi_id = epi['id']
        estado = "Disponible"
        
 
        # Si la clave reservaID existesignifica que el tiempo no ha expirado aún
        if db.exists(f"{PREFIX_ALQUILER}{epi_id}"):
            estado = "Alquilado"
        elif db.exists(f"{PREFIX_RESERVA}{epi_id}"):
            estado = "Reservado"
            
        epi['estado'] = estado
        resultado.append(epi)
        
    return resultado

def reservar_capitulo(id_capitulo):
    key_reserva = f"{PREFIX_RESERVA}{id_capitulo}"
    key_alquiler = f"{PREFIX_ALQUILER}{id_capitulo}"

    # No se puede reservar si ya está ocupado
    if db.exists(key_reserva) or db.exists(key_alquiler):
        return False, "El capítulo no está disponible."

    #  4 MINUTOS ---
    # Usamos el comando SETEX (SET con EXpiración)
    # Param 1: La clave (ej: "reserva:1")
    # Param 2: Tiempo en segundos (240 seg = 4 minutos)
    # Param 3: Valor ("ocupado")
    
    db.setex(key_reserva, 240, "ocupado") 
    
    return True, "Reservado por 4 minutos."

def confirmar_alquiler(id_capitulo, pago_cliente):
    key_reserva = f"{PREFIX_RESERVA}{id_capitulo}"
    key_alquiler = f"{PREFIX_ALQUILER}{id_capitulo}"
    
    # Validar que exista una reserva previa
    if not db.exists(key_reserva):
        return False, "La reserva ha expirado o no existe."
    
    #  Validar el pago 

    raw_data = db.get(KEY_EPISODIOS)
    episodios = json.loads(raw_data) if raw_data else []
    episodio_obj = next((e for e in episodios if e['id'] == id_capitulo), None)
    
    if episodio_obj:
        precio_real = episodio_obj.get('precio', 0)

        if float(pago_cliente) < float(precio_real):
            return False, f"Pago insuficiente. El precio es ${precio_real}."

    #  Confirmar alquiler por 24 hs

    db.delete(key_reserva)
    
    # Creamos el alquiler definitivo por 24 horas (86400 segundos)
    # Nuevamente usamos la magia de Redis para que expire al día siguiente
    db.setex(key_alquiler, 86400, "pagado")
    
    return True, "¡Pago exitoso! Tienes 24 horas para ver el episodio."
