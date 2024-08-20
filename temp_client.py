import asyncio
import websockets
from smbus3 import SMBus
import time

uri = "ws://localhost:8765"

# Get I2C bus
bus = SMBus(1)

# SHT31 address, 0x44(68)
# Send measurement command, 0x2C(44)
#		0x06(06)	High repeatability measurement


async def communicate():
    async with websockets.connect(uri) as websocket:
        while True:
            bus.write_i2c_block_data(0x44, 0x2C, [0x06])
            data = bus.read_i2c_block_data(0x44, 0x00, 6)

            # Convert the data
            temp = data[0] * 256 + data[1]
            cTemp = -45 + (175 * temp / 65535.0)

            await websocket.send(str(cTemp))

            response = await websocket.recv()
            print(f"Recieve Response from server : {response}")
            time.sleep(5)


if __name__== "__main__":
        asyncio.run(communicate())