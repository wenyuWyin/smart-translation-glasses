from flask_socketio import emit
from flask import request
from app import socketio

# Dictionary to map user_id to WebSocket session ID
user_sessions = {}


@socketio.on("connect")
def handle_websocket_connect():
    print(f"WebSocket client connected: {request.sid}")


@socketio.on("register_user")
def register_user(data):
    """
    Register a user ID with the current WebSocket session ID.
    """
    user_id = data.get("user_id")
    if user_id:
        user_sessions[user_id] = request.sid
        print(f"User {user_id} registered with session ID {request.sid}")
        emit("registration_success", {"message": "User registered successfully"})
    else:
        emit("registration_error", {"error": "User ID is required"})


@socketio.on("disconnect")
def handle_websocket_disconnect():
    """
    Remove the user ID associated with this session ID
    """
    disconnected_user = None
    for user_id, sid in user_sessions.items():
        if sid == request.sid:
            disconnected_user = user_id
            break

    if disconnected_user:
        del user_sessions[disconnected_user]
        print(f"User {disconnected_user} disconnected (session ID: {request.sid})")


def notify_disconnection(user_id):
    """
    Notify the correct front-end app (based on user_id) about a device disconnection.
    """
    target_sid = user_sessions.get(user_id)
    if target_sid:
        print(
            f"Sending disconnection message to user {user_id} (session ID: {target_sid})"
        )
        socketio.emit("esp32_disconnect", {"status": "disconnected"}, to=target_sid)
    else:
        print(f"User {user_id} is not connected")


def send_status_update(user_id, battery, temperature, connection_status):
    """
    Notify the correct front-end app (based on user_id) about a device status update.
    """
    target_sid = user_sessions.get(user_id)
    if target_sid:
        data = {
            "event": "status_update",
            "battery": battery,
            "temperature": temperature,
            "wifiStatus": connection_status,
        }
        print(f"Sending status update to user {user_id}: {data}")
        socketio.emit("status_update", data, to=target_sid)
    else:
        print(f"User {user_id} is not registered")
