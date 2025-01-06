import socket
import threading
from collections import defaultdict

clients = {}
events = {}
rooms = defaultdict(set)
pubsub = defaultdict(list)
server = None

def init_server(host='127.0.0.1', port=5000):
    """Initialize the socket server."""
    global server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server started on {host}:{port}")

    
    threading.Thread(target=_accept_clients, daemon=True).start()

def on(event_name, handler):
    """Register an event handler."""
    events[event_name] = handler

def emit(event_name, data, client=None, room=None):
    """Emit an event to a specific client, room, or all clients."""
    if client:
        _send_to_client(client, event_name, data)
    elif room:
        for client in rooms[room]:
            _send_to_client(client, event_name, data)
    else:
        for client in clients:
            _send_to_client(client, event_name, data)

def subscribe(channel, client):
    """Subscribe a client to a Pub/Sub channel."""
    pubsub[channel].append(client)

def publish(channel, message):
    """Publish a message to all clients subscribed to a channel."""
    for client in pubsub[channel]:
        _send_to_client(client, "message", {"channel": channel, "data": message})

def join_room(room, client):
    """Add a client to a room."""
    rooms[room].add(client)

def leave_room(room, client):
    """Remove a client from a room."""
    rooms[room].discard(client)


def _accept_clients():
    """Accept incoming client connections."""
    while True:
        client, addr = server.accept()
        print(f"New connection: {addr}")
        clients[client] = addr
        threading.Thread(target=_handle_client, args=(client,), daemon=True).start()

def _handle_client(client):
    """Handle communication with a single client."""
    try:
        while True:
            data = client.recv(1024).decode('utf-8')
            if data:
                event_data = _parse_message(data)
                event_name = event_data.get("event")
                if event_name in events:
                    events[event_name](client, event_data)
            else:
                break
    except ConnectionResetError:
        pass
    finally:
        _disconnect_client(client)

def _send_to_client(client, event_name, data):
    """Send a message to a client."""
    message = _format_message(event_name, data)
    try:
        client.sendall(message.encode('utf-8'))
    except BrokenPipeError:
        _disconnect_client(client)

def _disconnect_client(client):
    """Handle client disconnection."""
    if client in clients:
        addr = clients[client]
        print(f"Client disconnected: {addr}")
        del clients[client]
        
        for room in rooms.values():
            room.discard(client)
        
        for channel in pubsub.values():
            if client in channel:
                channel.remove(client)
        client.close()

def _format_message(event_name, data):
    """Format the message to be sent."""
    return f"{event_name}:{data}"

def _parse_message(data):
    """Parse the incoming message."""
    try:
        event, payload = data.split(":", 1)
        return {"event": event, "data": payload}
    except ValueError:
        return {}
