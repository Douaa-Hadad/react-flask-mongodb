import os
import time
from pymongo import MongoClient

uri = os.getenv("MONGO_URI", "mongodb://mongo:27017/mongotask")
wait_timeout = int(os.getenv("MONGO_WAIT_TIMEOUT", "60"))
interval = 1
start = time.time()
print(f"Waiting for Mongo at {uri} (timeout {wait_timeout}s)")
while True:
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        print("Mongo is available")
        break
    except Exception as e:
        elapsed = time.time() - start
        if elapsed > wait_timeout:
            print(f"Timed out waiting for Mongo after {elapsed:.1f}s: {e}")
            raise
        print("Mongo not ready yet, retrying...", str(e))
        time.sleep(interval)
