from aiohttp import web
import socketio
import schedule

light_status = "ON"


sio = socketio.AsyncServer()
app = web.Application()
sio.attach(app)


async def index(request):
    return web.Response(text="Hello World", content_type="text/html")


async def control(request):
    return web.FileResponse("./external.html")


async def turningLight():
    global light_status
    if light_status == "ON":
        light_status = "OFF"
    else:
        light_status = "ON"
    await sio.emit('control signal', {"signal": light_status, "namespace": "/nuc"})


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

schedule.every(10).seconds.do(turningLight)

sio.wait()
