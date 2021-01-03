import discord
from discord.ext import commands
import secrets
import re
import datetime 
import sqlite3
from Constants import Constants

class ProgressPoster(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction_channel = self.bot.get_channel(payload.channel_id)
        user = self.bot.get_user(payload.user_id)
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        message = await reaction_channel.fetch_message(payload.message_id)

        progress_channel = self.bot.get_channel(Constants.PROGRESS_CHANNEL)

        if reaction_channel.id == Constants.QUEUE_CHANNEL:
            for emote in message.reactions:
                if str(emote.emoji) == Constants.REACTION_EMOTE:
                    if user == self.bot.user:
                        return
                    
                    flag = True
                    farmer_role = discord.utils.get(message.guild.roles, id= Constants.FARMER_ID)
                    if farmer_role not in member.roles:
                        flag = False                        
                        return await message.remove_reaction(Constants.REACTION_EMOTE, user)

                    if flag:
                        buyer = message.embeds[0].fields[0].value
                        card = message.embeds[0].fields[1].value
                        location = message.embeds[0].fields[2].value
                        nos = message.embeds[0].fields[3].value
                        farm_type = message.embeds[0].fields[4].value 
                        price = message.embeds[0].fields[5].value
                        catch = re.search("[0-9]+", buyer)
                        ids = catch.start()
                        ide = catch.end()
                        buyer_id = buyer[ids:ide] 

                        footers = ["Owe Ashy my life for resurrecting me again!", "So ladies n' gentlemen, I got the medicine so you should keep ya eyes on the ball", "Believe me, waifus > stats!", "Everyday is my birthday!", "you love me... you love me not. you love me...","Do try out the other bots too.", "Ashy initially wanted me to be a hentai-ish bot *sad moans*", "Mark's looking for loli emotes, help when?", "te amo mami!", "We totally don't sell hentai here ;)", "Fun Fact: I Love You!", "Do say a 'hi' to our beloved traps here", "Suji... we miss you love :(", "omg wtf ily!", "Simp a sugar daddy when?", "Feel free to ping Ashy to remind them that they're a cute!", "Ha-ha-how you like that", "Unrequited love? I feel you"]
                        rand_foot = secrets.choice(footers)

                        farm_id = secrets.randbelow(10000)

                        embed= discord.Embed(title = f"__**Under Progress**__", timestamp = datetime.datetime.now(), colour = discord.Colour.blue())
                        embed.add_field(name = "**Order ID:** ", value = str(farm_id), inline = True)
                        embed.add_field(name = "**Card Name:** ", value = card, inline = False)
                        embed.set_thumbnail(url = user.avatar_url)
                        embed.add_field(name = "**Location:** ", value = location, inline = False)
                        embed.add_field(name = "**Card Amount:** ", value = nos, inline = False)
                        embed.add_field(name = "**Farm Type:** ", value = farm_type, inline = False)
                        embed.add_field(name = "**Price:** ", value = price, inline = False)
                        embed.set_footer(text = rand_foot)

                        msg = await progress_channel.send(f"**Buyer:** <@{buyer_id}> \n**Farmer:** <@{user.id}>", embed = embed)
                        await msg.add_reaction(Constants.REACTION_EMOTE)

                        
                        mydb = sqlite3.connect("farm.sqlite")
                        cursor = mydb.cursor()
                        cmd = "insert into FARM values(?, ?, ?, ?, ?, ?, ?, ?)"
                        val = (user.id, buyer_id, card, nos, location, price, farm_id, farm_type)
                        cursor.execute(cmd, val)

                        await message.delete()
                        mydb.commit()
                        cursor.close()
                        mydb.close()

def setup(bot):
    bot.add_cog(ProgressPoster(bot))


