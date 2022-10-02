# The commands:
#   +say #channel message
#   +giverole @user role name
#   +removerole @user role name
#   +kick @user reason
#   +mute @user
#   +unmute @user
#   +warn @user reason
#   +directmessage @user message
#   +clear amount
#   +delete
# All of the commands above are in the same order as they are in the code

import discord
from discord.ext import commands
from decouple import config

bot  =  commands.Bot(intents = discord.Intents().all(), command_prefix = '+', help_command = None)

embed = discord.Embed(color = 0xffffff)
embed.set_author(name = 'LuxBot', icon_url = 'https://cdn.discordapp.com/attachments/1024218756098035722/1024711066221019276/LuxLogoBW.png')
embed.add_field(name = 'Command usage', value = '+say #channel message\n+giverole @user role name\n+removerole @user role name\n+kick @user\n+mute @user\n+unmute @user\n+warn @user reason\n+directmessage @user message\n+clear amount\n+delete')
embed.add_field(name = 'Command explanation', value = 'say: Sends a message in a channel, if no channel specified the message will be sent into the users channel\ngiverole: Gives a role to a user\nremoverole: Removes a role from a user\nkick: Kicks a user from the server\nmute: Prohibits a user from typing\nunmute: Allows users to type again\nwarn: Warns a user for the given reason\ndirectmessage: Sends a private message to a user\nclear: Deletes an amount of messages. If no amount specified, every message in that channel will get deleted\ndelete: Deletes the previous message')
embed.add_field(name = 'Command aliases', value = 'say: tell\ndirectmessage: dm\nclear: purge, cls\ndelete: del')

@bot.command(pass_context = True, name = 'help')
async def help(ctx):
    await ctx.send(embed = embed)

@bot.command(pass_context = True, name = 'say', aliases = ['tell'])
async def saycmd(ctx, channelGiven: str, *, message: str = None):
    channelNew = channelGiven.removeprefix('<#').removesuffix('>')
    for channel in ctx.guild.channels:
        if isinstance(channel, discord.TextChannel):
            if channelNew == str(channel.id):
                await channel.send(message)
                return
            elif str(ctx.channel.id) == str(channel.id):
                if not message:
                    await ctx.send(channelGiven)
                else:
                    await ctx.send(channelGiven + ' ' + message)

@bot.command(pass_context = True, name = 'giverole')
async def giverole(ctx, user: discord.Member, role: discord.Role):
    await user.add_roles(role)
    await ctx.send(f'Succesfully gave **{user}** the **{role.name}** role.')

@bot.command(pass_context = True, name = 'removerole')
async def removerole(ctx, user: discord.Member, role: discord.Role):
    await user.remove_roles(role)
    await ctx.send(f'Succesfully removed the **{role.name}** role from **{user}**.')

@bot.command(pass_context = True, name = 'kick')
async def kick(ctx, user: discord.Member):
    await user.kick()
    await ctx.send(f'Succesfully kicked **{user}**.')

@bot.command(pass_context = True, name = 'mute')
async def mute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    if not role:
        await ctx.send('Creating **Muted** role')
        await ctx.guild.create_role(name='Muted', permissions = discord.Permissions(1115137))
        role = discord.utils.get(ctx.guild.roles, name='Muted')
        for channel in ctx.guild.channels:
            if isinstance(channel, discord.TextChannel):
                await channel.set_permissions(role, send_messages = False)
        await user.add_roles(role)
        await ctx.send(f'Succesfully muted **{user}**.')
    else:
        await user.add_roles(role)
        await ctx.send(f'Succesfully muted **{user}**.')

@bot.command(pass_context = True, name = 'unmute')
async def unmute(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name='Muted')
    await user.remove_roles(role)
    await ctx.send(f'Succesfully unmuted **{user}**.')

@bot.command(pass_context = True, name = 'warn')
async def warn(ctx, user: discord.Member, *, reason: str):
    await ctx.send(f'**{user}** has been warned for **{reason}**')
    await user.send(f'You have been warned on **{ctx.guild.name}** for **{reason}**')

@bot.command(pass_context = True, name = 'directmessage', aliases = ['dm'])
async def directmessage(ctx, user: discord.Member, *, message: str):
    await user.send(message)
    await ctx.send(f'Succesfully sent message: **{message}** to **{user}**.')

@bot.command(pass_context = True, name = 'clear', aliases = ['purge', 'cls'])
async def clear(ctx, amount: int = None):
    if amount  ==  None:
        await ctx.channel.purge(limit = 10000)
    else:
        await ctx.channel.purge(limit = amount+1)

@bot.command(pass_context = True, name = 'delete', aliases = ['del'])
async def delete(ctx):
    await ctx.channel.purge(limit = 2)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(error)

@bot.event
async def on_ready():
    print('{0.user}'.format(bot))
    await bot.change_presence(activity = discord.Activity(type = discord.ActivityType.listening, name = '+help'))

bot.run(config('TOKEN'))