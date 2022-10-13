import nextcord
from nextcord import Interaction, SlashOption
from nextcord.ext import commands
import os
import logging
from typing import Optional
from datetime import datetime, timedelta, date, time
import string
TOKEN = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.default()
intents = nextcord.Intents().all()
intents.message_content = True
bot = commands.Bot(command_prefix = ".", intents = intents)

@bot.event
async def on_ready():
    print("{0.user}".format(bot) + " has been initialized")

# ~~~~~ AUDIT LOG ~~~~~
logging = True
logschannel = #Paste a Text channel's ID

# ~~~~~~ ADMIN COMMANDS {prefix} ~~~~~~

#kick
@commands.has_permissions(kick_members = True)
@bot.command(pass_context = True)
async def kick(ctx, user: nextcord.Member = None, *, reason = "No reason provided"):
    if user is None:
        embed = nextcord.Embed(color = 0xff6a00, title = "No User mentioned", description = "Please specify a user to kick.")
        await ctx.send(embed = embed)
    elif user == ctx.message.author:
        embed = nextcord.Embed(color = 0xff6a00, title = "You cannot kick yourself", description = "Are you stoopid?")
        await ctx.send(embed = embed)
    elif user.guild_permissions.administrator:
        embed = nextcord.Embed(color = 0xff6a00, title = "You cannot kick an Admin", description = "This user is an Admin, you cannot kick them")
        await ctx.send(embed = embed)
    else:
        DMembed = nextcord.Embed(color = 0xff6a00, title = f"You have been kicked from {user.guild.name}", description = f"Kicked for: **{reason}**\n Kicked by: {ctx.author.name}")
        await user.send(embed = DMembed)
        await user.kick(reason = reason)
        embed = nextcord.Embed(color = 0xff6a00, title = f"Kicked {user}", description = f"{user.mention} has been kicked for **{reason}** by {ctx.author.mention}")
        await ctx.send(embed = embed)
        if logging is True:
            log_channel = bot.get_channel(logschannel)
            embed = nextcord.Embed(color = 0xff6a00, title = f"Kicked {user}", description = f"{user.mention} has been kicked for **{reason}** by {ctx.author.mention}")
            await log_channel.send(embed = embed)

#ban
@commands.has_permissions(ban_members = True)
@bot.command(pass_context = True)
async def ban(ctx, user: nextcord.Member = None, *, reason = "No reason provided"):
    if user is None:
        embed = nextcord.Embed(color = 0xff0000, title = "No User mentioned", description = "Please specify a user to ban.")
        await ctx.send(embed = embed)
    elif user == ctx.message.author:
        embed = nextcord.Embed(color = 0xff0000, title = "You cannot ban yourself", description = "Are you stoopid?")
        await ctx.send(embed = embed)
    elif user.guild_permissions.administrator:
        embed = nextcord.Embed(color = 0xff0000, title = "You cannot ban an Admin", description = "This user is an Admin, you cannot ban them")
        await ctx.send(embed = embed)
    else:
        DMembed = nextcord.Embed(color = 0xff0000, title = f"You have been banned from {user.guild.name}", description = f"Banned for: **{reason}**\n Banned by: {ctx.author.name}")
        await user.send(embed = DMembed)
        await user.ban(reason = reason)
        embed = nextcord.Embed(color = 0xff0000, title = f"Banned {user}", description = f"{user.mention} has been banned for **{reason}** by {ctx.author.mention}")
        await ctx.send(embed = embed)
        if logging is True:
            log_channel = bot.get_channel(logschannel)
            embed = nextcord.Embed(color = 0xff0000, title = f"Banned {user}", description = f"{user.mention} has been banned for **{reason}** by {ctx.author.mention}")
            await log_channel.send(embed = embed)

#unban
@commands.has_permissions(ban_members = True)
@bot.command(pass_context = True)
async def unban(ctx, id: int = None):
    if id is None:
        embed = nextcord.Embed(color = 0x00ff04, title = "No User mentioned", description = "Please specify an ID to unban.")
        await ctx.send(embed = embed)
    else:
        user = await client.fetch_user(id)
        await ctx.guild.unban(user)
        embed = nextcord.Embed(color = 0x00ff04, title = f"Unbanned {user}", description = f"{user.mention} has been unbanned by {ctx.author.mention}")
        await ctx.send(embed = embed)
        if logging is True:
            log_channel = bot.get_channel(logschannel)
            embed = nextcord.Embed(color = 0x00ff04, title = f"Unbanned {user}", description = f"{user.mention} has been unbanned by {ctx.author.mention}")
            await log_channel.send(embed = embed)

