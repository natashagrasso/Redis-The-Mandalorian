import redis
import os

def get_redis_connection():
    try:
   
      
        redis_host = os.environ.get("REDIS_HOST", "localhost")
        redis_port = int(os.environ.get("REDIS_PORT", 6379))
        
        
        client = redis.Redis(host=redis_host, port=redis_port, db=0, decode_responses=True)
        
      
        client.ping()
        print(f"✅ Conectado a Redis en {redis_host}:{redis_port}")
        return client
        
    except redis.ConnectionError as e:
        print(f"❌ Error conectando a Redis: {e}")
        return None
