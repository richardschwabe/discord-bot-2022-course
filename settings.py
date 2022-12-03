import pathlib
import os
import logging
from logging.config import dictConfig
from dotenv import load_dotenv
import discord

load_dotenv()

DISCORD_API_SECRET = os.getenv("DISCORD_API_TOKEN")

BASE_DIR = pathlib.Path(__file__).parent

CMDS_DIR = BASE_DIR / "cmds"
COGS_DIR = BASE_DIR / "cogs"

VIDEOCMDS_DIR = BASE_DIR / "videocmds"

GUILDS_ID = discord.Object(id=int(os.getenv("GUILD")))
FEEDBACK_CH = int(os.getenv("FEEDBACK_CH",0))

LOGGING_CONFIG = {
    "version": 1, 
    "disabled_existing_loggers": False, 
    "formatters":{
        "verbose":{
            "format": "%(levelname)-10s - %(asctime)s - %(module)-15s : %(message)s"
        },
        "standard":{
            "format": "%(levelname)-10s - %(name)-15s : %(message)s"
        }
    }, 
    "handlers":{
        "console": {
            'level': "DEBUG", 
            'class': "logging.StreamHandler",
            'formatter': "standard"
        }, 
        "console2": {
            'level': "WARNING", 
            'class': "logging.StreamHandler",
            'formatter': "standard"
        }, 
        "file": {
            'level': "INFO", 
            'class': "logging.FileHandler",
            'filename': "logs/infos.log",
            'mode': "w", 
            'formatter': "verbose"
        }, 
    }, 
    "loggers":{
        "bot": {
            'handlers': ['console'],
            "level": "INFO", 
            "propagate": False
        }, 
        "discord": {
            'handlers': ['console2', "file"],
            "level": "INFO", 
            "propagate": False
        }
    }
}

dictConfig(LOGGING_CONFIG)