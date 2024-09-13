import os
import redis
from dotenv import load_dotenv

# Custom path can be given to experiment locally with different env vars.
load_dotenv()

class KV:
    def __init__(self, url: str = None):
        self.url = os.getenv("KV_URL", "redis://localhost:6379")
        if url:
            self.url = url
        
        self.redis_client = redis.from_url(url=self.url)

    def set(self, key, value) -> bool:
        result = self.redis_client.set(key, value)
        return result

    def get(self, key) -> bool:
        result = self.redis_client.get(key)
        return result.decode()
