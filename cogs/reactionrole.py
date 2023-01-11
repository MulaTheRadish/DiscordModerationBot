import discord
from discord.ext import commands 
import re
import sqlite3

class RxnCog(commands.GroupCog, name = 'reactionrole'):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_raw_reaction_add(self, reaction):
		db = sqlite3.connect('main.db')
		cursor = db.cursor()
		if '<:' in str(reaction.emoji):
			cursor.execute(f"SELECT emoji, role, message_id, rxnchannel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji}'")
			guild = self.bot.get_guild(reaction.guild_id)
			result = cursor.fetchone()
			if result is None: 
				return
			elif str(reaction.emoji.id) in str(result[0]):
				on = discord.utils.get(guild.roles, id = result[1])
				user = guild.get_member(reaction.user_id)
				await user.add_roles(on)
			else:
				return
		elif '<:' not in str(reaction.emoji):
			cursor.execute(f"SELECT emoji, role, message_id, rxnchannel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji}'")
			guild = self.bot.get_guild(reaction.guild_id)
			result = cursor.fetchone()
			if result is None:
				return
			elif result is not None:
				on = discord.utils.get(guild.roles, id = result[1])
				user = guild.get_member(reaction.user_id)
				await user.add_roles(on)
			else:
				return

	@commands.Cog.listener()
	async def on_raw_reaction_remove(self, reaction):
		db = sqlite3.connect('main.db')	
		cursor = db.cursor()
		if '<:' in str(reaction.emoji):
			cursor.execute(f"SELECT emoji, role, message_id, rxnchannel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji}'")
			guild = self.bot.get_guild(reaction.guild_id)
			result = cursor.fetchone()
			if result is None: 
				return
			elif str(reaction.emoji.id) in str(result[0]):
				on = discord.utils.get(guild.roles, id = result[1])
				user = guild.get_member(reaction.user_id)
				await user.remove_roles(on)
			else:
				return
		elif '<:' not in str(reaction.emoji):
			cursor.execute(f"SELECT emoji, role, message_id, rxnchannel_id FROM reaction WHERE guild_id = '{reaction.guild_id}' and message_id = '{reaction.message_id}' and emoji = '{reaction.emoji}'")
			guild = self.bot.get_guild(reaction.guild_id)
			result = cursor.fetchone()
			if result is None: 
				return
			elif result is not None:
				on = discord.utils.get(guild.roles, id = result[1])
				user = guild.get_member(reaction.user_id)
				await user.remove_roles(on)
			else:
				return

	@discord.app_commands.command(name = "add", description = "Adds a reaction role")
	@discord.app_commands.checks.has_permissions(manage_roles = True)
	async def roleadd(self, interaction: discord.Interaction, channel:discord.TextChannel, messageid: str, emoji: str, role:discord.Role):
		db = sqlite3.connect('main.db')
		cursor = db.cursor()
		cursor.execute(f"SELECT emoji, role, message_id, rxnchannel_id FROM reaction WHERE guild_id = '{interaction.guild.id}' and message_id = '{messageid}'")
		result = cursor.fetchone()
		if '<:' in emoji:
			emm = re.sub(':.*?:', '', emoji).strip('<>')
			if result is None:
				sql = ("INSERT INTO reaction(emoji, role, message_id, rxnchannel_id, guild_id) VALUES(?, ?, ?, ?, ?)")
				VAL = (emm, role.id, messageid, channel.id, interaction.guild.id)
				msg = await channel.fetch_message(messageid)
				em = self.bot.get_emoji(emm)
				await msg.add_reaction(em)
				await interaction.response.send_message(f"{emoji} has been added.")
			elif str(messageid) not in str(result[3]):
				sql = ("INSERT INTO reaction(emoji, role, message_id, rxnchannel_id, guild_id) VALUES(?, ?, ?, ?, ?)")
				VAL = (emm, role.id, messageid, channel.id, interaction.guild.id)
				msg = await channel.fetch_message(messageid)
				em = self.bot.get_emoji(emm)
				await msg.add_reaction(em)
				await interaction.response.send_message(f"{emoji} has been added.")
		elif '<:' not in emoji:
			if result is None:
				sql = ("INSERT INTO reaction(emoji, role, message_id, rxnchannel_id, guild_id) VALUES(?, ?, ?, ?, ?)")
				VAL = (emoji, role.id, messageid, channel.id, interaction.guild.id)
				msg = await channel.fetch_message(messageid)
				await msg.add_reaction(emoji)
				await interaction.response.send_message(f"{emoji} has been added.")
			elif str(messageid) not in str(result[3]):
				sql = ("INSERT INTO reaction(emoji, role, message_id, rxnchannel_id, guild_id) VALUES(?, ?, ?, ?, ?)")
				VAL = (emoji, role.id, messageid, channel.id, interaction.guild.id)
				msg = await channel.fetch_message(messageid)
				await msg.add_reaction(emoji)
				await interaction.response.send_message(f"{emoji} has been added.")
		cursor.execute(sql, VAL)
		db.commit()
		cursor.close()
		db.close()

	@discord.app_commands.command(name = "remove", description = "Removes a reaction role")
	@discord.app_commands.checks.has_permissions(manage_roles = True)
	async def roleremove(self, interaction: discord.Interaction, messageid: str, emoji: str):
		db = sqlite3.connect('main.db')
		cursor = db.cursor()
		cursor.execute(f"SELECT emoji, role, message_id, rxnchannel_id FROM reaction WHERE guild_id = '{interaction.guild.id}' and message_id = '{messageid}'")
		result = cursor.fetchone()
		if '<:' in emoji:
			emm = re.sub(':.*?:', '', emoji).strip('<>')
			if result is None: 
				await interaction.response.send_message('That reaction was not found on that message.')
			elif str(messageid) in str(result[2]):
				cursor.execute(f"DELETE FROM reaction WHERE guild_id = '{interaction.guild.id}' and message_id = '{messageid}' and emoji = '{emm}'")
				await interaction.response.send_message('Reaction has been removed.')
			else:
				await interaction.response.send_message('That reaction was not found on that message.')
		elif '<:' not in emoji:
			if result is None: 
				await interaction.response.send_message('That reaction was not found on that message.')
			elif str(messageid) in str(result[2]):
				cursor.execute(f"DELETE FROM reaction WHERE guild_id = '{interaction.guild.id}' and message_id = '{messageid}' and emoji = '{emoji}'")
				await interaction.response.send_message('Reaction has been removed.')
			else:
				await interaction.response.send_message('That reaction was not found on that message.')
		db.commit()
		cursor.close()
		db.close()

async def setup(bot: commands.Bot):
	await bot.add_cog(RxnCog(bot))
	print('Loaded: reactionrole')