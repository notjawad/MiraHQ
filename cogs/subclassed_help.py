import datetime

import discord
from discord.ext import commands


class MyHelpCommand(commands.HelpCommand):
    # This function triggers when somone type `<prefix>help`
    async def send_bot_help(self, mapping):
        ctx = self.context

        embed = discord.Embed(colour=0x2F3136,
                              timestamp=datetime.datetime.utcnow())

        for cog in mapping.keys():
            if cog:
                if cog.qualified_name in ("ErrorHandler", "Events", "Help"):
                    pass
                else:
                    embed.add_field(name=cog.qualified_name, value=f"``<prefix>help {cog.qualified_name}``",
                                    inline=False)
            else:
                pass
        embed.set_footer(text="Commands are case-sensitive")
        await ctx.send(embed=embed)

    # Do what you want to do here

    # This function triggers when someone type `<prefix>help <cog>`
    async def send_cog_help(self, cog):
        ctx = self.context

        embed = discord.Embed(title=f"{cog.qualified_name} Commands")
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)

        for command in filtered:
            embed.add_field(name=command.name, value=f"{command.short_doc or '...'}\n", inline=False)
        await self.get_destination().send(embed=embed)

    # Do what you want to do here

    # This function triggers when someone type `<prefix>help <command>`
    async def send_command_help(self, command):
        ctx = self.context

    # Do what you want to do here

    # This function triggers when someone type `<prefix>help <group>`
    async def send_group_help(self, group):
        ctx = self.context

        f = []

        for command in group.commands:
            f.append(f"`{command.name}` - {command.brief}")

        embed = discord.Embed(colour=0x2F3136)
        embed.description = "\n".join(f)
        await ctx.send(embed=embed)

    # Do what you want to do here


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

        # Storing main help command in a variable
        self.client._original_help_command = client.help_command

        # Assiginig new help command to bot help command
        client.help_command = MyHelpCommand()

        # Setting this cog as help command cog
        client.help_command.cog = self

    # Event triggers when this cog unloads
    def cog_unload(self):
        # Setting help command to the previous help command so if this cog unloads the help command restores to previous
        self.client.help_command = self.client._original_help_command


def setup(client):
    client.add_cog(Help(client))
