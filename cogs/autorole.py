import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
import sqlite3

class AutoCog(commands.GroupCog, name = 'autorole', description = 'Automatically assigns a new Member/ Bot a role.'):
    def __init__(self, bot):
        self.bot = bot
        super().__init__()
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        if member.bot:
            result = cursor.execute(f"SELECT autorole_bot_id FROM main WHERE guild_id = {member.guild.id}").fetchone()
            if result[0] is None:
                return
            else:
                autorole = discord.utils.get(member.guild.roles, id = result[0])
                await member.add_roles(autorole)
        else:
            result = cursor.execute(f"SELECT autorole_user_id FROM main WHERE guild_id = {member.guild.id}").fetchone()
            if result[0] is None:
                return
            else:
                autorole = discord.utils.get(member.guild.roles, id = result[0])
                await member.add_roles(autorole)

    @discord.app_commands.command(name = "set", description = "Sets the role which will be assigned to new members/ bots.")
    @discord.app_commands.checks.has_permissions(manage_roles = True)
    @discord.app_commands.choices(member = [
        app_commands.Choice(name = 'Bots', value = 'bot'),
        app_commands.Choice(name = 'Users', value = 'user')
    ])
    async def set(self, interaction: discord.Interaction, member: app_commands.Choice[str], role: discord.Role):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT autorole_{member.value}_id FROM main WHERE guild_id = {interaction.guild.id}").fetchone()
        if result is None:
            sql = (f"INSERT INTO main(autorole_{member.value}_id, guild_id) VALUES(?, ?)")
            val = (role.id, interaction.guild.id)
        if result is not None: 
            sql = (f"UPDATE main SET autorole_{member.value}_id = ? WHERE guild_id = ?")
            val = (role.id, interaction.guild.id)
        embed = discord.Embed(description = f'Autorole for {member.value}s has been updated to {role.mention}', colour = 0xe53838)
        await interaction.response.send_message(embed = embed)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoCog(bot))
    print('Loaded: autorole')