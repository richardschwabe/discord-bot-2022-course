
import settings
import discord
from discord.ext import commands
from discord import app_commands

logger = settings.logging.getLogger("bot")

games_list = {
    "unrailed": {
        "title": "Unrailed",
        "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/1016920/header.jpg?t=1667079473"
    },
    "valorant": {
        "title": "Valorant",
        "url": None
    },
    "csgo": {
        "title": "Counter-Strike: Global Offensive",
        "url": "https://cdn.cloudflare.steamstatic.com/steam/apps/730/header.jpg?t=1668125812"
    },
    "other": {
        "title": "a game",
        "url": None
    }
}

class ReadyOrNotView(discord.ui.View):

    joined_users = []
    declined_users = []
    tentative_users = []

    initiatior: discord.User = None
    players: int = 0
    message : discord.abc.Messageable = None


    async def on_timeout(self):
        """This is added outside the video,
        it handles any timeouts and disables the buttons
        make sure to change the timeout in
        view = ReadyOrNotView(timeout=180)
        """
        self.disable_all_buttons()
        await self.update_message()


    async def send(self, interaction: discord.Interaction):
        # This is necessary to make sure, that the lists are empty when the next
        # /play usage is run!
        self.joined_users = list()
        self.declined_users = list()
        self.tentative_users = list()

        self.joined_users.append(interaction.user.display_name)
        embed = self.create_embed()
        await interaction.response.send_message(view=self, embed=embed)
        self.message = await interaction.original_response()


    def convert_user_list_to_str(self, user_list, default_str="No one"):
        if len(user_list):
            return "\n".join(user_list)
        return default_str

    def create_embed(self):
        desc = f"{self.initiatior.display_name} is looking for another {self.players - 1} players to play {self.game['title']}"
        embed = discord.Embed(title="Lets get together", description=desc)

        if self.game['url']:
            embed.set_image(url=self.game['url'])

        embed.add_field(inline=True, name="✅Joined", value=self.convert_user_list_to_str(self.joined_users))
        embed.add_field(inline=True, name="❌Declined", value=self.convert_user_list_to_str(self.declined_users))
        embed.add_field(inline=True, name="🔄Tentative", value=self.convert_user_list_to_str(self.tentative_users))

        return embed

    def check_players_full(self):
        if len(self.joined_users) >= self.players:
            return True
        return False


    def disable_all_buttons(self):
        self.join_button.disabled = True
        self.decline_button.disabled = True
        self.tentative_button.disabled = True

    async def update_message(self):
        if self.check_players_full():
            self.disable_all_buttons()

        embed = self.create_embed()
        await self.message.edit(view=self, embed=embed)

    @discord.ui.button(label="Join",
                       style=discord.ButtonStyle.green)
    async def join_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.message = interaction.message
        await interaction.response.defer()

        if interaction.user.display_name not in self.joined_users:
            self.joined_users.append(interaction.user.display_name)
        # remove from declined and from tentative if inside
        if interaction.user.display_name in self.tentative_users:
            self.tentative_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.declined_users:
            self.declined_users.remove(interaction.user.display_name)

        await self.update_message()


    @discord.ui.button(label="Decline",
                       style=discord.ButtonStyle.red)
    async def decline_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.message = interaction.message
        await interaction.response.defer()


        if interaction.user.display_name not in self.declined_users:
            self.declined_users.append(interaction.user.display_name)
        # remove from joined and from tentative if inside
        if interaction.user.display_name in self.tentative_users:
            self.tentative_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.joined_users:
            self.joined_users.remove(interaction.user.display_name)

        await self.update_message()

    @discord.ui.button(label="Maybe",
                       style=discord.ButtonStyle.blurple)
    async def tentative_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        self.message = interaction.message
        await interaction.response.defer()

        if interaction.user.display_name not in self.tentative_users:
            self.tentative_users.append(interaction.user.display_name)
        # remove from declined and from joined if inside
        if interaction.user.display_name in self.joined_users:
            self.joined_users.remove(interaction.user.display_name)
        if interaction.user.display_name in self.declined_users:
            self.declined_users.remove(interaction.user.display_name)

        await self.update_message()

def run():
    intents = discord.Intents.default()
    intents.message_content = True
    # intents.members = True

    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        bot.tree.copy_global_to(guild=settings.GUILDS_ID)
        await bot.tree.sync(guild=settings.GUILDS_ID)

    @bot.tree.command()
    @app_commands.choices(game=[
        app_commands.Choice(name="Unrailed", value="unrailed"),
        app_commands.Choice(name="Valorant", value="valorant"),
        app_commands.Choice(name="CS:GO", value="csgo"),
        app_commands.Choice(name="Other", value="other"),
    ])
    async def play(interaction: discord.Interaction,game : app_commands.Choice[str], players: int = 5 ):
        view = ReadyOrNotView(timeout=None)
        view.initiatior = interaction.user
        view.game = games_list[game.value]
        view.players = players
        await view.send(interaction)


    bot.run(settings.DISCORD_API_SECRET, root_logger=True)


if __name__ == "__main__":
    run()
