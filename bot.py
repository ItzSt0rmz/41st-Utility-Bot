import os
import sys
import time
import datetime

import discord
from discord.ext.commands import Bot
from discord import Intents
import assets
import register_command
import role_analyze
import role_counter
from discord.ext import commands
import discord.ext.commands
from dotenv import load_dotenv

import git_push
import merit_config

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
TOKEN_TEST = os.getenv('DISCORD_TOKEN_TEST')
GUILD = os.getenv('DISCORD_GUILD')
KYODA_ID = 583386313466708035
FORCEPS_ID = 173202312762884096
STORM_ID = 483307383339089920
BOT_OPERATOR_ROLE = "Technical Commander"
embed_color = 0xBF502E
credit_emoji = '<:credits:937788738950545464>'


def startup(START):
    global LAUNCH
    global bot

    if START == TOKEN:
        intents = Intents.all()
        bot = Bot(intents=intents, command_prefix='.')
        bot.remove_command('help')
        LAUNCH = TOKEN

    if START == TOKEN_TEST:
        intents = Intents.all()
        bot = Bot(intents=intents, command_prefix='..')
        bot.remove_command('help')
        LAUNCH = TOKEN_TEST


startup(TOKEN)
bot_version = '4.0.4'
bot_version_date = '12/16/2022 (US EST)'


@bot.event
async def on_ready():
    now = datetime.datetime.now()
    dev_team_channel = bot.get_channel(939028644175699968)
    bot_command_channel = bot.get_channel(936902313589764146)

    message = (f"{bot.user.name} is live:\n"
               f"`v{bot_version}` - From `{bot_version_date}` \n"
               f"Release - `Alpha` \n"
               f"Launch time: `{now.month}/{now.day}/{now.year} - {now.hour}:{now.minute}`")

    print(f"{bot.user.name} is connected!")
    print('\n\n' + message)
    print(discord.__version__)
    await dev_team_channel.send(message)
    await bot_command_channel.send(message)


def credit_counter(role_names, discord_id):
    role_total = role_counter.credit_counter(role_names)
    merit_total = merit_config.merit_reader(discord_id)
    demerit_total = merit_config.demerit_reader(discord_id)

    if role_total == False:
        print("bruh")
        return False
    else:
        merit_sum = role_total + int(merit_total)
        total = merit_sum - int(demerit_total)
        return total


@bot.command(name='add')
@commands.has_role('Economy Admin')
async def add(ctx, user: discord.Member, message):
    role_names = [str(r) for r in user.roles]
    
    var_credit_value = merit_config.add_credits(user.id, int(message))
    role_credit_value = credit_counter(role_names, user.id)
    mention = format(f"<@!{user.id}>")

    embed = discord.Embed(
        description=f"Transferred {credit_emoji}`{var_credit_value}` to `user-id: {user.id}`.\n\n"
                    f"{mention} now has {credit_emoji}`{role_credit_value}`.", color=embed_color)
    embed.set_author(
        name=user.display_name, icon_url=user.avatar.url)
    await ctx.send(embed=embed)
    print(f"LOG ~ '{ctx.author.id}' used [ .add ] on '{user.id}'")


@bot.command(name='sub-merits')
@commands.has_role('Technical Commander')
async def sub_merits(ctx, user: discord.Member, message):
    if ctx.author.id == KYODA_ID or FORCEPS_ID:
        role_names = [str(r) for r in user.roles]

        var_credit_value = merit_config.subtract_merits(user.id, int(message))
        role_credit_value = credit_counter(role_names, user.id)
        mention = format(f"<@!{user.id}>")

        embed = discord.Embed(
            description=f"Removed {credit_emoji}`{var_credit_value}` from [ MERITS.TXT ] for `user-id: {user.id}`.\n\n"
                        f"{mention} now has {credit_emoji}`{role_credit_value}`.", color=embed_color)
        embed.set_author(
            name=user.display_name, icon_url=user.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .sub-merits ] on '{user.id}'")


