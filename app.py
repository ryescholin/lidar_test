
# app.py
import socketio
import argparse
import numpy as np
import cv2

from TauLidarCommon.frame import FrameType
from TauLidarCamera.camera import Camera
sio = socketio.AsyncServer(
    async_mode="asgi", cors_allowed_origins="http://localhost:3000"
)

app = socketio.ASGIApp(sio)
camera = None 
@sio.event
async def connect(sid, environ):
    print(sid, 'connected')
    global sid_save 
    sid_save = sid
    Camera.setRange(0, 4500)                   ## points in the distance range to be colored
    camera = Camera.open("COM4")             ## Open the first available Tau Camera
    camera.setModulationChannel(0)             ## autoChannelEnabled: 0, channel: 0
    camera.setIntegrationTime3d(0, 1000)       ## set integration time 0: 1000
    camera.setMinimalAmplitude(0, 10)          ## set minimal amplitude 0: 80
    # while True:
    #         frame = camera.readFrame(FrameType.DISTANCE)

    #         if frame:
    #             mat_depth_rgb = np.frombuffer(frame.data_depth_rgb, dtype=np.uint16, count=-1, offset=0).reshape(frame.height, frame.width, 3)
    #             mat_depth_rgb = mat_depth_rgb.astype(np.uint8)

    #             # Upscalling the image
    #             upscale = 4
    #             img =  cv2.resize(mat_depth_rgb, (frame.width*upscale, frame.height*upscale))
    #             await sio.emit( 'img', img )
    #             #cv2.imshow('Depth Map', img)

    #             if cv2.waitKey(1) == 27: break

@sio.event
async def disconnect(sid):
    print(sid, 'disconnected')
    cv2.destroyAllWindows()
    camera.close()

@sio.event
async def sum(sid, data):
    result = data['numbers'][0] + data['numbers'][1]
    await sio.emit('sum_result', {'result': result}, to=sid)