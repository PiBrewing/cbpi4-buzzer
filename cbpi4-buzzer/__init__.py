
# -*- coding: utf-8 -*-
import os
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from cbpi.api.config import ConfigType
from cbpi.api.base import CBPiBase

try:
    import RPi.GPIO as GPIO
except Exception:
    logger.error("Failed to load RPi.GPIO. Using Mock")
    MockRPi = MagicMock()
    modules = {
        "RPi": MockRPi,
        "RPi.GPIO": MockRPi.GPIO
    }
    patcher = patch.dict("sys.modules", modules)
    patcher.start()
    import RPi.GPIO as GPIO


logger = logging.getLogger(__name__)

buzzer_gpio = None
buzzer_level = None
buzzer = None

class Buzzer(CBPiExtension):

    def __init__(self,cbpi):
        self.cbpi = cbpi
        self._task = asyncio.create_task(self.run())


    async def run(self):
        self.sound = {'standard':["H", 0.1, "L", 0.1, "H", 0.1, "L", 0.1, "H", 0.1, "L"],
                      'warning':["H", 0.2, "L", 0.1, "H", 0.1, "L", 0.1, "H", 0.1, "L"],
                      'error':["H", 0.3, "L", 0.1, "H", 0.1, "L", 0.1, "H", 0.1, "L"]}
        logger.info('Starting Buzzer background task')
        await self.buzzer_gpio()
        await self.buzzer_level()
        if buzzer_gpio is None or buzzer_gpio == "" or not buzzer_gpio:
            logger.warning('Check buzzer GPIO is set')
        if buzzer_level is None or buzzer_level == "" or not buzzer_level:
            logger.warning('Check buzzer level is set') 
        else:
            self.listener_ID = self.cbpi.notification.add_listener(self.buzzerEvent)
            logger.info("Buzzer Lisetener ID: {}".format(self.listener_ID))
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(buzzer_gpio, GPIO.OUT)
            logging.info("Buzzer started")
            await self.start_buzz()
        pass

    async def buzzer_gpio(self):
        global buzzer_gpio
        buzzer_gpio = self.cbpi.config.get("buzzer_gpio", None)
        if buzzer_gpio is None:
            logger.info("INIT Buzzer GPIO")
            try:
                await self.cbpi.config.add("buzzer_gpio", 5, ConfigType.SELECT, "Buzzer GPIO", [{"label": "0", "value": 0},
                                                                                                {"label": "1", "value": 1},
                                                                                                {"label": "2", "value": 2},
                                                                                                {"label": "3", "value": 3},
                                                                                                {"label": "4", "value": 4},
                                                                                                {"label": "5", "value": 5},
                                                                                                {"label": "6", "value": 6},
                                                                                                {"label": "7", "value": 7},
                                                                                                {"label": "8", "value": 8},
                                                                                                {"label": "9", "value": 9},
                                                                                                {"label": "10", "value": 10},
                                                                                                {"label": "11", "value": 11},
                                                                                                {"label": "12", "value": 12},
                                                                                                {"label": "13", "value": 13},
                                                                                                {"label": "14", "value": 14},
                                                                                                {"label": "15", "value": 15},
                                                                                                {"label": "16", "value": 16},
                                                                                                {"label": "17", "value": 17},
                                                                                                {"label": "18", "value": 18},
                                                                                                {"label": "19", "value": 19},
                                                                                                {"label": "20", "value": 20},
                                                                                                {"label": "21", "value": 21},
                                                                                                {"label": "22", "value": 22},
                                                                                                {"label": "23", "value": 23},
                                                                                                {"label": "24", "value": 24},
                                                                                                {"label": "25", "value": 25},
                                                                                                {"label": "26", "value": 26},
                                                                                                {"label": "27", "value": 27}])
                buzzer_gpio = self.cbpi.config.get("buzzer_gpio", None)
            except:
                logger.warning('Unable to update config')
                
    async def buzzer_level(self):
        global buzzer_level
        buzzer_level = self.cbpi.config.get("buzzer_level", None)
        if buzzer_level is None:
            logger.info("INIT Buzzer Beep Level")
            try:
                await self.cbpi.config.add("buzzer_level", "HIGH", ConfigType.SELECT, "Buzzer Beep Level", [{"label": "HIGH","value": "HIGH"},
                                                                                                            {"label": "LOW", "value": "LOW"}])
                buzzer_level = self.cbpi.config.get("buzzer_level", None)
            except:
                logger.warning('Unable to update database')

    async def buzzerEvent(self, cbpi, title, message, type, action):
        if str(type) == "info" or str(type) == "success":
            type = "standard"
        else:
            type = str(type)

        try:
            for i in self.sound[type]:
                if (isinstance(i, str)):
                    if i == "H" and buzzer_level == "HIGH":
                        GPIO.output(int(buzzer_gpio), GPIO.HIGH)
                    elif i == "H" and buzzer_level != "HIGH":
                        GPIO.output(int(buzzer_gpio), GPIO.LOW)
                    elif i == "L" and buzzer_level == "HIGH":
                        GPIO.output(int(buzzer_gpio), GPIO.LOW)
                    else:
                        GPIO.output(int(buzzer_gpio), GPIO.HIGH)
                else:
                    await asyncio.sleep(i)
        except Exception as e:
            pass

    async def start_buzz(self):
        try:
            for i in self.sound['standard']:
                if (isinstance(i, str)):
                    if i == "H" and buzzer_level == "HIGH":
                        GPIO.output(int(buzzer_gpio), GPIO.HIGH)
                    elif i == "H" and buzzer_level != "HIGH":
                        GPIO.output(int(buzzer_gpio), GPIO.LOW)
                    elif i == "L" and buzzer_level == "HIGH":
                        GPIO.output(int(buzzer_gpio), GPIO.LOW)
                    else:
                        GPIO.output(int(buzzer_gpio), GPIO.HIGH)
                else:
                    await asyncio.sleep(i)
        except Exception as e:
            pass


def setup(cbpi):
    cbpi.plugin.register("Buzzer", Buzzer)
    pass
