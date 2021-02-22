import discord
from discord.ext import commands, owoify
from discord.ext.commands import Cog
from discord.ext.commands import command
from discord.utils import get
from discord import Activity, ActivityType, Embed
from discord import __version__ as discord_version

import datetime
from datetime import timedelta
import time
from time import sleep as bedtime


import platform


import random
import asyncio
import os
from gtts import gTTS
import io
from PIL import Image


class Random(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @command()
    async def owoify(self, ctx, text):
        lol = await owoify.owoify(f"{text}")
        await ctx.send(lol)
        
            
    @command()
    @commands.cooldown(1, 40, commands.BucketType.guild)
    async def magic(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        file = await self.bot.se.magic(f'{user.avatar_url}')
        filea = discord.File(file, "floor.gif")
        di = discord.Embed(title="Woah, **bakayaro phonaryo** is cool :sunglasses:",  description="I just got you a filter, you like?")
        di.set_image(url="attachment://floor.gif")
        await ctx.send(file=filea, embed=di)
        
    @magic.error
    async def magic_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            l = self.bot.get_command("magic")
            left = l.get_cooldown_retry_after(ctx)
            msg = await ctx.send("Just Getting The Cooldown")
            e = discord.Embed(
                title=f"Cooldown left - {round(left)}", color=discord.colour.Color.from_rgb(231, 84, 128))
            await msg.edit(content="", embed=e)
            
    
    @command()
    @commands.cooldown(1, 40, commands.BucketType.guild)
    async def braille(self, ctx, user: discord.Member=None):
        user = user or ctx.author
        file = await self.bot.se.braille(f'{user.avatar_url}')
        await ctx.send(file)
        
    @braille.error
    async def braille_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            l = self.bot.get_command("braille")
            left = l.get_cooldown_retry_after(ctx)
            msg = await ctx.send("Just Getting The Cooldown")
            e = discord.Embed(
                title=f"Cooldown left - {round(left)}", color=discord.colour.Color.from_rgb(231, 84, 128))
            await msg.edit(content="", embed=e)
            
    @command()
    @commands.cooldown(1, 40, commands.BucketType.guild)
    async def qr(self, ctx, colour="255-255-255", *, url=None):
        colours = dict([("255-255-255", "255-255-255"),
                        ("black", "0-0-0"), ("red", "FF0000"), ("blue", "00f")])
        col = ["black", "red", "blue"]
        if colour == "255-255-255":
            col = ["255-255-255", "red", "blue"]
        e = discord.Embed(title="Here you go, Made qr code!")
        msg = await ctx.send("Creating!")

        if colour in col:
            yes = (colours[colour])
            url1 = url.replace(" ", "+")
            qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={url1}&bgcolor={yes}"
            e.set_image(url=qr)
            await msg.edit(content="", embed=e)

        else:
            if not colour in col:
                if url is None:
                    url = ""
                colour = f"{colour} {url}"
                colour1 = colour.replace(" ", "+")
                qr = f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={colour1}"
                e.set_image(url=qr)
                await msg.edit(content="", embed=e)
            else:
                pass
    @qr.error
    async def qr_handler(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            l = self.bot.get_command("qr")
            left = l.get_cooldown_retry_after(ctx)
            msg = await ctx.send("Just Getting The Cooldown")
            e = discord.Embed(
                title=f"Cooldown left - {round(left)}", color=discord.colour.Color.from_rgb(231, 84, 128))
            await msg.edit(content="", embed=e)

    @command(usage="remind <time> <reminder> (Time needs to be in seconds...)")
    async def remind(self, ctx, time, *, reminder):
        e = discord.Embed(title="I will remind you!",
                          descripition=f"I will you remind you in {time} seconds!")
        await ctx.send(embed=e)
        await asyncio.sleep(int(time))
        e2 = discord.Embed(
            title=f"Hello {ctx.author}", description=f"I have come to remind you to {reminder}!")
        await ctx.message.reply(embed=e2)

    @command(pass_context=True, usage="ar <role>")
    async def ar(self, ctx, *, role1):
        member = ctx.message.author
        role = discord.utils.get(member.guild.roles, name=f"{role1}")
        await member.add_roles(role)
        e = discord.Embed(
            title="Added Roles", description=f"I have added the roles '{role1}' for you!")
        await ctx.send(embed=e)

    @command(usage="sn <name>")
    async def sn(self, ctx, *, name):
        tts = gTTS(text=f"Hi! {name} is really cool!", lang='en')
        tts.save("announce.mp3")
        await ctx.send(file=discord.File("announce.mp3"))
        await asyncio.sleep(5)
        os.remove("announce.mp3")

    @command(usage="tts <text>")
    async def tts(self, ctx, *, text):
        lol = gTTS(text=f"{text}")
        lol.save("tts.mp3")
        await ctx.send(file=discord.File("tts.mp3"))
        await asyncio.sleep(5)
        os.remove("tts.mp3")

    @command(name="stats", description="A usefull command that displays bot statistics.", usage="stats")
    async def stats(self, ctx):
        pythonVersion = platform.python_version()
        dpyVersion = discord.__version__
        serverCount = len(self.bot.guilds)
        memberCount = len(set(self.bot.get_all_members()))

        embed = discord.Embed(
            title=f"{self.bot.user.name} Stats",
            description="\uFEFF",
            colour=ctx.author.colour,
            timestamp=ctx.message.created_at,
        )

        embed.add_field(name="Bot Version:", value=self.bot.version)
        embed.add_field(name="Python Version:", value=pythonVersion)
        embed.add_field(name="Discord.Py Version", value=dpyVersion)
        embed.add_field(name="Total Guilds:", value=serverCount)
        embed.add_field(name="Total Users:", value=memberCount)
        embed.add_field(name="Bot Developers:", value="DHRUVA SHAW#0550")

        embed.set_footer(text=f"{ctx.author} | {self.bot.user.name}")
        embed.set_author(name=self.bot.user.name,
                         icon_url=self.bot.user.avatar_url)

        await ctx.send(embed=embed)

    @command(aliases=['color', 'colour', 'sc'])
    async def show_color(self, ctx, *, color: discord.Colour):
        '''Enter a color and you will see it!'''
        file = io.BytesIO()
        Image.new('RGB', (200, 90), color.to_rgb()).save(file, format='PNG')
        file.seek(0)
        em = discord.Embed(color=color, title=f'Showing Color: {str(color)}')
        em.set_image(url='attachment://color.png')
        await ctx.send(file=discord.File(file, 'color.png'), embed=em)

    @command()
    async def hi(self, ctx):
        await ctx.send("hi.")

    @command()
    async def gay(self, ctx):
        await ctx.send(f"You are {random.randint(1, 100)}% gay")


def setup(bot):
    bot.add_cog(Random(bot))