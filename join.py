from discord.ext import commands
import discord

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Do something when a member joins the server
        welcome_channel = member.guild.get_channel(1186421848230084708)
        if welcome_channel:
            member_count = member.guild.member_count

            embed = discord.Embed(
                title=f'Welcome to {member.guild.name}, {member.display_name}!',
                description=f'{member.mention} has joined the server! We now have {member_count} Members',
                color=discord.Color.green()
            )
            
            # Access the avatar URL directly from the Member object
            avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
            embed.set_thumbnail(url=avatar_url)
            await welcome_channel.send(embed=embed)

            # Save member information to a file
            self.save_member_info(member)

    def save_member_info(self, member):
        with open('member_info.txt', 'a') as file:
            file.write(f'Member Joined: {member.name}#{member.discriminator} ({member.id})\n')

def setup(bot):
    bot.add_cog(Events(bot))
