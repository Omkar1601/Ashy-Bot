from discord.ext import commands 
import discord
import datetime
from Constants import Constants



class OrderPage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        if message.author.id == 749183619020488735:
            return

        if message.channel.id != Constants.ORDER_CHANNEL:
            return
        else:                
            async for msg in message.channel.history(before = message.created_at):
                if msg.author.id == 749183619020488735:                    
                    await msg.delete()
                    embed= discord.Embed(title = "**__How To Order:__**", colour = discord.Colour.light_grey())
                    embed.add_field(name = "**Format:**", value = "Your Order should pertain to the following format: **total-cards card-name farm-speed location(optional)** \n For example: \n `400 cards Asuna normal loc 12-9`  or  `400 cards Asuna slow loc 12` or `400 cards Asuna normal`", inline = False)
                    embed.add_field(name = "**P.S**", value = "Every message must contain only one order. For multiple orders, send different messages for each \nDo not use emojis or any other unnecessary phrases in your order too. Thank You for choosing us!!", inline = False )
                    await message.channel.send(embed = embed)
                    return                    
                                        
                else:
                    embed= discord.Embed(title= "**__How To Order:__**", colour= discord.Colour.light_grey())
                    embed.add_field(name = "**Format:**", value = "Your Order should pertain to the following format: **total-cards card-name farm-speed location(optional)** \n For example: \n `400 cards Asuna normal loc 12-9`  or  `400 cards Asuna slow loc 12` or `400 cards Asuna normal`", inline = False)
                    embed.add_field(name = "**P.S**", value = "Every message must contain only one order. For multiple orders, send different messages for each \nDo not use emojis or any unnecessary phrases in your order too. Thank You for choosing us!!", inline = False )
                    await message.channel.send(embed = embed)
                    return
                    

def setup(bot):
    bot.add_cog(OrderPage(bot))