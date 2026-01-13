import redis
import os

def get_redis_connection():
    try:
        # Obtenemos el host y puerto desde las variables de entorno (definidas en docker-compose)
        # Si no las encuentra, usa 'localhost' por defecto (para pruebas locales)
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        redis_port = int(os.environ.get("REDIS_PORT", 6379))
        
        # Creamos la conexión (decode_responses=True nos devuelve Strings en vez de Bytes)
        client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        
        # Probamos conexión rápida
        client.ping()
        print(f"✅ Conectado a Redis en {redis_host}:{redis_port}")
        return client
        
    except redis.ConnectionError as e:
        print(f"❌ Error conectando a Redis: {e}")
        return None