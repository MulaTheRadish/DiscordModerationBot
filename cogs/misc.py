import discord
from discord.ext import commands
from PIL import Image
from io import BytesIO

from discord import ui, Interaction

def hex_to_rgb(hex):
	rgb = []
	for i in (0, 2, 4):
		decimal = int(hex[i : i + 2], 16)
		rgb.append(decimal)
	return tuple(rgb)

class Embed_Generator(ui.View, title = 'Embed Generator'):
	
	@ui.select(cls = ui.ChannelSelect, placeholder = "Select a channel please!", channel_types=[discord.ChannelType.text])
	async def my_user_select(self, interaction: Interaction, select: ui.ChannelSelect):
		print(self.channel)

class MiscCog(commands.Cog, name = 'Misc'):
	def __init__(self, bot):
		self.bot = bot

	@discord.app_commands.command(name = "embed", description = "Create an embed in any specified channel.")
	@discord.app_commands.checks.has_permissions(manage_messages = True)
	async def embed(self, interaction: discord.Interaction):
		await interaction.response.send_modal(Embed_Generator())

	@commands.command()
	async def count(self, ctx):
		member_count = len(ctx.guild.members)
		true_member_count = len([m for m in ctx.guild.members if not m.bot])
		bot_count = member_count - true_member_count
		embed = discord.Embed(colour = 0x99b67e)
		embed.set_thumbnail(url=f"{ctx.guild.icon.url}")
		embed.add_field(name = "Member Count:", value = f"{member_count}", inline = False)
		embed.add_field(name = "Bot Count:", value = f"{bot_count}", inline = False)
		embed.add_field(name = "User Count:", value = f"{true_member_count}", inline = False)
		embed.set_footer(text = "Tip: Inviting more people increases the Member and User Count!")
		await ctx.send(embed = embed)

	@commands.command(aliases = ['pfp', 'p'])
	async def picture(self, ctx, user: discord.User = None):
		if user is None:
			user = ctx.message.author
		user = await self.bot.fetch_user(user.id)
		embed = discord.Embed(colour = user.accent_colour)
		embed.set_image(url = user.avatar.url)
		await ctx.send(embed = embed)

	@commands.command(aliases = ['b', 'bn'])
	async def banner(self, ctx, user: discord.User = None):
		if user is None: 
			user = ctx.message.author
		colour_string = f"{user.accent_colour}"
		embed = discord.Embed(colour = user.accent_colour)
		embed.set_footer(text = colour_string)
		if user.banner:
			embed.set_image(url = user.banner.url)
			await ctx.send(embed = embed)
		else:
			banner = Image.new(mode = "RGB", size = (600, 240), color = hex_to_rgb(colour_string[1:]))
			with BytesIO as image_binary:
				banner.save(image_binary, 'PNG')
				image_binary.seek(0)
				file = discord.file(fp = image_binary, filename = "banner.png")
				await ctx.send(file = file, embed = embed)
	
async def setup(bot: commands.Bot):
	await bot.add_cog(MiscCog(bot))
	print('Loaded: misc')