#Clear messages
@commands.has_permissions(manage_messages = True)
@bot.command(pass_context = True, name = "clear", aliases = ["purge"])
async def purge(ctx, limit: Optional[int] = 1):
    if 0 < limit <= 100:
        await ctx.message.delete()
        deleted = await ctx.channel.purge(limit = limit)
        await ctx.send(f"Deleted {len(deleted):,} messages.", delete_after = 5)
    else:
        await ctx.send("The limit provided is not within acceptable bounds.")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# ~~~~~~ ADMIN COMMANDS {slash} ~~~~~~

#Kick
@bot.slash_command(description = "Kick a member")
async def kick(interaction: nextcord.Interaction, user:nextcord.Member, reason: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not authorized to run this commannd.", ephemeral = True)
    else:
        DMembed = nextcord.Embed(color = 0xff6a00, title = f"You have been kicked from {user.guild.name}", description = f"Kicked for: **{reason}**\n Kicked by: {interaction.user.mention}")
        await user.send(embed = DMembed)
        await interaction.response.send_message(f"Kicked {user.mention}", ephemeral = True)
        if logging is True:
            log_channel = bot.get_channel(logschannel)
            embed = nextcord.Embed(color = 0xff6a00, title = f"Kicked {user}", description = f"{user.mention} has been kicked for **{reason}** by {interaction.user.mention}")
            await log_channel.send(embed = embed)
        await user.kick(reason = reason)

#Ban
@bot.slash_command(description = "Ban a member")
async def ban(interaction: nextcord.Interaction, user:nextcord.Member, reason: str):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not authorized to run this commannd.", ephemeral = True)
    else:
        DMembed = nextcord.Embed(color = 0xff0000, title = f"You have been banned from {user.guild.name}", description = f"Banned for: **{reason}**\n Banned by: {interaction.user.mention}")
        await user.send(embed = DMembed)
        await interaction.response.send_message(f"Banned {user.mention}", ephemeral = True)
        if logging is True:
            log_channel = bot.get_channel(logschannel)
            embed = nextcord.Embed(color = 0xff0000, title = f"Banned {user}", description = f"{user.mention} has been banned for **{reason}** by {interaction.user.mention}")
            await log_channel.send(embed = embed)
        await user.ban(reason = reason)

#Unban
@bot.slash_command(description = "Unban a member")
async def unban(interaction: nextcord.Interaction, user:nextcord.Member):
    if not interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("You are not authorized to run this commannd.", ephemeral = True)
    else:
        await interaction.response.send_message(f"Unbanned {user.mention}", ephemeral = True)
        if logging is True:
            log_channel = bot.get_channel(logschannel)
            embed = nextcord.Embed(color = 0x00ff04, title = f"Unbanned {user}", description = f"{user.mention} has been unbanned by {interaction.user.mention}")
            await log_channel.send(embed = embed)
        await interaction.guild.unban(user)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# ~~~~~ USER COMMANDS {prefix} ~~~~~

#Member Count
@bot.command(aliases = ["membercount"])
async def members(ctx):
    await ctx.send(f'{ctx.guild.member_count}')

#ABout me and my dev
@bot.command(aliases = ["aboutme"])
async def about(ctx):
    embed = nextcord.Embed(color = 0xc2cc00, title = "About me and my dev", description = " ")
    await ctx.send(embed = embed)

#Ping
@bot.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

#Dev time
@bot.command()
async def time(ctx):
    time = datetime.now()
    timestr = time.isoformat(' ', 'seconds')
    await ctx.send(f"Current time: {timestr}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

# ~~~~~ USER COMMANDS {slash} ~~~~~

#Help
@bot.slash_command(description = "Shows the list of commands for Jazbot")
async def help(interaction: nextcord.Integration):
    await interaction.response.send_message("Command under maintainance")

#Member count
@bot.slash_command(description = "Shows the total number of members in the guild")
async def members(interaction: nextcord.Integration, user: nextcord.Member):
    await interaction.response.send_message(f"{user.guild.member_count}")

#About bot and dev
@bot.slash_command(description = "About bot and dev")
async def help(interaction: nextcord.Integration):
    embed = nextcord.Embed(color = 0xc2cc00, title = "About me and my dev", description = " ")
    await interaction.response.send_message(embed = embed)

#Ping
@bot.slash_command(description = "Check bot Ping")
async def ping(interaction: nextcord.Integration):
    await interaction.response.send_message(f"Pong! {round(bot.latency * 1000)}ms")

#Dev time
@bot.slash_command(description = "Shows the time at dev's place")
async def time(interaction: nextcord.Integration):
    time = datetime.now()
    timestr = time.isoformat(' ', 'seconds')
    await interaction.response.send_message(f"Current time: {timestr}")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

bot.run(TOKEN)
