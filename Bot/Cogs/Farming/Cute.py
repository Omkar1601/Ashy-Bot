from contextlib import redirect_stdout
from discord.ext import commands
import traceback
import textwrap
import inspect
import io


class cute(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cute(self, ctx, *, body):
        if ctx.author.id in self.bot.owner_ids:
            env = {
                'ctx': ctx,
                'bot': self.bot,
                'channel': ctx.channel,
                'author': ctx.author,
                'guild': ctx.guild,
                'message': ctx.message,
                'source': inspect.getsource
            }

            def cleanup_code(content):

                if content.startswith('```') and content.endswith('```'):
                    return '\n'.join(content.split('\n')[1:-1])

                return content.strip('` \n')

            env.update(globals())

            body = cleanup_code(body)
            stdout = io.StringIO()
            err = out = None

            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

            def paginate(text: str):                    
                last = 0
                pages = []
                for curr in range(0, len(text)):
                    if curr % 1980 == 0:
                        pages.append(text[last:curr])
                        last = curr
                        appd_index = curr
                if appd_index != len(text)-1:
                    pages.append(text[last:curr])
                return list(filter(lambda a: a != '', pages))

            try:
                exec(to_compile, env)
            except Exception as e:
                err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
                return await ctx.message.add_reaction('\u2049')

            func = env['func']
            try:
                with redirect_stdout(stdout):
                    ret = await func()

            except Exception:
                value = stdout.getvalue()
                err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                if ret is None:
                    if value:
                        try:
                            out = await ctx.send(f'```py\n{value}\n```')
                        except:
                            paginated_text = paginate(value)
                            for page in paginated_text:
                                if page == paginated_text[-1]:
                                    out = await ctx.send(f'```py\n{page}\n```')
                                    break
                                await ctx.send(f'```py\n{page}\n```')
                else:
                    try:
                        out = await ctx.send(f'```py\n{value}{ret}\n```')

                    except:
                        paginated_text = paginate(f"{value}{ret}")
                        for page in paginated_text:
                            if page == paginated_text[-1]:
                                out = await ctx.send(f'```py\n{page}\n```')
                                break
                            await ctx.send(f'```py\n{page}\n```')

            if out:
                await ctx.message.add_reaction('\u2705')
            elif err:
                await ctx.message.add_reaction('\u2049')
            else:
                await ctx.message.add_reaction('\u2705')


def setup(bot):
    bot.add_cog(cute(bot))
