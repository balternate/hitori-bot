import discord
import lib.locareader
from lib.sussyconfig import get_config
import lib.sussyhelper as sh
import config as bot_config

config = get_config()

loca_sheet = "loca/loca - devmanage.csv"


def get_loca(id_: str):
    return lib.locareader.get_string_by_id(loca_sheet, id_)


sh.HelpManager.add_command_help(
    sh.CommandHelpGroup(
        group_name="mod_manage",
        command_type=sh.CommandType.SLASH,
        description=get_loca("add_cmd_desc"),
        usage=get_loca("add_cmd_desc"),
        commands=[
            sh.CommandHelp(
                command_name="add_mod",
                command_type=sh.CommandType.SLASH,
                description=get_loca("add_cmd_desc"),
                usage=get_loca("add_cmd_desc"),
                parameters=[
                    sh.CommandParameterDescription(
                        name="user",
                        description=get_loca("add_param_user_desc"),
                        required=True
                    ),
                ]
            ),
            sh.CommandHelp(
                command_name="remove_mod",
                command_type=sh.CommandType.SLASH,
                description=get_loca("remove_cmd_desc"),
                usage=get_loca("remove_cmd_desc"),
                parameters=[
                    sh.CommandParameterDescription(
                        name="user",
                        description=get_loca("remove_param_user_desc"),
                        required=True
                    ),
                ]
            ),
        ]
    ),
    sh.HelpSection.GENERAL
)


async def slash_command_listener_add(ctx: discord.Interaction, user: discord.User):
    print(f"{ctx.user} used add_mod command!")

    if ctx.user.id not in config.dev_ids:
        await ctx.followup.send(get_loca("no_permission"))
        return

    if user.id in config.dev_ids:
        await ctx.followup.send(get_loca("already_mod"))
        return

    config.dev_ids.append(user.id)
    bot_config.json_config["dev_ids"].append(user.id)
    bot_config.save_config()

    await ctx.followup.send(get_loca("added").format(user.mention))


async def slash_command_listener_remove(ctx: discord.Interaction, user: discord.User):
    print(f"{ctx.user} used remove_mod command!")

    if ctx.user.id not in config.dev_ids:
        await ctx.followup.send(get_loca("no_permission"))
        return

    if ctx.user.id == user.id:
        await ctx.followup.send(get_loca("cannot_remove_self"))
        return

    if user.id not in config.dev_ids:
        await ctx.followup.send(get_loca("not_mod"))
        return

    config.dev_ids.remove(user.id)
    bot_config.json_config["dev_ids"].remove(user.id)
    bot_config.save_config()

    await ctx.followup.send(get_loca("removed").format(user.mention))
