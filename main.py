try:
    import asyncio
    import sys
    import os
    import time
    import datetime

    import json
    from functools import partial
    from keep_alive import keep_alive

    import random as rand

    from colorama import Fore, Back, Style, init

    init(autoreset=True)

    import fortnitepy
    from fortnitepy.ext import commands
    import BenBotAsync
    import aiohttp
    import requests

except ModuleNotFoundError as e:
    print(e)
    print(
        Fore.LIGHTYELLOW_EX
        + " • "
        + Fore.RESET
        + 'Failed to import 1 or more modules. Run "INSTALL PACKAGES.bat'
    )
    exit()

os.system("cls||clear")

intro = (
    Fore.LIGHTBLUE_EX
    + """ 
    GhoulFN, created by amesa#0001 and gummy bear
#6969
                                                                    
 """
)

print(intro)


def lenPartyMembers():
    members = client.party.members
    return len(members)


def warn(*args, **kwargs):
    pass


import warnings

warnings.warn = warn


def lenFriends():
    friends = client.friends
    return len(friends)


def getNewSkins():
    r = requests.get("https://benbotfn.tk/api/v1/files/added")

    response = r.json()

    cids = []

    for cid in [
        item for item in response if item.split("/")[-1].upper().startswith("CID_")
    ]:
        cids.append(cid.split("/")[-1].split(".")[0])

    return cids


def getNewEmotes():
    r = requests.get("https://benbotfn.tk/api/v1/files/added")

    response = r.json()

    eids = []

    for cid in [
        item for item in response if item.split("/")[-1].upper().startswith("EID_")
    ]:
        eids.append(cid.split("/")[-1].split(".")[0])

    return eids


def get_device_auth_details():
    if os.path.isfile("auths.json"):
        with open("auths.json", "r") as fp:
            return json.load(fp)
    else:
        with open("auths.json", "w+") as fp:
            json.dump({}, fp)
    return {}


def store_device_auth_details(email, details):
    existing = get_device_auth_details()
    existing[email] = details

    with open("auths.json", "w") as fp:
        json.dump(existing, fp)


with open("config.json") as f:
    try:
        data = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(
            Fore.LIGHTYELLOW_EX
            + " [ERROR] "
            + Fore.RESET
            + "There was an error in one of the bot's files! (config.json). If you have problems trying to fix it, contact support."
        )
        print(Fore.LIGHTYELLOW_EX + f"\n {e}")
        exit(1)


with open("config.json") as f:
    try:
        info = json.load(f)
    except json.decoder.JSONDecodeError as e:
        print(
            Fore.LIGHTYELLOW_EX
            + " [ERROR] "
            + Fore.RESET
            + "There was an error in one of the bot's files! (info.json) If you have problems trying to fix it, contact support."
        )
        print(Fore.LIGHTYELLOW_EX + f"\n {e}")
        exit(1)


def is_admin():
    async def predicate(ctx):
        return ctx.author.id in info["FullAccess"]

    return commands.check(predicate)


device_auth_details = get_device_auth_details().get(data["email"], {})

prefix = data["prefix"]

client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    auth=fortnitepy.AdvancedAuth(
        email=data["email"],
        password=data["password"],
        prompt_authorization_code=True,
        delete_existing_device_auths=True,
        **device_auth_details,
    ),
    platform=fortnitepy.Platform(data["platform"]),
)





@client.event
async def event_device_auth_generate(details, email):
    store_device_auth_details(email, details)


@client.event
async def event_ready():
    
    os.system("cls||clear")
    print(intro)
    print(
        Fore.LIGHTBLUE_EX
        + " • "
        + Fore.RESET
        + "Client is called "
        + Fore.LIGHTBLUE_EX
        + f"{client.user.display_name}"
    )

    member = client.party.me

    await member.edit_and_keep(
        partial(fortnitepy.ClientPartyMember.set_outfit, asset=data["cid"]),
        partial(fortnitepy.ClientPartyMember.set_backpack, asset=data["bid"]),
        partial(fortnitepy.ClientPartyMember.set_pickaxe, asset=data["pid"]),
        partial(
            fortnitepy.ClientPartyMember.set_banner,
            icon=data["banner"],
            color=data["banner_color"],
            season_level=data["level"],
        ),
        partial(
            fortnitepy.ClientPartyMember.set_battlepass_info,
            has_purchased=True,
            level=data["bp_tier"],
        ),
    )

    client.set_avatar(
        fortnitepy.Avatar(
            asset=data["avatar"], background_colors=["#ffffff", "#2E8B57", "#7FFF00"]
        )
    )


@client.event
async def event_party_invite(invite):
    if data["joinoninvite"].lower() == "true":
        try:
            await invite.accept()
            print(
                Fore.LIGHTBLUE_EX
                + " • "
                + Fore.RESET
                + "Accepted party invite from"
                + Fore.LIGHTBLUE_EX
                + f"{invite.sender.display_name}"
            )
        except Exception:
            pass
    elif data["joinoninvite"].lower() == "false":
        if invite.sender.id in info["FullAccess"]:
            await invite.accept()
            print(
                Fore.LIGHTBLUE_EX
                + " • "
                + Fore.RESET
                + "Accepted party invite from "
                + Fore.LIGHTBLUE_EX
                + f"{invite.sender.display_name}"
            )
        else:
            print(
                Fore.LIGHTBLUE_EX
                + " • "
                + Fore.RESET
                + "Never accepted party invite from "
                + Fore.LIGHTBLUE_EX
                + f"{invite.sender.display_name}"
            )


