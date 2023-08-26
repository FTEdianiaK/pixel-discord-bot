# Pixel: Discord bot for my private server, Foxie's Cookie Jar.
# Copyright (C) 2023 Foxie EdianiaK a.k.a. F_TEK

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import discord
from discord.ext import commands
from os import system
import csv
import requests
import json
from alive_progress import alive_bar
from alive_progress import config_handler
from datetime import datetime


# Window title change
system("title Pixel")


# Bot pre-setup
intents = discord.Intents.default()
intents.message_content = True

activity = discord.Activity(name="updates for you :3",
                            type=discord.ActivityType.watching)

bot = commands.Bot(command_prefix="p.", intents=intents, activity=activity)


# Creates necessary files
try:
    with open("secrets.json", "x", encoding="utf-8") as f:
        _dat = {"dis": "BOT TOKEN HERE",
                "yt": "API KEY HERE",
                "itch": "JSON LINK HERE",
                "us": "API KEY HERE"}
        json.dump(_dat, f)
        f.close()
except FileExistsError:
    pass

try:
    with open("github.csv", "x", encoding="utf-8") as f:
        f.close()
except FileExistsError:
    pass

try:
    with open("youtube.csv", "x", encoding="utf-8") as f:
        f.close()
except FileExistsError:
    pass

try:
    with open("itch.csv", "x", encoding="utf-8") as f:
        f.close()
except FileExistsError:
    pass

try:
    with open("unsplash.csv", "x", encoding="utf-8") as f:
        f.close()
except FileExistsError:
    pass

try:
    with open("updated.txt", "x", encoding="utf-8") as f:
        f.close()
except FileExistsError:
    pass


# Constants list
TOKENS = {}      # dis, yt, itch, us
GITHUB = []      # 0 repo, 1 mem, 2 channel, 3 role
YOUTUBE = []     # 0 id, 1 mem, 2 channel, 3 msg, 4 role
ITCH = []        # 0 game, 1 mem, 2 channel, 3 role
UNSPLASH = []    # 0 user, 1 mem, 2 channel, 3 role
UPDATED = ""     # last check date


# Loads files
with open("secrets.json", "r", encoding="utf-8") as f:
    TOKENS = json.load(f)
    f.close()

with open("github.csv", "r", encoding="utf-8") as f:
    _raw = csv.reader(f)
    for _row in _raw:
        if _row != []:
            GITHUB.append(_row)
    f.close()

with open("youtube.csv", "r", encoding="utf-8") as f:
    _raw = csv.reader(f)
    for _row in _raw:
        if _row != []:
            YOUTUBE.append(_row)
    f.close()

with open("itch.csv", "r", encoding="utf-8") as f:
    _raw = csv.reader(f)
    for _row in _raw:
        if _row != []:
            ITCH.append(_row)
    f.close()

with open("unsplash.csv", "r", encoding="utf-8") as f:
    _raw = csv.reader(f)
    for _row in _raw:
        if _row != []:
            UNSPLASH.append(_row)
    f.close()

with open("updated.txt", "r", encoding="utf-8") as f:
    DATE = f.read()
    f.close()


# License header & Version check
print("""Pixel  Copyright (C) 2023  Foxie EdianiaK a.k.a. F_TEK
This program comes with ABSOLUTELY NO WARRANTY. This is free software,
and you are welcome to redistribute it under certain conditions.
For more details refer to the LICENSE file in the GitHub repository.""")

print("\n" * 4)


# Sets up alive bars
config_handler.set_global(spinner="circles",
                          bar="checks",
                          spinner_length=3)


# Global functions
async def save():
    with alive_bar(5, title="Saving", length=4) as bar:
        with open("github.csv", "w", encoding="utf-8") as f:
            _wrt = csv.writer(f)
            _wrt.writerows(GITHUB)
            f.close()
            print("Saved github.csv")
            bar()
        with open("youtube.csv", "w", encoding="utf-8") as f:
            _wrt = csv.writer(f)
            _wrt.writerows(YOUTUBE)
            f.close()
            print("Saved youtube.csv")
            bar()
        with open("itch.csv", "w", encoding="utf-8") as f:
            _wrt = csv.writer(f)
            _wrt.writerows(ITCH)
            f.close()
            print("Saved itch.csv")
            bar()
        with open("unsplash.csv", "w", encoding="utf-8") as f:
            _wrt = csv.writer(f)
            _wrt.writerows(UNSPLASH)
            f.close()
            print("Saved unsplash.csv")
            bar()
        with open("updated.txt", "w", encoding="utf-8") as f:
            f.write(DATE)
            f.close()
            print("Saved updated.txt")
            bar()
    print("Saved!")


