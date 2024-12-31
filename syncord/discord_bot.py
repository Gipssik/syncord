from typing import Optional

from discord import VoiceChannel, Intents, Interaction, AllowedMentions
from discord.ext import commands

from syncord.config import settings
from syncord.maps import PARTICIPANTS_MAP, GUILDS_MAP
from syncord.telegram_bot import ping_missing_members, send_message
from syncord.utils import write_json_to_file

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    if settings.SYNC_COMMANDS:
        await bot.tree.sync()
        await bot.close()


@bot.tree.command(name="pm", description="Ping missing members")
async def ping_missing(interaction: Interaction, message: Optional[str] = None):
    current_channel = None
    for channel in interaction.guild.channels:
        if isinstance(channel, VoiceChannel) and interaction.user in channel.members:
            current_channel = channel
            break

    if current_channel is None:
        print(f"Channel not found for {interaction.user.name}")
        await interaction.response.send_message("You are not in a voice channel")
        return

    print(
        f"Channel {current_channel.guild.name}({current_channel.guild.id}):{current_channel.name} members:"
        f" {[f'{member.name}:::{member.id}' for member in current_channel.members]}"
    )

    present_members = {PARTICIPANTS_MAP[member.id] for member in current_channel.members}
    missing_members = sorted(list(set(PARTICIPANTS_MAP.values()) - present_members))

    telegram_chat_id = GUILDS_MAP.get(interaction.guild.id)
    if not telegram_chat_id:
        print(f"Telegram chat id not found for {interaction.guild.name}")
        await interaction.response.send_message("This guild is not configured")
        return

    author = PARTICIPANTS_MAP.get(interaction.user.id, interaction.user.name)

    await ping_missing_members(missing_members, telegram_chat_id, author, message)

    pinged_message = (
        f"Pinged {', '.join([f'`{member}`' for member in missing_members])}" if missing_members else "Nobody to ping"
    )
    await interaction.response.send_message(pinged_message)


@bot.tree.command(name="set-telegram", description="Set telegram chat id")
async def set_telegram_chat_id(interaction: Interaction, chat_id: int):
    try:
        GUILDS_MAP[interaction.guild.id] = chat_id
        write_json_to_file(settings.GUILDS_FILE, GUILDS_MAP)
    except Exception as e:
        print(f"Error setting telegram chat id: {e}")
        await interaction.response.send_message("Error setting telegram chat id")
        return
    else:
        await interaction.response.send_message(f"Telegram chat id set to `{chat_id}`")


@bot.tree.command(name="add-participant", description="Add participant")
async def add_participant(interaction: Interaction, discord_mention: str, telegram_username: str):
    discord_id = int(discord_mention.lstrip("<").lstrip("@").rstrip(">"))
    new_member = interaction.guild.get_member(discord_id)
    if new_member is None:
        await interaction.response.send_message("User not found")
        return

    try:
        PARTICIPANTS_MAP[new_member.id] = telegram_username.lstrip("@")
        write_json_to_file(settings.PARTICIPANTS_FILE, PARTICIPANTS_MAP)
    except Exception as e:
        print(f"Error adding participant: {e}")
        await interaction.response.send_message("Error adding participant")
        return
    else:
        await interaction.response.send_message(
            f"Participant {new_member.mention} added",
            allowed_mentions=AllowedMentions.none(),
        )


@bot.tree.command(name="remove-participant", description="Remove participant")
async def remove_participant(interaction: Interaction, discord_mention: str):
    discord_id = int(discord_mention.lstrip("<").lstrip("@").rstrip(">"))
    member = interaction.guild.get_member(discord_id)
    if member is None:
        await interaction.response.send_message("User not found")
        return

    try:
        del PARTICIPANTS_MAP[member.id]
        write_json_to_file(settings.PARTICIPANTS_FILE, PARTICIPANTS_MAP)
    except Exception as e:
        print(f"Error removing participant: {e}")
        await interaction.response.send_message("Error removing participant")
        return
    else:
        await interaction.response.send_message(
            f"Participant {member.mention} removed",
            allowed_mentions=AllowedMentions.none(),
        )


@bot.tree.command(name="list-participants", description="List participants")
async def list_participants(interaction: Interaction):
    participants_str = ""
    for discord_id, telegram_username in PARTICIPANTS_MAP.items():
        member = interaction.guild.get_member(discord_id)
        if member is None:
            continue
        participants_str += f"{member.mention}: `{telegram_username}`\n"

    await interaction.response.send_message(participants_str, allowed_mentions=AllowedMentions.none())


@bot.tree.command(name="syncping", description="Synced pimg-pong")
async def sync_ping(interaction: Interaction):
    chat_id = GUILDS_MAP.get(interaction.guild.id)
    if not chat_id:
        await interaction.response.send_message("This guild is not configured")
        return
    await send_message("Pong!", chat_id)
    await interaction.response.send_message("Ping!")
