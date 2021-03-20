import discord
from discord.ext.commands import Bot, command, Context
from discord_handler.helper import get_response, yes_no

from prediction_db import models
from prediction_db.models import Questions

from discord_handler.base.cog_interface import ICog, AuthorState


class Setup(ICog):
    """
    Setup commands. Use this first when you add Intro Bot to your server.
    """

    def __init__(self, bot: Bot):
        super().__init__(bot, AuthorState.Owner)

    @command(
        name='setup',
        brief='Starts the setup process for Predictions Bot',
        help='Starts the setup process. This will guide you through the basic channels and settings.'
    )
    async def setup(self, ctx: Context):
        n= "Please input the name of the competition:"
        name= await get_response(ctx, n)
        comp_name= name[0].strip()
        qs= {}
        op= {}
        i=1

        while True:
            q = "Please enter the question:"
            qe= await get_response(ctx, q)
            if qe[0].strip().lower() == "end":
                break
            else:
                qta= qe[0].strip()
                o= await get_response(ctx, "Please input the options of this questions, separated by a new line.")
                ol= o[0].split("\n")

                s= f"Q{i}) {qta}\n**__Options:__** {ol}"
                await ctx.send(f"{s}\nAdded!")
                qs[i] = qta
                op[i] = ol
            i+=1

        s1= ""
        for j in list(qs):
            s1+= f"Q{j}) {qs[j]}\n**__Options available:__**{op[j]}\n"

        emb= discord.Embed(title= "Predictions Form", description= "", colour= discord.Colour.red())
        emb.add_field(name= comp_name, value= s1, inline= False)

        confirm= await yes_no("Are you sure you want to add this?", ctx, embed= emb)

        if confirm:
            models.Questions(name= comp_name, questions= qs, options= op).save()
        else:
            await ctx.send("Cancelled!")


def setup(bot):
    bot.add_cog(Setup(bot))