async def clean(args: tuple) -> list:
    arg = ",".join(args)
    arg = arg.split(",")
    return arg


# Log in event
@bot.event
async def on_ready():
    global DATE
    print(f"\n~ ~ ~ Logged in as {bot.user} ~ ~ ~")

    _now = str(datetime.now())[:10]
    if DATE != _now:
        DATE = _now
        await check(None)


# Dev commands
@bot.command()
async def ping(ctx: commands.Context):
    print("Ping - Pong!")
    await ctx.channel.send("Pong!")


@bot.command()
async def echo(ctx: commands.Context, *args):
    arg = clean(args)
    print(f"Echo: {arg}")
    await ctx.channel.send(f'"{str(arg)}"')


# Config commands
@bot.command()
@commands.is_owner()
async def git(ctx: commands.Context, *args):
    arg = await clean(args)

    if arg == [""]:
        await ctx.channel.send("""**p.git ADD/DEL/LIST *ARGS***
- ADD - REPO (CHANNEL) (ROLE)
- DEL - REPO
- LIST""")
    else:
        act = arg[0]
        arg = arg[1:]
        _con = True

        if act == "add" or act == "ADD":
            if arg == []:
                _con = False
                await ctx.channel.send("ERROR: REPO required")
            if len(arg) > 3:
                _con = False
                await ctx.channel.send("ERROR: Too many positional arguments "
                                       + "given")

            if _con:
                _repo = ""
                _channel = ""
                _role = ""
                for i in arg:
                    if i[1] == "#":
                        _channel = i[2:-1]
                    elif i[1] == "@":
                        if i[2] == "&":
                            _role = i[3:-1]
                        else:
                            _con = False
                            await ctx.channel.send("ERROR: Expected ROLE, got "
                                                   + "USER")
                    else:
                        _repo = i

                if _channel == "":
                    _channel = ctx.channel.id

                if _con:
                    print(f"Addded {_repo} to GITHUB")
                    GITHUB.append([_repo, "", _channel, _role])
                    await save()
                    await ctx.channel.send(f"Addded {_repo} to GITHUB")
        elif act == "del" or act == "DEL":
            if arg == []:
                _con = False
                await ctx.channel.send("ERROR: REPO required")
            if len(arg) > 1:
                _con = False
                await ctx.channel.send("ERROR: Too many positional arguments "
                                       + "given")
            if _con:
                for i in range(0, len(GITHUB)):
                    j = GITHUB[i]
                    if j[0] == arg[0]:
                        print(f"Removed {arg[0]} from GITHUB")
                        GITHUB.pop(i)
                        await ctx.channel.send(f"Removed {arg[0]} from GITHUB")
            await save()
        elif act == "list" or act == "LIST":
            print("Reading GITHUB")
            await ctx.channel.send(str(GITHUB))
        else:
            print("ERROR: Unknown p.git subcommand")
            print(act, arg)
            await ctx.channel.send("ERROR: Unknown p.git subcommand")


