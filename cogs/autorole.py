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
            result = cursor.execute(f"SELECT autoroleBotID FROM autoroleTable WHERE guildID = {member.guild.id}").fetchone()
        else:
            result = cursor.execute(f"SELECT autoroleUserID FROM autoroleTable WHERE guildID = {member.guild.id}").fetchone()
        if result[0] is None:
            return
        else:
            autorole = discord.utils.get(member.guild.roles, id = result[0])
            await member.add_roles(autorole)

    @discord.app_commands.command(name = "set", description = "Sets the role which will be assigned to new members/ bots.")
    @discord.app_commands.checks.has_permissions(manage_roles = True)
    @discord.app_commands.choices(member = [
        app_commands.Choice(name = 'Bots', value = 'autoroleBotID'),
        app_commands.Choice(name = 'Users', value = 'autoroleUserID')
    ])
    async def set(self, interaction: discord.Interaction, member: app_commands.Choice[str], role: discord.Role):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT {member.value} FROM autoroleTable WHERE guildID = {interaction.guild.id}").fetchone()
        if result is None:
            sql = (f"INSERT INTO autoroleTable({member.value}, guildID) VALUES(?, ?)")
            val = (role.id, interaction.guild.id)
        if result is not None: 
            sql = (f"UPDATE autoroleTable SET {member.value} = ? WHERE guildID = ?")
            val = (role.id, interaction.guild.id)
        embed = discord.Embed(description = f'Autorole for {member.name} has been updated to {role.mention}', colour = 0xe53838)
        await interaction.response.send_message(embed = embed)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(AutoCog(bot))
    print('Loaded: autorole')