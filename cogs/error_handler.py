from discord.ext import commands


class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Prevent commands with local error handlers from being handled here
        if hasattr(ctx.command, "on_error"):
            return

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f"{ctx.command} can not be used in Direct Messages.")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("You are missing one or more required arguments.")


def setup(client):
    client.add_cog(ErrorHandler(client))
