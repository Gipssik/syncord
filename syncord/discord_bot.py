from typing import Optional

from discord import VoiceChannel, Intents, Interaction
from discord.ext import commands

from syncord.config import settings
from syncord.telegram_bot import ping_missing_members, send_message

intents = Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="/", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


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

    print(f"Channel members: {[f'{member.name}:::{member.id}' for member in current_channel.members]}")

    author = settings.PARTICIPANTS_MAP.get(interaction.user.id, interaction.user.name)
    present_members = {settings.PARTICIPANTS_MAP[member.id] for member in current_channel.members}
    missing_members = sorted(list(set(settings.PARTICIPANTS_MAP.values()) - present_members))
    await ping_missing_members(missing_members, settings.GUILDS_MAP[interaction.guild.id], author, message)
    pinged_message = (
        f"Pinged {', '.join([f'`{member}`' for member in missing_members])}" if missing_members else "Nobody to ping"
    )
    await interaction.response.send_message(pinged_message)


@bot.tree.command(name="syncping", description="Synced pimg-pong")
async def sync_ping(interaction: Interaction):
    await send_message("Pong!", settings.GUILDS_MAP[interaction.guild.id])
    await interaction.response.send_message("Ping!")
