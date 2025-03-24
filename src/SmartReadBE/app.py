from app import create_app, socketio
import signal

app = create_app()

# Shutdown the executor when the app stops
def shutdown_executor(exception=None):
    if hasattr(app, "executor"):
        print("Shutting down task executor")
        app.executor.shutdown(wait=True)

signal.signal(signal.SIGTERM, shutdown_executor) 

if __name__ == "__main__":
    socketio.run(app, debug=True, host="0.0.0.0", port=5000)
