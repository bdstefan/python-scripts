import redis
import os

print("Hello {}!".format(os.environ.get("USER")))

host = raw_input("Redis host (127.0.0.1): ") or "127.0.0.1"
port = raw_input("Redis port (6379): ") or "6379"

try:
    r = redis.StrictRedis(host=host, port=port, db=0)
    print("Connected to {}".format(r.connection_pool.pid))
except Exception as e:
    print("Couldn't connect Redis server. Error: ".format(e.message))
    exit(1)

# Delete all keys without a TTL to expire and not accessed in the last 6 months
deleted_keys = 0
for key in r.scan_iter("*"):
     idle = r.object("idletime", key)

     if r.ttl(key) == -1 and idle > 3600 * 24 * 30 * 6:
        print("Removed {}".format(key))
        r.delete(key)
        deleted_keys += 1

if deleted_keys:
    print("Deleted {} keys.".format(deleted_keys))
else:
    print("There are no key that have to be deleted")