@bot.command()
@commands.is_owner()
async def yt(ctx: commands.Context, *args):
    arg = await clean(args)

    if arg == [""]:
        await ctx.channel.send("""**p.yt ADD/DEL/LIST *ARGS***
- ADD - ID (CHANNEL) (MESSAGE) (ROLE)
- DEL - ID
- LIST""")
    else:
        act = arg[0]
        arg = arg[1:]
        _con = True

        if act == "add" or act == "ADD":
            if arg == []:
                _con = False
                await ctx.channel.send("ERROR: ID required")
            if len(arg) > 4:
                _con = False
                await ctx.channel.send("ERROR: Too many positional arguments "
                                       + "given")

            if _con:
                _id = ""
                _channel = ""
                _role = ""
                _msg = ""
                for i in arg:
                    if i[1] == "#":
                        _channel = i[2:-1]
                    elif i[1] == "@":
                        if i[2] == "&":
                            _role = i[3:-1]
                        else:
                            _con = False
                            await ctx.channel.send("ERROR: Expected ROLE, got "
                                                   + "USER")
                    else:
                        if _id == "":
                            _id = i
                        else:
                            _msg = i

                if _channel == "":
                    _channel = ctx.channel.id

                if _con:
                    print(f"Added {_id} to YOUTUBE")
                    YOUTUBE.append([_id, "", _channel, _msg, _role])
                    await save()
                    await ctx.channel.send(f"Added {_id} to YOUTUBE")
        elif act == "del" or act == "DEL":
            if arg == []:
                _con = False
                await ctx.channel.send("ERROR: ID required")
            if len(arg) > 1:
                _con = False
                await ctx.channel.send("ERROR: Too many positional arguments "
                                       + "given")
            if _con:
                for i in range(0, len(YOUTUBE)):
                    j = YOUTUBE[i]
                    if j[0] == arg[0]:
                        print(f"Removed {arg[0]} from YOUTUBE")
                        YOUTUBE.pop(i)
                        await ctx.channel.send(f"Removed {arg[0]} "
                                               + "from YOUTUBE")
            await save()
        elif act == "list" or act == "LIST":
            print("Reading YOUTUBE")
            await ctx.channel.send(str(YOUTUBE))
        else:
            print("ERROR: Unknown p.yt subcommand")
            print(act, arg)
            await ctx.channel.send("ERROR: Unknown p.yt subcommand")


@bot.command()
@commands.is_owner()
async def itch(ctx: commands.Context, *args):
    arg = await clean(args)

    if arg == [""]:
        await ctx.channel.send("""**p.itch ADD/DEL/LIST *ARGS***
- ADD - GAME (CHANNEL) (MESSAGE) (ROLE)
- DEL - GAME
- LIST""")
    else:
        act = arg[0]
        arg = arg[1:]
        _con = True

        if act == "add" or act == "ADD":
            if arg == []:
                _con = False
                await ctx.channel.send("ERROR: GAME required")
            if len(arg) > 3:
                _con = False
                await ctx.channel.send("ERROR: Too many positional arguments "
                                       + "given")

            if _con:
                _game = ""
                _channel = ""
                _role = ""
                for i in arg:
                    if i[1] == "#":
                        _channel = i[2:-1]
                    elif i[1] == "@":
                        if i[2] == "&":
                            _role = i[3:-1]
                        else:
                            _con = False
                            await ctx.channel.send("ERROR: Expected ROLE, got "
                                                   + "USER")
                    else:
                        _game = i

                if _channel == "":
                    _channel = ctx.channel.id

                if _con:
                    print(f"Added {_game} to ITCH")
                    ITCH.append([_game, "", _channel, _role])
                    await save()
                    await ctx.channel.send(f"Added {_game} to ITCH")
        elif act == "del" or act == "DEL":
            if arg == []:
                _con = False
                await ctx.channel.send("ERROR: GAME required")
            if len(arg) > 1:
                _con = False
                await ctx.channel.send("ERROR: Too many positional arguments "
                                       + "given")
            if _con:
                for i in range(0, len(ITCH)):
                    j = ITCH[i]
                    if j[0] == arg[0]:
                        print(f"Removed {arg[0]} from ITCH")
                        ITCH.pop(i)
                        await ctx.channel.send(f"Removed {arg[0]} from ITCH")
            await save()
        elif act == "list" or act == "LIST":
            print("Reading ITCH")
            await ctx.channel.send(str(ITCH))
        else:
            print("ERROR: Unknown p.itch subcommand")
            print(act, arg)
            await ctx.channel.send("ERROR: Unknown p.itch subcommand")


