
# -*- coding: utf-8 -*-
import threading, time
from aiohttp import web
import logging
from unittest.mock import MagicMock, patch
import asyncio
import random
from cbpi.api import *
from cbpi.api.config import ConfigType
from cbpi.api.base import CBPiBase
import os, re

logger = logging.getLogger(__name__)

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

buzzer_gpio = None
buzzer_gpio_inverted = None
buzzer_level = None
buzzer = None

class BuzzerThread (threading.Thread):

    def __init__(self, sound,gpio, gpio_inverted, level):
        threading.Thread.__init__(self)
        self.gpio = gpio
        self.gpio_inverted = gpio_inverted
        self.sound = sound
        self.level = level
        self.runnig = True
        self.HIGH = 1 if self.gpio_inverted is False else 0
        self.LOW = 0 if self.gpio_inverted is False else 1

    def shutdown(self):
        pass

    def stop(self):
        pass

    def run(self):
        try:
            for i in self.sound:
                if (isinstance(i, str)):
                    if i == "H" and self.level == "HIGH":
                        GPIO.output(int(self.gpio), self.HIGH)
                    elif i == "H" and self.level != "HIGH":
                        GPIO.output(int(self.gpio), self.LOW)
                    elif i == "L" and self.level == "HIGH":
                        GPIO.output(int(self.gpio), self.LOW)
                    else:
                        GPIO.output(int(self.gpio), self.HIGH)
                else:
                    time.sleep(i)
        except Exception as e:
            pass
        finally:
            pass



class Buzzer(CBPiExtension):

    def __init__(self,cbpi):
        self.cbpi = cbpi
        self._task = asyncio.create_task(self.run())


    async def run(self):
        plugin = await self.cbpi.plugin.load_plugin_list("cbpi4-buzzer")
        self.version=plugin[0].get("Version","0.0.0")
        self.name=plugin[0].get("Name","cbpi4-buzzer")

        self.buzzer_update = self.cbpi.config.get(self.name+"_update", None)


        self.sound = {'standard':["H", 0.1, "L", 0.1, "H", 0.1, "L", 0.1, "H", 0.1, "L"],
                      'warning':["H", 0.2, "L", 0.1, "H", 0.1, "L", 0.1, "H", 0.2, "L"],
                      'error':["H", 0.3, "L", 0.1, "H", 0.3, "L", 0.1, "H", 0.3, "L"]}
        logger.info('Starting Buzzer background task')
        await self.buzzer_settings()
        if buzzer_gpio is None or buzzer_gpio == "" or not buzzer_gpio:
            logger.warning('Check buzzer GPIO is set')
        if buzzer_gpio_inverted is None or buzzer_gpio_inverted == "":
            logger.warning('Check buzzer GPIO Inverted is set')
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

    async def buzzer_settings(self):
        global buzzer_gpio_inverted
        global buzzer_gpio
        global buzzer_level
        buzzer_level = self.cbpi.config.get("buzzer_level", None)
        buzzer_gpio = self.cbpi.config.get("buzzer_gpio", None)
        buzzer_gpio_inverted = self.cbpi.config.get("buzzer_gpio_inverted", None)

        if buzzer_gpio_inverted is None:
            logger.info("INIT Buzzer GPIO Inverted")
            try:
                await self.cbpi.config.add("buzzer_gpio_inverted", False, type=ConfigType.SELECT, description="Buzzer GPIO Inverted ('High' on 'Low')",
                                                                                                            source=self.name,
                                                                                                            options= [{"label": "no", "value": False}, 
                                                                                                                        {"label": "yes", "value": True}])
                buzzer_gpio_inverted = self.cbpi.config.get("buzzer_gpio_inverted", False)
            except:
                logger.warning('Unable to update config')
        else:
            if self.buzzer_update == None or self.buzzer_update != self.version:
                try:

                    await self.cbpi.config.add("buzzer_gpio_inverted",buzzer_gpio_inverted, type=ConfigType.SELECT, description="Buzzer GPIO Inverted ('High' on 'Low')",
                                            source=self.name,
                                           options= [{"label": "no", "value": False}, 
                                                     {"label": "yes", "value": True}])
                except:
                    logger.warning('Unable to update config')                


        if buzzer_gpio is None:
            logger.info("INIT Buzzer GPIO")
            try:
                await self.cbpi.config.add("buzzer_gpio", 5, type=ConfigType.SELECT, description="Buzzer GPIO", 
                                                                                        source=self.name,
                                                                                        options=[{"label": "0", "value": 0},
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
        else:
            if self.buzzer_update == None or self.buzzer_update != self.version:
                try:

                    await self.cbpi.config.add("buzzer_gpio", buzzer_gpio, type=ConfigType.SELECT, description="Buzzer GPIO", 
                                                                                        source=self.name,
                                                                                        options=[{"label": "0", "value": 0},
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
                except:
                    logger.warning('Unable to update config')                 


        if buzzer_level is None:
            logger.info("INIT Buzzer Beep Level")
            try:
                await self.cbpi.config.add("buzzer_level", "HIGH", type=ConfigType.SELECT, description="Buzzer Beep Level", 
                                                                                            source=self.name,
                                                                                            options=[{"label": "HIGH","value": "HIGH"},
                                                                                                    {"label": "LOW", "value": "LOW"}])
                buzzer_level = self.cbpi.config.get("buzzer_level", None)
            except:
                logger.warning('Unable to update database')
        else:
            if self.buzzer_update == None or self.buzzer_update != self.version:
                try:

                    await self.cbpi.config.add("buzzer_level", buzzer_level, type=ConfigType.SELECT, description="Buzzer Beep Level", 
                                                                                                source=self.name,
                                                                                                options=[{"label": "HIGH","value": "HIGH"},
                                                                                                        {"label": "LOW", "value": "LOW"}])
                except:
                    logger.warning('Unable to update config')                          

        if self.buzzer_update == None or self.buzzer_update != self.version:
            try:

                await self.cbpi.config.add(self.name+"_update", self.version, type=ConfigType.STRING, description="Buzzer update status",
                                                                                                            source="hidden")
            except:
                logger.warning('Unable to update config')              

    async def buzzerEvent(self, cbpi, title, message, type, action):
        if str(type) == "info" or str(type) == "success":
            type = "standard"
        else:
            type = str(type)

        self.buzzer = BuzzerThread(self.sound[type], buzzer_gpio, buzzer_gpio_inverted, buzzer_level)
        self.buzzer.daemon = False
        self.buzzer.start()
        self.buzzer.stop()

    async def start_buzz(self):
        self.buzzer = BuzzerThread(self.sound['standard'], buzzer_gpio, buzzer_gpio_inverted, buzzer_level)
        self.buzzer.daemon = False
        self.buzzer.start()
        self.buzzer.stop()

def setup(cbpi):
    cbpi.plugin.register("Buzzer", Buzzer)
    pass