@client.event
async def event_friend_request(request):
    if data["friendaccept"].lower() == "true":
        try:
            await request.accept()
            print(
                f" • Accepted friend request from {request.display_name}"
                + Fore.LIGHTBLACK_EX
                + f" ({lenFriends()})"
            )
        except Exception:
            pass
    elif data["friendaccept"].lower() == "false":
        if request.id in info["FullAccess"]:
            try:
                await request.accept()
                print(
                    Fore.LIGHTBLUE_EX
                    + " • "
                    + Fore.RESET
                    + "Accepted friend request from "
                    + Fore.LIGHTBLUE_EX
                    + f"{request.display_name}"
                    + Fore.LIGHTBLACK_EX
                    + f" ({lenFriends()})"
                )
            except Exception:
                pass
        else:
            print(f" • Never accepted friend request from {request.display_name}")

banned = []

@client.event
async def event_party_message(message: fortnitepy.PartyMessage):
    if message.content == "" and client.party.me.leader:
        await message.author.kick()
        banned.append(message.author.id)
@client.event
async def event_party_member_confirm(confirmation: fortnitepy.PartyJoinConfirmation):
    if confirmation.user.id not in banned:
        await confirmation.accept()

banned = []

@client.event
async def event_party_message(message: fortnitepy.PartyMessage):
    if message.content == "Heyy :bruh)                                                                                                                                For your own bot:                                                                                                                                : Youtube: LupusLeaks                                                                                                                                - TikTok: LupusLeaks                                                                                                                                -Instagram: LupusLeaks                                                                                                                                -Discord: https://ezfn.net/discord"and client.party.me.leader:
        await message.author.kick()
        banned.append(message.author.id)

@client.event
async def event_party_member_confirm(confirmation: fortnitepy.PartyJoinConfirmation):
    if confirmation.user.id not in banned:
        await confirmation.accept()

@client.event
async def event_party_member_join(member: fortnitepy.PartyMember) -> None:
    
    await client.party.send(
        f" Hello, thank you for using our bot."
    )
    await client.party.me.set_emote(asset="EID_CandyDance")
    await asyncio.sleep(1.25)
    await client.party.me.clear_emote()
    await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)

@client.event
async def event_party_member_confirm(confirmation):
    if confirmation.user.id in client.blocked_users:
        await confirmation.reject()
    else:
        await confirmation.confirm()


@client.event
async def event_party_member_leave(member):
    
    await client.party.set_privacy(fortnitepy.PartyPrivacy.PUBLIC)
    if client.user.display_name != member.display_name:
        try:
            print(
                Fore.LIGHTYELLOW_EX
                + f" • {member.display_name}"
                + Fore.RESET
                + " has left the lobby."
                + Fore.LIGHTBLACK_EX
                + f" ({lenPartyMembers()})"
            )
        except fortnitepy.HTTPException:
            pass


@client.event
async def event_party_message(message):
    if message.author.id in info["FullAccess"]:
        name = Fore.LIGHTBLUE_EX + f"{message.author.display_name}"
    else:
        name = Fore.RESET + f"{message.author.display_name}"
    print(Fore.GREEN + " • [Party] " + f"{name}" + Fore.RESET + f": {message.content}")


@client.event
async def event_friend_message(message):
    if message.author.id in info["FullAccess"]:
        name = Fore.LIGHTMAGENTA_EX + f"{message.author.display_name}"
    else:
        name = Fore.RESET + f"{message.author.display_name}"
    print(
        Fore.LIGHTMAGENTA_EX
        + " • [Whisper] "
        + f"{name}"
        + Fore.RESET
        + f": {message.content}"
    )

    if message.content.upper().startswith("CID_"):
        await client.party.me.set_outfit(asset=message.content.upper())
        await message.reply(f"Skin set to: {message.content}")
    elif message.content.upper().startswith("BID_"):
        await client.party.me.set_backpack(asset=message.content.upper())
        await message.reply(f"Backpack set to: {message.content}")
    elif message.content.upper().startswith("EID_"):
        await client.party.me.set_emote(asset=message.content.upper())
        await message.reply(f"Emote set to: {message.content}")
    elif message.content.upper().startswith("PID_"):
        await client.party.me.set_pickaxe(asset=message.content.upper())
        await message.reply(f"Pickaxe set to: {message.content}")
    elif message.content.startswith("Playlist_"):
        try:
            await client.party.set_playlist(playlist=message.content)
            await message.reply(f"Playlist set to: {message.content}")
        except fortnitepy.Forbidden:
            await message.reply(
                f"I can not set gamemode because I am not party leader."
            )
    elif message.content.lower().startswith("prefix"):
        await message.reply(f"Current prefix: !")


@client.event
async def event_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"")
    elif isinstance(error, IndexError):
        pass
    elif isinstance(error, fortnitepy.HTTPException):
        pass
    elif isinstance(error, commands.CheckFailure):
        await ctx.send("")
    elif isinstance(error, TimeoutError):
        await ctx.send("You took too long to respond!")
    else:
        print(error)

@client.command()
async def hi(ctx):
    await ctx.send('Hello')
    
    
    
