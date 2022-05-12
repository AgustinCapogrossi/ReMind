from discord import *
from discord.ext import commands
from datetime import *
import time
import asyncio
bot = commands.Bot(command_prefix='<', description='This is a reminders oriented bot.')

# python src/index.py

clan_list={ 
                "EMK" : "Expansive Multiversal Kingdom",
                "CC"  : "Crusher Core",
                "TKO" : "Total Knock-Out",
                "MIH" : "Made in Heaven",
                "TWOH": "The World Over Heaven",
                "DC"  : "Dark Clouds",
                "COL" : "Children of Light",
                "FF"  : "Freeza Force",
                "TA"  : "Tāresu-Army",
                "G"   : "Guest",
                "GW"  : "Generational Warriors",
                "PCE" : "Planetary Covent Enforcers"
              }


@bot.command()
async def stats(ctx):
    embed = Embed(title=f"{ctx.guild.name}",description="Single purpose bot planned to set reminders", timestamp= datetime.utcnow())
    await ctx.send(embed=embed)

@bot.command()
async def remind_me(ctx, timer :str, msg: str, dm :str):
    """Creates a reminder for the user who invokes the method.

    Args:
        ctx (_type_): Server context.
        timer (str): Amount of time you want to wait before you get a reminder.
        msg (str): Message you want to be reminded of.
        dm (str): Whether you want to receive the reminder via dm
    """
    remind_role = utils.get(ctx.guild.roles, name ="Reminder")
    time_convert = {"s": 1 , "m" : 60, "h": "3600", "d": 86400}
    rmnder = (int (timer[:-1]) * (time_convert[timer[-1]]))
    await ctx.author.add_roles(remind_role)
    await ctx.reply("You were assigned the **Reminder** role. **DO NOT REMOVE IT** ")
    await asyncio.sleep(int(rmnder))
    await ctx.author.remove_roles(remind_role)
    if (dm=="yes" or dm == "Yes" or dm == "YES"):
        await ctx.author.send(f"Here's the reminder you set on {datetime.utcnow()}: {msg}")
    else:
        await ctx.reply(f"Here's the reminder you set on {datetime.utcnow()}: {msg}")

@bot.command()
@commands.has_any_role('Omni King','Grand Priest','Angel','God Of Destruction','Grand Kai','Kai')
async def clan(ctx, user: User, utag: str):
    name = str(user.display_name)
    tag = ""
    new_name= ""
    serverID = ctx.message.guild.id
    guild = bot.get_guild(serverID)
    roles = guild.roles
    uroles = user.roles

    if utag not in clan_list:
        await ctx.send("Incorrect tag.")
    elif "#" in name:
        await ctx.send("The username isn't in the right format.")
    elif name[0] != "[":
        await ctx.send("The user doesn't have a tag.")
    else:
        for i in name:
            if i == "[":
                for j in name:
                    if j != "]":
                        tag = tag + j
                    else:
                        tag = tag +j
                        break

        for i in range(len(uroles)):
            for j in clan_list:
                if uroles[i].name == clan_list[j]:
                    await user.remove_roles(uroles[i])
        for i in clan_list:
            if i == utag:
                new_name = name.replace(tag,"["+utag+"]")
                for j in range(len(roles)):
                    if clan_list[i] == roles[j].name:
                        await user.add_roles(roles[j])
                        await user.edit(nick= new_name)
                        await ctx.send(f"{user.name}'s clan has been updated to **{roles[j].name}**")

# Events
@bot.event
async def on_ready():
    await bot.change_presence(status=Status.online, activity=Game('with the API'))
    print('My bot is ready')

@bot.event
async def on_disconnect():
    await bot.change_presence(status=Status.offline)
    print('My bot off')

bot.run('OTczOTQ4Njg0ODU1Mjg3ODE4.G5SgxN.pqFJtpesUrtkq6tbYXSL-Q4ipW69QsQzuoWB9Y')