import discord
from discord.ext import commands

class WelcomeEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = self.bot.get_channel(1018368134828265593)
        if channel is not None:
            await channel.send(f"Bienvenue sur le serveur, {member.mention} ! 🎉 Nous sommes ravis de t'avoir parmi nous !")

async def setup(bot):
    await bot.add_cog(WelcomeEvent(bot))
