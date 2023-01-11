import discord
from discord.ext import commands

class ModCog(commands.Cog, name = 'moderation'):
    def __init__(self, bot):
        self.bot = bot

    @discord.app_commands.command(name = "lock", description = "Locks the channel")
    @discord.app_commands.checks.has_permissions(manage_channels = True)
    async def lock(self, interaction: discord.Interaction):
        perms = interaction.channel.overwrites_for(interaction.guild.default_role)
        perms.send_messages = False
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite = perms)
        embed = discord.Embed(title=f"{interaction.channel} has been locked", color=0xf8a630)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name = "unlock", description = "Unlocks the channel")
    @discord.app_commands.checks.has_permissions(manage_channels = True)
    async def unlock(self, interaction: discord.Interaction):
        perms = interaction.channel.overwrites_for(interaction.guild.default_role)
        perms.send_messages = None
        await interaction.channel.set_permissions(interaction.guild.default_role, overwrite = perms)
        embed = discord.Embed(title=f"{interaction.channel} has been unlocked", color=0xf8a630)
        await interaction.response.send_message(embed=embed)

    @discord.app_commands.command(name = "clear", description = "Deletes the selected number of messages")
    @discord.app_commands.checks.has_permissions(manage_messages = True)
    async def clear(self, interaction:discord.Interaction, number: int):
        await interaction.response.send_message(f"Clearing {number} messages")
        await interaction.channel.purge(limit = number)

async def setup(bot: commands.Bot):
    await bot.add_cog(ModCog(bot))
    print('Loaded: moderation')