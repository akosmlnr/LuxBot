# The commands:
#   +say #channel message
#   +giverole @user role name
#   +removerole @user role name
#   +kick @user reason
#   +dm @user message
#   +clear amount
#   +delete
# All of the commands above are in the same order as they are in the code

import discord
from discord.ext import commands
from decouple import config

bot = commands.Bot(intents=discord.Intents().all(), command_prefix='+', help_command=None)

embed = (discord.Embed(title='Commands', description='+say <#channel> <message>\n+giverole <@user> <role name>\n+removerole <@user> <role name>\n+kick <@user>\n+dm <@user> <message>\n+clear/purge/cls <number>\n+delete/del', color=0xffffff))
embed.set_author(name='LuxBot', icon_url='https://raw.githubusercontent.com/akosmlnr/LuxBot/master/Assets/LuxLogoBW.png')

@bot.command(pass_context=True, name='help')
async def help(ctx):
    await ctx.send(embed=embed)

@bot.command(pass_context=True, name='say')
async def say(ctx, channel: discord.TextChannel, *, message: str):
    await channel.send(message)

@bot.command(pass_context=True, name='giverole')
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f'Succesfully gave **{user}** the **{role.name}** role.')

@bot.command(pass_context=True, name='removerole')
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f'Succesfully removed the **{role.name}** role from **{user}**.')

@bot.command(pass_context=True, name='kick')
async def kick(ctx, user: discord.Member):
    await user.kick()
    await ctx.send(f'Succesfully kicked **{user}**.')

@bot.command(pass_context=True, name='dm')
async def dm(ctx, user: discord.Member, *, message: str):
    await user.send(message)
    await ctx.send(f'Succesfully sent message: **{message}** to **{user}**.')

@bot.command(pass_context=True, name='clear', aliases=['purge', 'cls'])
async def clear(ctx, amount: int=None):
    if amount == None:
        await ctx.channel.purge(limit=10000)
    else:
        await ctx.channel.purge(limit=amount+1)

@bot.command(pass_context=True, name='delete', aliases=['del'])
async def delete(ctx):
    await ctx.channel.purge(limit=2)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@bot.event
async def on_ready():
    print('{0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="+help"))

bot.run(config('TOKEN'))