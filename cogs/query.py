import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class QueryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @discord.app_commands.command(name = 'query', description = 'Know about the current configurations of the server.')
    @discord.app_commands.choices(query = [
        app_commands.Choice(name = 'Autorole', value = 'autorole'),
        app_commands.Choice(name = 'Media Only', value = 'media only')
        ])
    async def query(self, interaction: discord.Interaction, query: app_commands.Choice[str]):
        
        if query.value == 'autorole':
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            result = cursor.execute(f"SELECT autoroleUserID, autoroleBotID FROM autoroleTable WHERE guild_id = {interaction.guild.id}").fetchone()
            if result is None:
                embed = discord.Embed(title = "Neither bots nor users will be assigned new roles.")
                embed.set_thumbnail(url=f"{interaction.guild.icon.url}")
                await interaction.response.send_message(embed = embed)
            else:
                embed = discord.Embed(colour = 0xe53838)
                embed.set_thumbnail(url=f"{interaction.guild.icon.url}")
                if result[0] is not None:
                    role = discord.utils.get(interaction.guild.roles, id = result[0])
                    embed.add_field(name = "New Users will recieve the following role:", value = f"{role.mention}", inline = False)
                if result[1] is not None:
                    role = discord.utils.get(interaction.guild.roles, id = result[1])
                    embed.add_field(name = "New Bots will recieve the following role:", value = f"{role.mention}", inline = False)
                await interaction.response.send_message(embed = embed)
        
        if query.value == 'media only':
            description = ""
            db = sqlite3.connect('main.db')
            cursor = db.cursor()
            result = cursor.execute(f"SELECT channelID FROM mediaOnlyTable WHERE guildID = {interaction.guild.id}").fetchall()
            for channel in result:
                description += f"<#{channel[0]}>\n"
            embed = discord.Embed(title = "Current Media Only Channels:", description = description)
            await interaction.response.send_message(embed = embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(QueryCog(bot))
    print('Loaded: query')