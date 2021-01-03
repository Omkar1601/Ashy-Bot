from discord.ext import commands
from Constants import Constants


class MsgEdit(commands.Cog):
    def __init__(self, bot):
        self.bot= bot

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.channel.id == Constants.ORDER_CHANNEL:    
            if after.content == before.content:
                return
            if after.author.bot:
                return
            if Constants.REACTION_EMOTE in before.reactions:
                await after.channel.send(f"<@{after.author.id}> avoid editing an Order which has already been registered by the bot. And if you still intend to make any change to your order, ping a Farmer/ Helper for further instructions." , delete_after= 10)
            else:
                await after.channel.send(f"<@{after.author.id}> Ummm... edited messages do not count! If your order was missing the emote <a:BTtick:749907713558839357> , do post another fresh order with the correct format.", delete_after= 10)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel.id == Constants.ORDER_CHANNEL:
            if Constants.VALIDATION_EMOTE in message.reactions:
                await message.channel.send(f"<@{message.author.id}> do not delete your farming orders registered by the bot. If changes are to be made to your order, ping a Farmer/Helper and wait for further instructions.", delete_after= 10)
                return


def setup(bot):
    bot.add_cog(MsgEdit(bot))