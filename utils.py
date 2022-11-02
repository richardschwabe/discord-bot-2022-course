import settings

logger = settings.logging.getLogger(__name__)

async def load_videocmds(bot):
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")
    for extension_file in settings.VIDEOCMDS_DIR.glob("*.py"):
        if extension_file.name != "__init__.py" and not extension_file.name.startswith("_"):
            await bot.load_extension(f"{settings.VIDEOCMDS_DIR.name}.{extension_file.name[:-3]}")
            logger.debug(f"Loadded CMD: {extension_file.name}")