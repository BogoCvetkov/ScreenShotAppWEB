import os

from Project.app.auth.security import hash_value
from Project.errors.custom_errors import AppServiceError
from flask import request, jsonify
from flask_sse import sse


# Route accepting post requests for publishing ServerSentEvents
# Used by the workers to notify the app, which sends the SSE to the frontend

# /stream/event/?key=authentication_key
def publish_event():
    # Check for key
    key = request.args.get("key", None)
    if not key: raise AppServiceError("Missing key", 401)

    # Check if the key comes from the workers - the only eligible entity to use this endpoint
    key = hash_value(key)
    worker_key = hash_value(os.environ["WORKER_SECRET"])

    if key != worker_key: raise AppServiceError("Invalid key", 401)

    # Get the data
    data = request.json

    # Send SSE to the client
    sse.publish({ "message": data }, type="workers")

    return jsonify(data=data)