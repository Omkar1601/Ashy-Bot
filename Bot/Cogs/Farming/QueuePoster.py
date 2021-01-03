import discord
from discord.ext import commands
import re
import random
import datetime
from Constants import Constants


def Cards(self, text):
    text = text.lower()

    if 'cards' in text:
        c_catch = re.search('cards', text)
        c_start = c_catch.start()
        c_end = c_catch.end()
        return c_start, c_end

    elif 'card' in text:
        c_catch = re.search('cards', text)
        c_start = c_catch.start()
        c_end = c_catch.end()
        return c_start, c_end

def Speedo(self, text):
    if 'slow' in text:
        s_catch = re.search('slow', text)
        s_start = s_catch.start()
        s_end = s_catch.end()
        return s_start, s_end, 0
    else:
        n_catch = re.search('normal', text)
        n_start = n_catch.start()
        n_end = n_catch.end()
        return n_start, n_end, 1

def Loc(self, text):
    if "loc" in text:
            loc_catch= re.search("loc", text)
            l_start= loc_catch.start()
            l_end= loc_catch.end()
            return l_start, l_end
    elif "location" in text:
            loc_catch= re.search("location", text)
            l_start= loc_catch.start()
            l_end= loc_catch.end()
            return l_start, l_end

def LocCatch(self, text):
    for index, c in enumerate(text):
            if c.isdigit():                
                    loc_start= index
                    if loc_start:
                            for index2, c2 in enumerate(text[loc_start:]):
                                    if c2.isalpha():
                                            loc_end= index2
                                            floor= text[loc_start:loc_end]
                                            return floor
                                    else:
                                            floor= text[loc_start:]
                                            return floor
                    else:
                            floor= "Not Specified"
                            return floor

def PriceCalc(self, card_amount, card_location, speed_flag):
    rate_floor = int(card_location.strip())
    spchar= re.compile(r"[/\|:-]")
    sp_catch= spchar.search(card_location)

    if sp_catch != None:
        spchar_index= sp_catch.start()
        rate_floor= int(card_location[:spchar_index])

    if speed_flag == 0:
        if rate_floor <30:
            charge_rate = 80
        else:
            charge_rate = 70
    
    if speed_flag == 1:
        if rate_floor <= 50:
            charge_rate = 125
        
        elif rate_floor >= 51 and rate_floor <=55:
            charge_rate = 110

        else:
            charge_rate = 150 

    card_amount = int(card_amount.strip())
    return card_amount * charge_rate


class QueuePoster(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        queue_channel = Constants.QUEUE_CHANNEL

        if(message.channel.id != Constants.ORDER_CHANNEL):
            return

        else:
            if(message.author == self.bot.user):
                return

            flag = 0
            text = message.content
            text = text.replace('.', ' ')
            text = text.replace(',', ' ')
            text = text.replace('(', ' ')
            text = text.replace(')', ' ')

            card_start, card_end = Cards(self, text)
            
            for index, c in enumerate(text[:card_start]):
                if c.isdigit():
                    amount_start = index
                    flag+=1
                    break
            
            card_amount = text[amount_start:card_start]
            card_name = ""
            card_location = "Not Specified"

            text2 = text.lower()
            speed_end = 0
            speed_flag = 1
            speed_flag2 = ''

            if "normal" in text2 or 'slow' in text2:
                speed_start, speed_end, speed_flag = Speedo(self, text2)
                card_name = text[card_end:speed_start]
                flag+=1

            if "loc" in text2[speed_end:] or "location" in text2[speed_end:]:
                loc_start, loc_end = Loc(self, text2)

                if loc_start != None and loc_end != None:
                    card_location= LocCatch(self, text2[loc_end:])

            farming_cost = 0

            if speed_flag == 0:
                speed_flag2 = 'Slow'
            
            else:
                speed_flag2 = 'Normal'

            
            if card_location == 'Not Specified':
                farming_cost = "Couldn't calculate 'cos card location isn't specified."
            
            else:
                farming_cost = PriceCalc(self, card_amount, card_location, speed_flag)

            footers= ["Owe Ashy my life for resurrecting me again!", "So ladies n' gentlemen, I got the medicine so you should keep ya eyes on the ball", "Believe me, waifus > stats!", "Everyday is my birthday!", "you love me... you love me not. you love me...","Do try out the other bots too.", "Ashy initially wanted me to be a hentai-ish bot *sad moans*", "Mark's looking for loli emotes, help when?", "te amo mami!", "We totally don't sell hentai here ;)", "Fun Fact: I Love You!", "Do say a 'hi' to our beloved traps here", "Suji... we miss you love :(", "omg wtf ily!", "Simp a sugar daddy when?", "Feel free to ping Ashy to remind them that they're a cute!", "Ha-ha-how you like that", "Unrequited love? I feel you"]
            rand_foot= random.choice(footers)

            embed= discord.Embed(title= "__**ORDER**__", timestamp= datetime.datetime.now(), colour= discord.Colour.blue())
            embed.set_thumbnail(url= self.bot.user.avatar_url)
            embed.add_field(name = "**Buyer:** ", value = f"<@{message.author.id}>", inline = False)
            embed.add_field(name = "**Card Name:** ", value = str(card_name), inline = False) 
            embed.add_field(name = "**Location:** ", value = str(card_location), inline = False)
            embed.add_field(name = "**Card Amount:** ", value = str(card_amount), inline = False)
            embed.add_field(name = "**Farm Type:** ", value = str(speed_flag2), inline = False)
            embed.add_field(name = "**Price:** ", value = str(farming_cost), inline = False)
            embed.set_footer(text= rand_foot)

            if flag == 1:
                msg = await queue_channel.send(embed = embed)
                await msg.add_reaction(Constants.REACTION_EMOTE)
                await message.add_reaction(Constants.VALIDATION_EMOTE)


def setup(bot):
    bot.add_cog(QueuePoster(bot))

            
                    
            







            


