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
    await computer.do(
        "First go to https://hdr.is to get a feel for the aesthetics of the website. Then create a python web server that serves a simple html page with the text 'Hello World' in that style."
    )
    await computer.close()


asyncio.run(main())
