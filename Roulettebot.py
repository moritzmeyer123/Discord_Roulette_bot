import discord
from discord.ext import commands
import random
import os

client = commands.Bot(command_prefix = '!')
client.remove_command('help')

def is_file_empty(file_path):
    """ Check if file is empty by confirming if its size is 0 bytes"""
    # Check if file exist and it is empty
    return  os.path.exists(file_path) and not os.stat(file_path).st_size == 0

def getCreditAmount(author):
    try:
        f = open("creditfile.txt", "r")
    except:
        f = open("creditfile.txt", "x")
        return 0
    sum = 0
    try:
        for x in f:
            if x.split(' ')[1] == str(author):
                sum += int(x.split(' ')[2])
        f.close
        return sum
    except:
        f.close
        return 0

#Einloggen
@client.event
async def on_ready():
    print("Der Bot ist online.")


@client.command(pass_context = True)
async def help(ctx):
    await ctx.message.channel.purge(limit=1)
    embedVar = discord.Embed(title = "Roulettebot Commands", color = 0x7289da)
    embedVar.add_field(name = "Wetten", value = "!roulette BID AMOUNT, BID = black | red | number[0;36]", inline = False)
    embedVar.add_field(name = "Erfahre deinen Geldstatus", value = "!credits", inline = True)
    embedVar.add_field(name = "50 neue Credits", value = "!getcredits", inline = True)
    await ctx.send(embed = embedVar, delete_after = 10.0)


@client.command()
async def getcredits(ctx):
    await ctx.message.channel.purge(limit=1)
    print("CTX: " + str(ctx.message))
    #amount = ctx.content.split(' ')[1]
    amount = 50
    if not is_file_empty('creditfile.txt'):
        f = open("creditfile.txt", "a")
        #Date[0] + Author[1] + Amount[2]
        f.write(str(ctx.message.created_at).split(' ')[0] + " " + str(ctx.message.author) + " " + str(amount) + "\n")
        await ctx.send('Dir wurden 50 Credits gutgeschrieben!', delete_after = 10.0)
        f.close()
    else:
        #Finde letzten Eintrag des Senders
        f = open("creditfile.txt", "r")
        index = 0
        letzerEintrag = -1
        for x in f:
            if str(ctx.message.author) == x.split(' ')[1]:
                letzerEintrag = index
            index += 1
        #Gucke nach dem Datum
        f.close()
        if not letzerEintrag == -1:
            f = open("creditfile.txt", "r")
            index = 0
            for x in f:
                if letzerEintrag == index:
                    date = x.split(' ')[0]
                index += 1
            f.close()
            if str(ctx.message.created_at).split(' ')[0] == date:
                await ctx.send("Du hast heute bereits neue Credits angefordert! Schaue morgen wieder vorbei!", delete_after = 10.0)
            else:
                f = open("creditfile.txt", "a")
                f.write(str(ctx.message.created_at).split(' ')[0] + " " + str(ctx.message.message.author) + " " + str(amount) + "\n")
                await ctx.send('Dir wurden 50 Credits gutgeschrieben!', delete_after = 10.0)
                f.close()
        else:
            f = open("creditfile.txt", "a")
            f.write(str(ctx.message.created_at).split(' ')[0] + " " + str(ctx.message.author) + " " + str(amount) + "\n")
            await ctx.send('Dir wurden 50 Credits gutgeschrieben!', delete_after = 10.0)
            f.close()

@client.command()
async def credits(ctx):
    await ctx.message.channel.purge(limit=1)
    credits = getCreditAmount(ctx.author)
    await ctx.send('Du hast ' + str(credits) + ' Credits', delete_after=10.0)

@client.command()
async def roulette(ctx):
    await ctx.message.channel.purge(limit=1)
    bid = ctx.message.content.split(' ')[1]
    amount = ctx.message.content.split(' ')[2]
    #Hat der Spieler noch genügend Credits?
    if getCreditAmount(ctx.author) < int(amount):
        await ctx.send('Du hast zu wenig Credits.', delete_after = 10.0)
    else:    
        #!roulette[0] BID[1] AMOUNT[2]
        #bid_param = -1 für black
        #bid_param = -2 für red
        #bid_param = -3 für Ungültige Eingabe
        #bid_param = [0;36] für einzelne Zahl
        if bid.lower() == "black":
            bid_param = -1
        elif bid.lower() == "red":
            bid_param = -2
        else:
            try:
                bid_param = int(bid)
            except:
                bid_param = -3
        if bid_param == -3 or bid_param > 36:
            await ctx.send('Ungültige Eingabe', delete_after = 10.0)
            return
        result = random.randint(0,36)
        won = False
        if bid_param == -1:
            #won = result % 2 == 0 and not result == 0
            black_numbers = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]
            if result in black_numbers:
                won = True
        elif bid_param == -2:
            #won = result % 2 == 1
            red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
            if result in red_numbers:
                won = True
        else:
            won = result == bid_param
        f = open("creditfile.txt", "a")
        if won and bid_param >= 0:
            await ctx.send("$$$ Du hast gewonnen $$$", delete_after = 10.0)
            amount = int(amount) * 34
            f.write(str(ctx.message.created_at).split(' ')[0] + " " + str(ctx.message.author) + " " + str(int(amount) * 34) + "\n")
            await ctx.send("Die Zahl war " + str(result), delete_after = 10.0)
        elif won and (bid_param == -1 or bid_param == -2):
            f.write(str(ctx.message.created_at).split(' ')[0] + " " + str(ctx.message.author) + " " + str(amount) + "\n")
            await ctx.send("$$$ Du hast gewonnen $$$", delete_after = 10.0)
            await ctx.send("Die Zahl war " + str(result), delete_after = 10.0)
        else:
            f.write(str(ctx.message.created_at).split(' ')[0] + " " + str(ctx.message.author) + " -" + amount + "\n")
            await ctx.send("Leider verloren :(", delete_after = 10.0)
            await ctx.send("Die Zahl war " + str(result), delete_after = 10.0)


client.run("NzEyNjgwNzY2MzAzMTA5MTgw.XsVFrw.Il7vOjwKn0zfKMBR1QqUoGdFgAo")