@bot.command()
@commands.is_owner()
async def us(ctx: commands.Context, *args):
    arg = await clean(args)

    if arg == [""]:
        await ctx.channel.send("""**p.us ADD/DEL/LIST *ARGS***
- ADD - USER (CHANNEL) (ROLE)
- DEL - USER
- LIST""")
    else:
        act = arg[0]
        arg = arg[1:]
        _con = True

        if act == "add" or act == "ADD":
            if arg == []:
                _con = False
                await ctx.channel.send("ERROR: USER required")
            if len(arg) > 3:
                _con = False
                await ctx.channel.send("ERROR: Too many positional arguments "
                                       + "given")

            if _con:
                _user = ""
                _channel = ""
                _role = ""
                for i in arg:
                    if i[1] == "#":
                        _channel = i[2:-1]
                    elif i[1] == "@":
                        if i[2] == "&":
                            _role = i[3:-1]
                        else:
                            _con = False
                            await ctx.channel.send("ERROR: Expected ROLE, got "
                                                   + "USER")
                    else:
                        _user = i

                if _channel == "":
                    _channel = ctx.channel.id

                if _con:
                    print(f"Added {_user} to UNSPLASH")
                    UNSPLASH.append([_user, "", _channel, _role])
                    await save()
                    await ctx.channel.send(f"Added {_user} to UNSPLASH")
        elif act == "del" or act == "DEL":
            if arg == []:
                _con = False
                await ctx.channel.send("ERROR: USER required")
            if len(arg) > 1:
                _con = False
                await ctx.channel.send("ERROR: Too many positional arguments "
                                       + "given")
            if _con:
                for i in range(0, len(UNSPLASH)):
                    j = UNSPLASH[i]
                    if j[0] == arg[0]:
                        print(f"Removed {arg[0]} from UNSPLASH")
                        UNSPLASH.pop(i)
                        await ctx.channel.send(f"Removed {arg[0]} "
                                               + "from UNSPLASH")
            await save()
        elif act == "list" or act == "LIST":
            print("Reading UNSPLASH")
            await ctx.channel.send(str(UNSPLASH))
        else:
            print("ERROR: Unknown p.us subcommand")
            print(act, arg)
            await ctx.channel.send("ERROR: Unknown p.us subcommand")


