import asyncio
import websockets
import json
import math
import time

# The "Hive" - Broadcasts BCI data to all connected screens
async def hive_brain(websocket, path):
    print("🐝 Drone connected to the Hive!")
    x, y = 50.0, 50.0
    direction = 1
    
    try:
        while True:
            # GHOST WANDER (Simulates your mouse pad swipes / X:Y coords)
            # Replace this with actual mouse/serial data if you have it!
            x += math.sin(time.time() * 0.5) * 0.8
            y += math.cos(time.time() * 0.7) * 0.8
            
            # Clamp the values to keep it in the "Matrix" bounds
            x = max(0, min(100, x))
            y = max(0, min(100, y))
            
            # Translate X/Y into the COMMANDS your interface recognizes
            # CUTOFF (Filter Freq): Maps X (0-100) to 200Hz - 5000Hz
            cutoff = int(200 + (x * 48))
            # TREMOR (Wobble Hz): Maps Y (0-100) to 1Hz - 15Hz
            tremor = round(1 + (y / 7.5), 2)
            # PITCH (Speed): Maps a combination to 0.5x - 1.8x speed
            pitch = round(0.5 + ((x + y) / 200), 2)
            
            # The payload sent to the video page
            payload = {
                "cutoff": cutoff,
                "tremor": tremor,
                "pitch": pitch,
                "x": round(x, 2),
                "y": round(y, 2)
            }
            
            await websocket.send(json.dumps(payload))
            await asyncio.sleep(0.05)  # 20 updates per second = SMOOTH BUZZING
            
    except:
        print("🐝 Drone disconnected.")

# Start the Hive Server (listens on ALL interfaces, Port 8081)
start_server = websockets.serve(hive_brain, "0.0.0.0", 8081)
print("🐝🔥 HIVE IS ONLINE! Connect your browser to the Queen Bee.")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
