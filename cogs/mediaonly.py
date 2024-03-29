import discord
from discord.ext import commands
import sqlite3

class MOCog(commands.GroupCog, name = 'mo'):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name = "set", description = "Add a media only channel.")
    @discord.app_commands.checks.has_permissions(manage_channels = True)
    async def set(self, interaction: discord.Interaction, channel: discord.TextChannel):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT channelID FROM mediaOnlyTable WHERE guildID = {interaction.guild.id}").fetchall()
        if channel.id in result[0]:
            await interaction.response.send_message(f"{channel.mention} is already a media only channel.")
        else:
            sql = ("INSERT INTO mediaOnlyTable(guildID, channelID) VALUES(?, ?)")
            val = (interaction.guild.id, channel.id)
            cursor.execute(sql, val)
            await interaction.response.send_message(f"{channel.mention} has been added to media only channels.")
        db.commit()
        cursor.close()
        db.close()
    
    @discord.app_commands.command(name = "remove", description = "Remove a media only channel.")
    @discord.app_commands.checks.has_permissions(manage_channels = True)
    async def remove(self, interaction: discord.Interaction, channel:discord.TextChannel):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT channelID FROM mediaOnlyTable WHERE guildID = {interaction.guild.id}").fetchall()
        if channel.id in result[0]:
            cursor.execute(f"DELETE FROM mediaOnlyTable WHERE channelID = {channel.id}")
            await interaction.response.send_message(f"{channel.mention} is no longer a media only channel.")
        else: 
            await interaction.response.send_message(f"{channel.mention} is not a media only channel.")
        db.commit()
        cursor.close()
        db.close()
    
    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT channelID FROM mediaOnlyTable WHERE guildID = {message.guild.id}").fetchone()
        if result is None:
            pass
        elif message.channel.id not in result[0]:
            pass
        elif not message.attachments or 'https://' not in message.content or not message.author.bot:
            await message.delete()
        
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT channelID FROM mediaOnlyTable WHERE guildID = {channel.guild.id}").fetchall()
        if channel.id in result[0]:
            cursor.execute(f"DELETE channelID FROM mediaOnlyTable WHERE channelID = {channel.id}")
        db.commit()
        cursor.close()
        db.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(MOCog(bot))
    print('Loaded: mediaonly')