@bot.command(name='remove')
@commands.has_role('Economy Admin')
async def remove(ctx, user: discord.Member, message):
    role_names = [str(r) for r in user.roles]

    var_credit_value = merit_config.remove_credits(user.id, int(message))
    role_credit_value = credit_counter(role_names, user.id)
    mention = format(f"<@!{user.id}>")

    embed = discord.Embed(
        description=f"Transferred {credit_emoji}`{var_credit_value}` from `user-id: {user.id}`.\n\n"
                    f"{mention} now has {credit_emoji}`{role_credit_value}`.", color=embed_color)
    embed.set_author(
        name=user.display_name, icon_url=user.avatar.url)
    await ctx.send(embed=embed)
    print(f"LOG ~ '{ctx.author.id}' used [ .remove ] on '{user.id}'")


@bot.command(name='sub-demerits')
@commands.has_role('Technical Commander')
async def sub_demerits(ctx, user: discord.Member, message):
    if ctx.author.id == KYODA_ID or FORCEPS_ID:
        role_names = [str(r) for r in user.roles]

        var_credit_value = merit_config.subtract_demerits(user.id, int(message))
        role_credit_value = credit_counter(role_names, user.id)
        mention = format(f"<@!{user.id}>")

        embed = discord.Embed(
            description=f"Removed {credit_emoji}`{var_credit_value}` from [ DEMERITS.TXT ] for `user-id: {user.id}`.\n\n"
                        f"{mention} now has {credit_emoji}`{role_credit_value}`.", color=embed_color)
        embed.set_author(
            name=user.display_name, icon_url=user.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .sub-demerits ] on '{user.id}'")


@bot.command(name='credits')
async def thing_for_roles(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        role_names = [str(r) for r in ctx.author.roles]
        user_id = str(ctx.author.id)
        mention = format(f"<@!{ctx.author.id}>")

        credit_value = credit_counter(role_names, user_id)

        if credit_value == False:
            embed = discord.Embed(
                description=f"You were not detected in the credit logs, or you have no credits. Please run `.register` "
                            f"to add yourself to the registry or to check integrity of your user.", color=embed_color)
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            if 'Medal of Valor' in role_names:
                embed = discord.Embed(
                    description=f"{mention}, You have {credit_emoji}`{credit_value}`.", color=embed_color)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    description=f"{mention}, You have {credit_emoji}`{credit_value}`.", color=embed_color)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
                print(f"LOG ~ '{ctx.author.id}' used [ .credits ]")


@bot.command(name='check-credits')
@commands.has_role('Economy Admin')
async def remove(ctx, user: discord.Member):
    role_names = [str(r) for r in user.roles]
    mention = format(f"<@!{user.id}>")

    credit_value = credit_counter(role_names, user.id)

    if credit_value == False:
        embed = discord.Embed(
            description=f"User was not detected in the credit logs, or has no credits. Please have them run `.register`"
                        f" to add yourself to the registry or to check integrity of your user. ", color=embed_color)
        embed.set_author(
            name=user.display_name, icon_url=user.avatar.url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description=f"{mention} has {credit_emoji}`{credit_value}`.", color=embed_color)
        embed.set_author(
            name=user.display_name, icon_url=user.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .add ] on '{user.id}'")


@bot.command(name='id')
@commands.has_role('Economy Admin')
async def identify(ctx, user: discord.Member):
    role_names = [str(r) for r in user.roles]
    mention = format(f"<@!{user.id}>")

    credit_value = credit_counter(role_names, user.id)
    credit_value_raw = role_counter.credit_counter(role_names)

    merit_checker = merit_config.merit_reader(user.id)
    demerit_checker = merit_config.demerit_reader(user.id)
    join_date = user.joined_at.strftime("%b %d, %Y")

    text = (f"Name: `{user.display_name}`\n"
            f"ID:`{user.id}`\n"
            f"Join Date: `{join_date}`\n"
            f"Credits: {credit_emoji}`{credit_value}`\n"
            f"Raw Credits: `{credit_value_raw}`\n"
            f"Merits: `{merit_checker}`\n"
            f"Demerits: `{demerit_checker}`\n"
            f"Certifications: \n```\n"
            f"{assets.certifications('command', role_names)}"
            f"{assets.certifications('sof1', role_names)}"
            f"{assets.certifications('sof2', role_names)}"
            f"{assets.certifications('trooper', role_names)}"
            f"{assets.certifications('pilot', role_names)}"
            f"{assets.certifications('veteran', role_names)}"
            f"{assets.certifications('valor', role_names)}```\n"
            f"<@!{user.id}>")

    if credit_value == False:
        embed = discord.Embed(
            description=f"User was not detected in the credit logs, or has no credits. Please have them run `.register`"
                        f" to add yourself to the registry or to check integrity of your user. ", color=embed_color)
        embed.set_author(
            name=user.display_name, icon_url=user.avatar.url)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(
            description=text, color=embed_color)
        embed.set_author(
            name=user.display_name, icon_url=user.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .id ] on '{user.id}'")


