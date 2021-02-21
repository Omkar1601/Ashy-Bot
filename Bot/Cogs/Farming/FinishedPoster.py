import discord
from discord.ext import commands
import sqlite3
import discord.utils
from Constants import Constants

class FinishedPoster(commands.Cog):
    def __init__(self, bot):
        self.bot= bot        

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction_channel= self.bot.get_channel(payload.channel_id)
        message= await reaction_channel.fetch_message(payload.message_id)
        user= self.bot.get_user(payload.user_id)
        guild= self.bot.get_guild(payload.guild_id)
        member= guild.get_member(payload.user_id)

        for emote in message.reactions:
            if(str(emote.emoji) != Constants.REACTION_EMOTE):
                pass
            else:
                if reaction_channel.id == Constants.PROGRESS_CHANNEL:
                        finished_channel = self.bot.get_channel(Constants.FINISHED_CHANNEL)
                        if user == self.bot.user:
                            return
                        flag = True
                        farmer_role = discord.utils.get(message.guild.roles, id = Constants.FARMER_ID)
                        if farmer_role not in member.roles:
                            flag = False
                            return await message.remove_reaction(Constants.REACTION_EMOTE, user)

                        if flag:
                            farm_id = message.embeds[0].fields[0].value
                            mydb = sqlite3.connect("Farm.sqlite")
                            cursor = mydb.cursor()
                            
                            cursor.execute(f"select * from FARM where Farm_ID = {farm_id} and Farmer_ID = {user.id}")
                            result = cursor.fetchone()

                            if not result:
                                await message.remove_reaction(Constants.REACTION_EMOTE, user)
                                await message.channel.send("You ain't working on this order!", delete_after= 5)
                                return

                            else: 
                                buyer = str(result[1])
                                card = str(result[2])
                                nos = str(result[3])                                        
                                price = str(result[5])

                                cursor.execute(f"select Custom_Msg from CUSTOM where Farmer_ID= {user.id}")
                                result = cursor.fetchone()

                                if result == None:
                                    await finished_channel.send(f"Heyaa <@{buyer}>! Your order for {nos} cards of {card} has been completed at a grand total of {price} gold. Please ping <@{user.id}> at your earliest convenience.")

                                else:
                                    msg = str(result[0])
                                    msg = msg.replace("BUYER", f"<@{buyer}>")
                                    msg = msg.replace("CARD", card)
                                    msg = msg.replace("NUM", nos)
                                    msg = msg.replace("PRICE", price)
                                    msg = msg.replace("FARMER", f"<@{user.id}>")

                                    await finished_channel.send(msg)
                                    

                                cursor.execute(f"delete from FARM where Farm_ID = {farm_id} and Farmer_ID = {user.id}")
                                await message.delete()

                            mydb.commit()
                            cursor.close()
                            mydb.close()

def setup(bot):
    bot.add_cog(FinishedPoster(bot))    
