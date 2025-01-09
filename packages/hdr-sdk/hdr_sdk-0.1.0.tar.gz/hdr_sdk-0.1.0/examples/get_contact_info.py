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
    await computer.do("Go to Quiib.com and find the contact information")
    await computer.close()


asyncio.run(main())
