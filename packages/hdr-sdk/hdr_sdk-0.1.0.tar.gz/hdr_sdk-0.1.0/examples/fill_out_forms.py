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
        "First go to https://hdr.is to understand the what the company does. Then navigate to https://plasticlabs.typeform.com/xenograntapp and fill out the form using the email address agent@hdr.is"
    )
    await computer.close()


asyncio.run(main())