@bot.command(name='whoami')
async def who_am_i(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        channel = await ctx.author.create_dm()
        role_names = [str(r) for r in ctx.author.roles]
        credit_value = credit_counter(role_names, ctx.author.id)
        credit_value_raw = role_counter.credit_counter(role_names)

        merit_checker = merit_config.merit_reader(ctx.author.id)
        demerit_checker = merit_config.demerit_reader(ctx.author.id)
        join_date = ctx.author.joined_at.strftime("%b %d, %Y")

        text = (f"**USER INFO:**\n\n"
                f"Name: `{ctx.author.display_name}`\n"
                f"ID:`{ctx.author.id}`\n"
                f"Join Date: `{join_date}`\n"
                f"Credits: {credit_emoji}`{credit_value}`\n"
                f"Raw Credits: `{credit_value_raw}`\n"
                f"Merits: `{merit_checker}`\n"
                f"Demerits: `{demerit_checker}`\n"
                f"Certifications: \n```\n"
                f"{assets.certifications('command', role_names)}"
                f"{assets.certifications('sof1', role_names)}"
                f"{assets.certifications('sof2', role_names)}"
                f"{assets.certifications('trooper', role_names)}"
                f"{assets.certifications('pilot', role_names)}"
                f"{assets.certifications('veteran', role_names)}"
                f"{assets.certifications('valor', role_names)}```")

        if credit_value == False:
            await ctx.send(f"User was not detected in the credit logs, or has no credits. Please have them run "
                           f"`.register` to add yourself to the registry or to check integrity of your user. ")
        else:
            await ctx.send(f"<@!{ctx.author.id}> - User Diagnostic sent in DM's.")
            await channel.send(text)
            print(f"LOG ~ '{ctx.author.id}' used [ .whoami ]")


# register command order:
# in all three
# in registry, in merit, not demerit
# in registry, not merit, in demerit
# in registry, not merit, not demerit
# not registry, in merit, in demerit
# not registry, not merit, in demerit
# not registry, in merit, not demerit
# not all three


@bot.command(name='register')
async def register(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        mention = f"<@!{ctx.author.id}>"
        channel = bot.get_channel(939028644175699968)

        database_check = register_command.register(str(ctx.author.id), ctx.author.display_name)
        print(f"LOG ~ '{ctx.author.id}' used [ .register ]")

        if database_check == "00" or "07":
            await ctx.send(register_command.channel_reply(database_check, mention))
        else:
            report_message = register_command.report_message(
                database_check, str(ctx.author.id), ctx.author.display_name, ctx.channel.id)
            report_log = register_command.report_log(
                database_check, str(ctx.author.id), ctx.author.display_name, ctx.channel.id)

            embed = discord.Embed(
                description=register_command.channel_reply(database_check, mention), color=embed_color)
            embed.set_author(
                name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)

            await channel.send(report_message)
            with open("reports.txt", "a") as report_file:
                report_file.write(f"{report_log}\n---------------\n")


@bot.command(name='store')
async def store(ctx, message):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        store_key_list = ["1", "2", "3", "4", "5", "6", "7", "8"]
        store_key_list_all = ["0"]
        credit_emoji_all = '["7]'

        if message in store_key_list or store_key_list_all:
            if message in store_key_list:
                embed = discord.Embed(
                    title=assets.store_command(credit_emoji, 0),
                    description=assets.store_command(credit_emoji, int(message)),
                    color=embed_color)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)

                await ctx.send()
                await ctx.send()
            if message in store_key_list_all:
                channel = await ctx.author.create_dm()
                await ctx.send(f"<@!{ctx.author.id}> - Store sent in DM's.")

                await channel.send(assets.store_command(credit_emoji_all, 0))
                await channel.send(assets.store_command(credit_emoji_all, 1))
                await channel.send(assets.store_command(credit_emoji_all, 2))
                await channel.send(assets.store_command(credit_emoji_all, 3))
                await channel.send(assets.store_command(credit_emoji_all, 4))
                await channel.send(assets.store_command(credit_emoji_all, 5))
                await channel.send(assets.store_command(credit_emoji_all, 6))
                await channel.send(assets.store_command(credit_emoji_all, 7))
                await channel.send(assets.store_command(credit_emoji_all, 8))
                print(f"LOG ~ '{ctx.author.id}' used [ .store ]")


@store.error
async def store_error(ctx, error):

    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(
            description=assets.store_command(credit_emoji, 69), color=embed_color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .store ]")


@bot.command(name='shop')
async def shop(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        embed = discord.Embed(
            title="41st Elite Corps Store:",
            description=assets.shop_command(), color=embed_color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .shop ]")


@bot.command(name='ggn-store')
async def ggn_store(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        embed = discord.Embed(
            title="Geetsly's Gaming Network Store Conversions:",
            description=assets.ggn_store_command(format(ctx.author.id)), color=embed_color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .ggn-store ]")


@bot.command(name='credit-info')
async def credit_diag(ctx, message):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        role_names = [str(r) for r in ctx.author.roles]
        credit_diag_key_list = ["1", "2", "3"]
        credit_diag_key_list_all = ["0"]
        credit_emoji_all = '["7]'

        if message in credit_diag_key_list or credit_diag_key_list_all:
            print(f"LOG ~ '{ctx.author.id}' used [ .credit-info ]")
            if message == "1":
                embed = discord.Embed(
                    title="Rank Credit Details:",
                    description=(role_analyze.rank_diag(role_names, credit_emoji) + f"\n\n"
                                 f"Total Role Credits: {credit_emoji} `{role_counter.credit_counter(role_names)}`\n"
                                 f"Total Credits: {credit_emoji} `{credit_counter(role_names, ctx.author.id)}`"),
                    color=embed_color)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            if message == "2":
                embed = discord.Embed(
                    title="Medal Credit Details:",
                    description=(role_analyze.medal_diag(role_names, credit_emoji) + f"\n\n"
                                 f"Total Role Credits: {credit_emoji} `{role_counter.credit_counter(role_names)}`\n"
                                 f"Total Credits: {credit_emoji} `{credit_counter(role_names, ctx.author.id)}`"),
                    color=embed_color)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            if message == "3":
                embed = discord.Embed(
                    title="Qual Credit Details:",
                    description=(role_analyze.qual_diag(role_names, credit_emoji) + f"\n\n"
                                 f"Total Role Credits: {credit_emoji} `{role_counter.credit_counter(role_names)}`\n"
                                 f"Total Credits: {credit_emoji} `{credit_counter(role_names, ctx.author.id)}`"),
                    color=embed_color)
                embed.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
            if message == "0":
                channel = await ctx.author.create_dm()
                await ctx.send(f"<@!{ctx.author.id}> - Credit details sent in DM's.")
                await channel.send(f"**Rank Credit Details**\n\n"
                                   f"{role_analyze.rank_diag(role_names, credit_emoji_all)}")
                await channel.send(f"\n**Medal Credit Details:**\n\n"
                                   f"{role_analyze.medal_diag(role_names, credit_emoji_all)}")
                await channel.send(f"\n**Qual Credit Details:**\n\n"
                                   f"{role_analyze.qual_diag(role_names, credit_emoji_all)}")
                await channel.send(f"\nTotal Role Credits: {credit_emoji} `{role_counter.credit_counter(role_names)}`\n"
                                   f"Total Credits: {credit_emoji} `{credit_counter(role_names, ctx.author.id)}`")


@credit_diag.error
async def credit_diag_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        embed = discord.Embed(
            description=assets.credit_diag_command(), color=embed_color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)


@bot.command(name='github')
async def github(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        embed = discord.Embed(
            description="https://github.com/G41st/41st-utility-bot \n"
                        "If you are interested in helping out with the bot, be sure to DM Kyoda!", color=embed_color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        button = discord.ui.Button(label="Open Link", style=discord.ButtonStyle.grey,
                                   url='https://github.com/G41st/41st-utility-bot')
        view = discord.ui.View()
        view.add_item(button)
        await ctx.send(embed=embed, view=view)
        print(f"LOG ~ '{ctx.author.id}' used [ .github ]")


@bot.command(name='dev-server')
async def dev_server_inv(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        channel = await ctx.author.create_dm()
        await ctx.send(f"<@!{ctx.author.id}> - Dev Team Server invite sent in DM's.")
        await channel.send("https://discord.gg/H2KArTCj5a")
        print(f"LOG ~ '{ctx.author.id}' used [ .dev-server ]")


@bot.command(name='help')
async def command_help(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        embed = discord.Embed(
            title="Commands:",
            description=assets.commands_command(), color=embed_color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .help ]")


# start troll commands

@bot.command(name='fuck')
async def fuck(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        await ctx.send("you")


@bot.command(name='bitches')
async def bitches(ctx):
    role_names = [str(r) for r in ctx.author.roles]

    if 'Medal of Valor' in role_names:
        salute_emoji = '<:GreenSalute:906047649982083113>'
        mention = format(f"<@!{ctx.author.id}>")
        await ctx.send(f"congratulations {mention}, you have bitches! {salute_emoji}")
    else:
        await ctx.send(f"you have no bitches")


@bot.command(name='drugs')
async def drugs(ctx):
    await ctx.send("deathsticks?")


@bot.command(name='shitterbawx')
async def shitterbawx(ctx):
    await ctx.send("pretorien is the better ginger")


@bot.command(name='chatterbox')
async def chatterbox(ctx):
    await ctx.send("you mean shitterbawx?")


@bot.command(name='your-mom')
async def your_mom(ctx):
    await ctx.send("is in my bed. your welcome.")


@bot.command(name='no-u')
async def no_u(ctx):
    await ctx.send(assets.rage())


@bot.command(name='troll')
async def troll(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        await ctx.send(f"{assets.troll_command()}")


@bot.command(name='adko')
async def adko(ctx):
    salute_emoji = '<:GreenSalute:906047649982083113>'

    await ctx.send(f"`MJR Adko CC-1258`\n"
                   f"Trained on: `07/12/2021 (US EAST)`\n"
                   f"Stepped down on: `03/20/2022 (US EAST)`\n"
                   f"- 'The road to freedom is paved with blood. (Unknown)' \n"
                   f"Godspeed brother, may Floppa bless you on your journey.\n"
                   f"{salute_emoji}")


@bot.command(name='blue')
async def adko(ctx):
    salute_emoji = '<:GreenSalute:906047649982083113>'

    await ctx.send(f"`CPT Blue CC-1591`\n"
                   f"Trained on: `08/20/2021 (US EAST)`\n"
                   f"Stepped down on: `03/20/2022 (US EAST)`\n"
                   f"- 'A loving, caring, human being. Always there for you if you need him. Like the brother you "
                   f"never got. (2LT Raven)' \n"
                   f"Godspeed brother.\n"
                   f"{salute_emoji}")


@bot.command(name='bruh')
async def your_mom(ctx):
    await ctx.send("bruh")


@bot.command(name='crash')
async def your_mom(ctx):
    await ctx.send("bruh")


@bot.command(name='lean')
async def lean(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/875310536902979615/987065758985125928/IMG_4467.gif")


@bot.command(name='penis')
async def penis(ctx):
    await ctx.send("aphra has a small penis")


@bot.command(name='bankruptaphra.com')
async def credit_card(ctx):

    with open("troll1.txt", "r") as troll_file:
        content = troll_file.readlines()

        old_cc_number = content[0]

        with open("troll1.txt", "w") as troll_file:
            int_cc_number = int(old_cc_number[0])
            new_cc_number = int_cc_number + 1

            content[0] = str(new_cc_number) + "\n"

            troll_file.writelines(content)

            await ctx.send(f"Aphra is now {new_cc_number} credits in debt! Spam this command to support "
                     f"`.baldceps-survivor-project.com`! ")


@bot.command(name='bankruptkyoda.com')
async def credit_card_2(ctx):

    with open("troll2.txt", "r") as troll_file:
        content = troll_file.readlines()

        old_cc_number = content[0]

        with open("troll2.txt", "w") as troll_file:
            int_cc_number = int(old_cc_number[0])
            new_cc_number = int_cc_number + 1

            content[0] = str(new_cc_number) + "\n"

            troll_file.writelines(content)

            await ctx.send(f"Kyoda is now {new_cc_number} credits in debt! Spam this command to support "
                     f"`.baldceps-survivor-project.com`! ")


@bot.command(name='baldceps-survivor-project.com')
async def beauty_project(ctx):

    with open("troll3.txt", "r") as troll_file:
        content = troll_file.readlines()

        old_cc_number = content[0]

        with open("troll3.txt", "w") as troll_file:
            int_cc_number = int(old_cc_number[0])
            new_cc_number = int_cc_number + 1

            content[0] = str(new_cc_number) + "\n"

            troll_file.writelines(content)

            await ctx.send(f"Thank you! Forceps will now regrow 1 (One) hair folicle. He now has {new_cc_number} "
                     f"hair folicles!\n\nVisit our site at https://www.baldceps-survivor-project.com")

# end troll commands

@bot.command(name='version')
async def version(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        version = (f"`v{bot_version}` - From `{bot_version_date}` \n"
                   f"Release - `Alpha`")

        embed = discord.Embed(
            title="41st Utilities Version:",
            description=f"{version}", color=embed_color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .version ]")


@bot.command(name='report')
async def report(ctx):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        embed = discord.Embed(
            title="Reporting Instructions:",
            description=assets.report_command(ctx.author.id), color=embed_color)
        embed.set_author(
            name=ctx.author.display_name, icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)
        print(f"LOG ~ '{ctx.author.id}' used [ .report ]")


@bot.command(name='report-send')
async def report_send(ctx, message):
    if ctx.channel.id == '936902313589764146' or '939028644175699968':
        now = datetime.datetime.now()

        channel = bot.get_channel(939028644175699968)

        report_message = (f"NEW REPORT - - - @here \n\n"
                          f"```{ctx.author.display_name} - {ctx.author.id}\n"
                          f"{now.month}/{now.day}/{now.year} in channel '#{ctx.message.channel}' \n"
                          f"{ctx.author.display_name} said:\n '{ctx.message.content}'```\n")

        report_log = (f"{ctx.author.display_name} - {ctx.author.id}\n"
                      f"{now.month}/{now.day}/{now.year} in channel '#{ctx.message.channel}' \n"
                      f"     {ctx.author.display_name} said:\n'{ctx.message.content}'")

        with open("reports.txt", "a") as report_file:
            report_file.write(f"{report_log}\n---------------\n")

        await channel.send(report_message)
        print(f"LOG ~ '{ctx.author.id}' used [ .report-send ]")


@bot.command(name='git-push')
@commands.has_role('Technical Commander')
async def shutdown(ctx):
    if ctx.author.id == KYODA_ID or FORCEPS_ID:
        await ctx.send("```41st://<utilities> ~ $```")
        await ctx.send("`Pushing to Git`")
        time.sleep(1)

        git_push.upload()

        await ctx.send("all databases have been pushed and are backed up.")
        print(f"LOG ~ '{ctx.author.id}' used [ .git-push ]")
    else:
        await ctx.send("`Not Authorised`")


@bot.command(name='ban')
@commands.has_role('Technical Commander')
async def ban(ctx, user: discord.Member, *, reason=None):
    if ctx.author.id == KYODA_ID or FORCEPS_ID:
        await ctx.send("```41st://<utilities> ~ $```")
        await ctx.send(f"<@!{user.id}> has been reduced to atoms.")
        await user.ban(reason=reason)
        print(f"LOG ~ '{ctx.author.id}' used [ .ban ] on {user.id}")


@bot.command(name='restart')
@commands.has_role('Technical Commander')
async def shutdown(ctx):
    if ctx.author.id == KYODA_ID or FORCEPS_ID:
        await ctx.send("```41st://<utilities> ~ $```")
        await ctx.send("`Pushing to Git`")
        time.sleep(1)

        git_push.upload()

        await ctx.send("`All databases have been pushed and are backed up.`")

        await ctx.send("`Shutdown in 5`")
        time.sleep(5)
        await ctx.send("https://www.youtube.com/watch?v=Gb2jGy76v0Y")
        print("```41st://<utilities> ~ $``` \n `RESTART`")
        sys.exit()


@bot.command(name='kill')
@commands.has_role('Technical Commander')
async def shutdown(ctx):
    if ctx.author.id == KYODA_ID or FORCEPS_ID:
        await ctx.send("```41st://<utilities> ~ $``` \n `HARD-SHUTDOWN`")
        print("```41st://<utilities> ~ $``` \n `HARD-SHUTDOWN`")
        time.sleep(1)
        sys.exit()


def main():
    while True:
        bot.run(LAUNCH)
