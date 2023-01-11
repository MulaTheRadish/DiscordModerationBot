import discord
from discord.ext import commands
import os

class MyBot(commands.Bot):

    def __init__(self):
        super().__init__(command_prefix = '>', intents = discord.Intents.all())

    async def setup_hook(self):
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await bot.load_extension(f'cogs.{filename[:-3]}')
        await bot.tree.sync()

    async def on_ready(self):
        print(f"{self.user} has connected to discord {discord.__version__}")

bot = MyBot()
bot.remove_command("help")

@bot.command(aliases = ['s'])
async def shutdown(message):
    if message.author.id == 392536210616090625 or message.author.id == 515776214359867392:
        embed = discord.Embed(title = "Shutting down", description = "You better fix me Mula", colour = 0xe17d4b)
        embed.set_thumbnail(url = bot.user.avatar.url)
        embed.set_footer(text = "I'll come for your ass")
        channel = bot.get_channel(message.channel.id)
        await channel.send(embed = embed)
        await bot.close()
    else:
        return

bot.run(TOKEN)