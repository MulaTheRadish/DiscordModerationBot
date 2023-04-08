import discord
from discord.ext import commands 
import sqlite3

class QuoteCog(commands.GroupCog, name = 'quote'):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases = ['q'])
	async def quote(self, ctx):
		db = sqlite3.connect('main.db')
		cursor = db.cursor()
		result = cursor.execute(f"SELECT quoteChannelID FROM main WHERE guildID = {ctx.guild.id}").fetchone()
		if result is None:
			await ctx.send("No designated channel for quotes.")
		else:
			message = await ctx.channel.fetch_message(ctx.message.reference.message_id)
			member = message.author
			embed = discord.Embed(title = "➤", url = message.jump_url, description = f"{message.content}\n- {member.mention}", color=0xca81d1)
			embed.set_thumbnail(url = member.avatar.url)
			embed.set_footer(text=message.created_at.strftime("%A, %B %d %Y @ %H:%M:%S %p"))
			if message.attachments:
				embed.set_image(url = message.attachments[0].url)
			elif 'https://' in message.content:
				embed.set_image(url = message.content)
			channel = self.bot.get_channel(result[0])
			await channel.send(embed = embed)
	
	@discord.app_commands.command(name = "set", description = "Set quote channel.")
	@discord.app_commands.checks.has_permissions(manage_channels = True)
	async def set(self, interaction: discord.Interaction, channel: discord.TextChannel):
		db = sqlite3.connect('main.db')
		cursor = db.cursor()
		result = cursor.execute(f"SELECT quoteChannelID FROM main WHERE guildID = {interaction.guild.id}").fetchone()
		if result is None:
			sql = ("INSERT INTO main(guildID, quoteChannelID) VALUES(?, ?)")
			val = (interaction.guild.id, channel.id)
			await interaction.response.send_message(f"Quote channel has been set to {channel.mention}")
		else:
			sql = ("UPDATE main SET quoteChannelID = ? WHERE guildID = ?")
			val = (channel.id, interaction.guild.id)
			await interaction.response.send_message(f"Quote channel has been updated to {channel.mention}")
		cursor.execute(sql,val)
		db.commit()
		cursor.close()
		db.close()
		
async def setup(bot: commands.Bot):
	await bot.add_cog(QuoteCog(bot))
	print('Loaded: quote')