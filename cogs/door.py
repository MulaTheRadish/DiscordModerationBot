import discord
from discord.ext import commands 
from discord import app_commands
import sqlite3

async def update_members(self, door, title, description, member):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT {door} FROM main WHERE guild_id = {member.guild.id}").fetchone()
        if result is None:
            return
        else:
            embed = discord.Embed(title = f"{title} {member.guild}!", description = f"{description} {member.mention}!", color=0x3073f8)
            embed.set_thumbnail(url = member.avatar.url)
            channel = self.bot.get_channel(result[0])
            await channel.send(embed = embed)

class DoorCog(commands.GroupCog, name = 'door', description = "Welcome/ Leave messages for members."):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        await update_members(self, "welcome_ch_id", "Welcome to", "Hello", member)
        
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        await update_members(self, "leave_ch_id", "Sorry to see you leave", "Goodbye", member)

    @discord.app_commands.command(name = "set", description = "Designates a channel for welcome and/or leave messages.")
    @discord.app_commands.checks.has_permissions(manage_channels = True)
    @discord.app_commands.choices(doors = [
        app_commands.Choice(name = "Welcome", value = "welcome_ch_id"),
        app_commands.Choice(name = "Leave", value = "leave_ch_id")
    ])
    async def door(self, interaction, doors: app_commands.Choice[str], channel: discord.TextChannel):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT {doors.value} FROM main WHERE guild_id = {interaction.guild.id}").fetchone()
        if result is None:
            sql = (f"INSERT INTO main(guild_id, {doors.value}) VALUES(?, ?)")
            val = (interaction.guild.id, channel.id)
        else:
            sql = (f"UPDATE main SET {doors.value} = ? WHERE guild_id = ?")
            val = (channel.id, interaction.guild.id)
        await interaction.response.send_message(f"{doors.name} channel has been set to {channel.mention}")
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(DoorCog(bot))
    print('Loaded: door')