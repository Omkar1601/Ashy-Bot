from discord.ext import commands 
import sqlite3
from Constants import Constants


class Custom(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_role(Constants.FARMER_ID)
    async def custom(self, ctx):
        await ctx.send(f"""**__Custom Finished-Channel Message:__** \nSet up your own custom message to be displayed on completion of your undertaken order with the following command: \n`{self.bot.command_prefix}setmsg <message>` where `<message>` should contain the following: \n:small_blue_diamond: BUYER \n:small_blue_diamond: CARD \n:small_blue_diamond: EXP \n:small_blue_diamond: PRICE \n:small_blue_diamond: FARMER \nExample: `{self.bot.command_prefix}setmsg Heya BUYER!!! Your order for EXP xp CARD has been completed at a grand total of PRICE gold. Please ping FARMER in Anitrade 1/2/3 at your convenience.` \n \nP.S. *To include emotes, add them to your message using their IDs [\\<:dead:123456\\> , :owo:]. The emotes, if custom, should be present in this server or DM/Ping Ashy with your message containing the emotes.*""")

    @commands.command()
    @commands.has_role(Constants.FARMER_ID)
    async def setmsg(self, ctx , *, custmsg):
      #  if (discord.utils.find("BUYER", custmsg) and discord.utils.find("CARD", custmsg) and discord.utils.find("EXP", custmsg) and discord.utils.find("PRICE", custmsg) and discord.utils.find("FARMER", custmsg)):
        if ("BUYER" not in custmsg or "CARD" not in custmsg or "EXP" not in custmsg or "PRICE" not in custmsg or "FARMER" not in custmsg):
            await ctx.send("Incorrect format! Use `sus!custom`")
            return
        else:

            mydb = sqlite3.connect("farm.sqlite")
            cursor = mydb.cursor()
            cursor.execute(f"select * from CUSTOM where Farmer_ID= {ctx.author.id}")
            result = cursor.fetchone()
            if not result:
                cmd = "insert into CUSTOM values(?, ?)"
                val = (ctx.author.id, custmsg)
                cursor.execute(cmd, val)
                await ctx.message.add_reaction(Constants.VALIDATION_EMOTE)
            else:
                cmd= "update CUSTOM set Custom_Msg= ? where Farmer_ID=?"
                val= (custmsg, ctx.author.id)
                cursor.execute(cmd, val)
                await ctx.message.add_reaction(Constants.VALIDATION_EMOTE)
            
            mydb.commit()
            cursor.close()
            mydb.close()

    
def setup(bot):
    bot.add_cog(Custom(bot))