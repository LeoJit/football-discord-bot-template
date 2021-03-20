import json
import os

import inflect
import discord
from discord.ext.commands import Bot
from discord.ext.commands import command, Context

from prediction_db import models
from prediction_db.models import Questions, Predictions

from discord_handler.base.cog_interface import ICog, AuthorState
from discord_handler.helper import choose_option, get_response, yes_no, CustCtx, get_user


path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..')

with open(os.path.join(path, 'secret.json'), 'r') as f:
    d = json.load(f)

p = inflect.engine()


class IntroEndedException(Exception):
    def __init__(self, message):
        super().__init__(message)


class All(ICog):
    """
    Commands that are available to all users on the server. Output may differ between different user levels.
    """

    def __init__(self, bot: Bot):
        super().__init__(bot, AuthorState.User)
        self.intro_running_list = []

    @command(
        name= "enter",
        brief= "Starts predictions.",
        help= "User can enter their predictions for the given set of questions."
    )
    async def enter(self, ctx: Context):
        await ctx.send("Lets predict in DMs! :wink:")
        channel = await CustCtx.from_member_dm(ctx.message.author, self.bot)

        comps= list(Questions.objects.all())
        comp= await choose_option(channel, "Which competition do you want to predict for?", comps)

        comp_db= Questions.objects.get(name= comp)
        questions= comp_db.questions
        options= comp_db.options
        ua= {}
        s=""

        for i in range(len(list(questions))):
            ts= ""
            ques= questions[str(i+1)]
            ts+= f"Q{i+1}) {ques}\n"
            s+= "Q. " + f"**{ques}**" + "\n"
            option_list= options[str(i+1)]
            a= await choose_option(channel, ques, option_list)
            ua[i+1] = a
            ts+= f"**Answer**- `{a}`"
            s+= a + "\n\n"
            await channel.send(ts)

        emb= discord.Embed(title= f"Predictions for {comp}", description=s, colour= discord.Colour.green())

        confirm= await yes_no("Are you sure you want to predict this?", channel, embed= emb)

        if confirm:
            print(u)
            models.Predictions(uid= ctx.author.id, name= comp, predictions= ua).save()
            await channel.send("Predicted! All the best :white_check_mark:")
        else:
            await channel.send("Cancelled!")

def setup(bot):
    bot.add_cog(All(bot))