# Check command
@bot.command()
@commands.is_owner()
async def check(ctx: commands.Context, *args):
    print("\nChecking...")

    if len(GITHUB) < 3:
        _bar_len = 3
    else:
        _bar_len = len(GITHUB)

    with alive_bar(len(GITHUB), title="GITHUB", length=_bar_len) as bar:
        for i in range(0, len(GITHUB)):
            j = GITHUB[i]
            _stat = f"Checked {j[0]} repo"
            try:
                gh = requests.get("https://api.github.com/repos/"
                                  + f"{j[0]}/releases")
            except requests.exceptions.ConnectionError:
                _stat = f"ERROR: Couldn't find {j[0]} repo"
            else:
                if gh.status_code == 200:
                    gh = json.loads(gh.text)
                    chk = gh[0]["name"]
                    url = f"https://github.com/{j[0]}/releases/latest"

                    if j[1] == "":
                        GITHUB[i][1] = chk
                    elif chk != j[1]:
                        GITHUB[i][1] = chk

                        ctx = bot.get_channel(int(j[2]))

                        msg = f"**{j[0].upper().split('/')[1]}**"
                        msg += f"\nNew version ({chk}) available!"
                        msg += f"\nGet it here:"
                        msg += f"\n{url}"

                        if j[3] != "":
                            msg += f"\n<@&{j[3]}>"

                        await ctx.send(msg)
                        _stat = f"Announced {j[0]} repo update"
                else:
                    _stat = f"ERROR: Couldn't find {j[0]} repo"
            print(_stat)
            bar()

    if len(YOUTUBE) < 3:
        _bar_len = 3
    else:
        _bar_len = len(YOUTUBE)

    with alive_bar(len(YOUTUBE),
                   title="YOUTUBE",
                   length=_bar_len) as bar:
        for i in range(0, len(YOUTUBE)):
            j = YOUTUBE[i]
            _stat = f"Checked channel #{j[0]}"
            try:
                yt = requests.get("https://www.googleapis.com/youtube/v3/"
                                  + f"search?part=snippet&channelId={j[0]}"
                                  + "&maxResults=1&order=date&type=video"
                                  + f"&key={TOKENS['yt']}")
            except requests.exceptions.ConnectionError:
                _stat = f"ERROR: Couldn't find channel #{j[0]} data"
            else:
                if yt.status_code == 200:
                    yt = json.loads(yt.text)
                    chk = yt["items"][0]["snippet"]["title"]
                    name = yt["items"][0]["snippet"]["channelTitle"]
                    url = f"https://youtu.be/{yt['items'][0]['id']['videoId']}"
                    img = yt["items"][0]["snippet"]["thumbnails"]["high"]["url"]

                    if j[1] == "":
                        YOUTUBE[i][1] = chk
                    elif chk != j[1]:
                        YOUTUBE[i][1] = chk

                        ctx = bot.get_channel(int(j[2]))

                        msg = discord.Embed(title=f"{name} - {chk}",
                                            description=f"{j[3]}",
                                            url=url)
                        msg.set_image(url=img)

                        await ctx.send(embed=msg)

                        if j[4] != "":
                            await ctx.send(f"<@&{j[4]}>")

                        _stat = f"Announced channel #{j[0]} update"
            print(_stat)
            bar()

    if len(ITCH) < 3:
        _bar_len = 3
    else:
        _bar_len = len(ITCH)

    with alive_bar(len(ITCH), title="ITCH", length=_bar_len) as bar:
        for i in range(0, len(ITCH)):
            j = ITCH[i]
            try:
                itch = requests.get(TOKENS["itch"])
            except requests.exceptions.ConnectionError:
                _stat = "ERROR: Couldn't get json"
            else:
                if itch.status_code == 200:
                    itch = json.loads(itch.text)
                    chk = itch[j[0]][0]
                    cls = itch[j[0]][1]
                    url = f"https://edianiak.itch.io/{j[0]}"
                    img = itch[j[0]][2]
                    name = itch[j[0]][3]
                    _stat = f"Checked {j[0]} {cls}"

                    if j[1] == "":
                        ITCH[i][1] = chk
                    elif chk != j[1]:
                        ITCH[i][1] = chk

                        ctx = bot.get_channel(int(j[2]))

                        msg = discord.Embed(title=name,
                                            description=f"This {cls} just "
                                            + "got updated!",
                                            url=url)
                        msg.set_image(url=img)

                        await ctx.send(embed=msg)

                        if j[3] != "":
                            await ctx.send(f"<@&{j[3]}>")

                        _stat = f"Announced {j[0]} {cls} update"
                else:
                    _stat = "ERROR: Couldn't get json"
            print(_stat)
            bar()

    if len(UNSPLASH) < 3:
        _bar_len = 3
    else:
        _bar_len = len(UNSPLASH)

    with alive_bar(len(UNSPLASH),
                   title="UNSPLASH",
                   length=_bar_len) as bar:
        for i in range(0, len(UNSPLASH)):
            j = UNSPLASH[i]
            _stat = f"Checked photos by {j[0]}"
            try:
                us = requests.get(f"https://api.unsplash.com/users/{j[0]}"
                                  + f"/photos?client_id={TOKENS['us']}"
                                  + "&per_page=1")
            except requests.exceptions.ConnectionError:
                _stat = f"ERROR: Couldn't load {j[0]}'s photos"
            else:
                if us.status_code == 200:
                    us = json.loads(us.text)
                    chk = us[0]["id"]
                    usr = us[0]["user"]["username"]
                    author = us[0]["user"]["name"]
                    img = us[0]["urls"]["regular"]
                    url = us[0]["links"]["html"]
                    pp = us[0]["user"]["profile_image"]["large"]

                    if j[1] == "":
                        UNSPLASH[i][1] = chk
                    elif chk != j[1]:
                        UNSPLASH[i][1] = chk

                        ctx = bot.get_channel(int(j[2]))

                        msg = discord.Embed(title="New photo by "
                                            + usr.upper(),
                                            url=url)
                        msg.set_image(url=img)
                        msg.set_footer(text=f"Photo by {author} on Unsplash",
                                       icon_url=pp)

                        await ctx.send(embed=msg)

                        if j[3] != "":
                            await ctx.send(f"<@&{j[3]}>")

                        _stat = f"Announced new photo by {j[0]}"
                else:
                    _stat = f"ERROR: Couldn't load {j[0]}'s photos"
            print(_stat)
            bar()

    print("Check complete!\n")

    await save()


# Starts bot
bot.run(TOKENS["dis"])
