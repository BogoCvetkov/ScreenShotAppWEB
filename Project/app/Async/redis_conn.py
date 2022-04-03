from redis import Redis

# Used by rq
redis_conn = Redis(host="localhost")

# Decrypted version that returns strings instead of bytes. Used when fetching keys from Redis
redis_conn_d = Redis(host="localhost",charset="utf-8", decode_responses=True)