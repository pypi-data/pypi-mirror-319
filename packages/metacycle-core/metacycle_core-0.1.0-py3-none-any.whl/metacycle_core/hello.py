from aiohttp import web
import asyncio
import socketio

sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)

heartbeat_task = None

async def heartbeat():
    """Emit a heartbeat message to all clients every second."""
    t = 0;
    while True:
        await sio.emit('heartbeat', {'timestamp': f'{t}'})
        await asyncio.sleep(1)
        t += 1;

async def index(request):
    """Serve the client-side application."""
    with open('index.html') as f:
        return web.Response(text=f.read(), content_type='text/html')

@sio.event
def connect(sid, environ):
    global heartbeat_task
    if heartbeat_task is None:
        heartbeat_task = sio.start_background_task(heartbeat)
    print("connect ", sid)

@sio.event
async def chat_message(sid, data):
    print("message ", data)

@sio.event
def disconnect(sid):
    print('disconnect ', sid)

# app.router.add_static('/static', 'static')
app.router.add_get('/', index)

def main():
    web.run_app(app)


if __name__ == '__main__':
    main()