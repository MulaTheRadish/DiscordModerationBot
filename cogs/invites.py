import discord
from discord.ext import commands
from discord import app_commands
import sqlite3

class inviteCog(commands.GroupCog, name = 'invite'):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name = "create", description = "Create a limited server invite unique to you")
    async def limit(self, interaction: discord.Interaction):
        db = sqlite3.connect('main.db')
        cursor = db.cursor()
        result = cursor.execute(f"SELECT invitesCreated FROM invitesTable WHERE guildID = {interaction.guild.id} and userID = {interaction.user.id}").fetchone()
        print(interaction.user.id)
        print(interaction.guild.id)
        print(result)
        if result is not None:
            await interaction.response.send_message("You only get to create 1 invite link per person in this server, of which, you've already used.", ephemeral = True)
        else: 
            sql = (f"INSERT INTO invitesTable(guildID, userID, invitesCreated) VALUES(?, ?, ?)")
            val = (interaction.guild.id, interaction.user.id, 1)
            link = await interaction.channel.create_invite(max_uses = 1)
            await interaction.response.send_message(f"Your link is ready: {link}, you have a limited selection.", ephemeral = True)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(inviteCog(bot))
    print('Loaded: invites')