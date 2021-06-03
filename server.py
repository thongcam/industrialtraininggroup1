from aiohttp import web
import socketio

light_status = "ON"


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def index(request):
    return web.Response(text="Hello World", content_type="text/html")


async def control(request):
    return web.FileResponse("./external.html")


@sio.on("change light status", namespace="/external")
async def change_light_status(sid, msg):
    print(f"{sid}: {msg}")
    if msg in ["ON", "OFF"]:
        light_status = msg
        await sio.emit('control signal', {"signal": msg, "namespace": "/nuc"})


app.router.add_get('/', index)
app.router.add_get('/control', control)

if __name__ == "__main__":
    web.run_app(app)

sio.wait()
