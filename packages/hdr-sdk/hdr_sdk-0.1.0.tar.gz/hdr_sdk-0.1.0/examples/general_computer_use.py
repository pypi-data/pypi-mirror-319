# TODO: Add examples
import asyncio
import logging
import os

import dotenv

from hdr_sdk import Computer

logging.basicConfig(level=logging.INFO)

dotenv.load_dotenv()


async def main():
    computer = Computer({"base_url": "wss://api.hdr.is/compute/ephemeral", "api_key": os.getenv("HDR_API_KEY")})

    await computer.connect()
    await computer.do("Tell me the weather in Tokyo")

    await computer.do("Tell me the weather in Tokyo using only bash")
    await computer.close()


asyncio.run(main())
