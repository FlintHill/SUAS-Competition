#!/usr/bin/env python

import asyncio, random, websockets

connected = set()

async def time(websocket, path):
	global connected

	connected.add(websocket)
	await asyncio.wait([ws.send('{"status": "connected"}') for ws in connected])
	
	while True:
		# BEGIN CHANGES HERE
		data = '{"alt": ' + str(22 * random.random()) + ', "dir": ' + str(44 * random.random()) + ', "speed": ' + str(33 * random.random()) + ', "vert_speed": ' + str(55 * random.random()) + ', "lat": ' + str(38.8712152 + random.random()) + ', "long": ' + str(-77.319965 + random.random()) + "}"
		
		# END CHANGES HERE
		await websocket.send(data)
		await asyncio.sleep(random.random())

start_server = websockets.serve(time, "127.0.0.1", 5678)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()