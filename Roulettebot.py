import discord
import random
import os

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

class MyClient(discord.Client):
    #Einloggen
    async def on_ready(self):
        print("Der Bot ist online.")

    #Nachrichtempfang
    async def on_message(self, message):
        #print("Nachricht von " + str(message.author) + " enthält " + message.content)
        if message.author == client.user:
            return
            
        if message.content.startswith("!help"):
            embedVar = discord.Embed(title = "Roulettebot Commands", color = 0x7289da)
            embedVar.add_field(name = "Wetten", value = "!roulette BID AMOUNT, BID = black | red | number[0;36]", inline = False)
            embedVar.add_field(name = "Erfahre deinen Geldstatus", value = "!credits", inline = True)
            embedVar.add_field(name = "50 neue Credits", value = "!getcredits", inline = True)
            await message.channel.send(embed = embedVar)
            

        if message.content.startswith("!getcredits"):
            #amount = message.content.split(' ')[1]
            amount = 50
            if not is_file_empty('creditfile.txt'):
                f = open("creditfile.txt", "a")
                #Date[0] + Author[1] + Amount[2]
                f.write(str(message.created_at).split(' ')[0] + " " + str(message.author) + " " + str(amount) + "\n")
                await message.channel.send('Dir wurden 50 Credits gutgeschrieben!')
                f.close()
            else:
                #Finde letzten Eintrag des Senders
                f = open("creditfile.txt", "r")
                index = 0
                letzerEintrag = -1
                for x in f:
                    if str(message.author) == x.split(' ')[1]:
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
                    if str(message.created_at).split(' ')[0] == date:
                        await message.channel.send("Du hast heute bereits neue Credits angefordert! Schaue morgen wieder vorbei!")
                    else:
                        f = open("creditfile.txt", "a")
                        f.write(str(message.created_at).split(' ')[0] + " " + str(message.author) + " " + str(amount) + "\n")
                        await message.channel.send('Dir wurden 50 Credits gutgeschrieben!')
                        f.close()
                else:
                    f = open("creditfile.txt", "a")
                    f.write(str(message.created_at).split(' ')[0] + " " + str(message.author) + " " + str(amount) + "\n")
                    await message.channel.send('Dir wurden 50 Credits gutgeschrieben!')
                    f.close()
                
        if message.content.startswith("!credits"):
           credits = getCreditAmount(message.author)
           await message.channel.send('Du hast ' + str(credits) + ' Credits')


        if message.content.startswith("!roulette"):
            bid = message.content.split(' ')[1]
            amount = message.content.split(' ')[2]
            #Hat der Spieler noch genügend Credits?
            if getCreditAmount(message.author) < int(amount):
                await message.channel.send('Du hast zu wenig Credits.')
            else:    
                #!roulette[0] BID[1] AMOUNT[2]
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
                    await message.channel.send('Ungültige Eingabe')
                    return
                result = random.randint(0,36)
                if bid_param == -1:
                    won = result % 2 == 0 and not result == 0
                elif bid_param == -2:
                    won = result % 2 == 1
                else:
                    won = result == bid_param
                f = open("creditfile.txt", "a")
                if won and bid_param == -3:
                    await message.channel.send("$$$ Du hast gewonnen $$$")
                    f.write(str(message.created_at).split(' ')[0] + " " + str(message.author) + " " + str(amount) + "\n")
                    await message.channel.send("Die Zahl war " + str(result))
                elif won and (bid_param == -1 or bid_param == -2):
                    f.write(str(message.created_at).split(' ')[0] + " " + str(message.author) + " " + str(amount) + "\n")
                    await message.channel.send("$$$ Du hast gewonnen $$$")
                    await message.channel.send("Die Zahl war " + str(result))
                else:
                    f.write(str(message.created_at).split(' ')[0] + " " + str(message.author) + " -" + amount + "\n")
                    await message.channel.send("Leider verloren :(")
                    await message.channel.send("Die Zahl war " + str(result))

client = MyClient()
client.run("NzEyNjgwNzY2MzAzMTA5MTgw.XsVFrw.aZnIk0JKXFyOgzvsP9UKRa9SFYA")

 
