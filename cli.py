import click
import json
import uuid
import sys

from stream_chat import StreamChat

chat = StreamChat(api_key="t45frc6vsuea", api_secret="5drawr26n42qq2bhmedj83f4kkvjha4mer49q9aydryat46gmp66bawx44zu5vk7")

__author__ = "Nick Parsons"

@click.group()
def main():
    """
    Stream Chat CLI built with Python
    """
    pass

@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def token(user_id):
    """This argument generates a token for a user"""
    response = chat.create_token(user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
def settings():
    """This argument gets app settings"""
    response = chat.get_app_settings()

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
def channels(channel_type):
    """This argument gets channels with a provided channel type"""
    response = chat.get_channel_types(channel_type)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def devices(user_id):
    """This argument gets a users devices"""
    response = chat.get_devices()

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--user_id", default=uuid.uuid4(), required=False, help="The unique identifier for the user.")
@click.option("--user_name", required=True, help="The name of the user.")
def add_user(user_id, user_name):
    """This argument adds a new user"""
    response = chat.update_user({ "id": user_id, name: user_name })

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def delete_user(user_id):
    """This argument deletes a user"""
    response = chat.delete_user(user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def export_user(user_id):
    """This argument exports a user"""
    response = chat.export_user(user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def deactivate_user(user_id):
    """This argument deactivates a user"""
    response = chat.deactivate_user(user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--user_id", default=uuid.uuid4(), required=False, help="The unique identifier for the user.")
@click.option("--timeout", required=False, default=3600, help="The duration of the timeout for a user.")
@click.option("--reason", required=False, default="Potty mouth!", help="The reason why you are banning this user.")
def ban_user(user_id, timeout, reason):
    """This argument bans an existing user"""
    response = chat.ban_user(user_id, timeout, reason)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def unban_user(user_id):
    """This argument unbans a user"""
    response = chat.unban_user(user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def create_channel(channel_type, channel_name, user_id):
    """This argument creates a new channel"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.create(user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--json", required=True, help="The JSON to update the channel with.")
def update_channel(channel_type, channel_name, json):
    """This argument creates a new channel"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.update(json)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
def delete_channel(channel_type, channel_name):
    """This argument deletes an existing channel"""
    if channel_type not in channel_types:
        click.echo("Invalid channel type!")
        sys.exit()

    channel = chat.channel(channel_type, channel_name)
    response = channel.delete()

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.option("--text", required=True, help="The text to send to the channel.")
def send_message(channel_type, channel_name, user_id, text):
    """This argument sends a new message"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.send_message({ "text": text }, user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--message_id", required=True, help="The unique identifier for the message.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.option("--text", required=True, help="The text to send to the channel.")
def update_message(message_id, user_id, text):
    """This argument updates a message"""
    response = chat.update_message({
        "id": message_id,
        "text": text,
        "user": { 
            "id": user_id
        },
    })

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--message_id", required=True, help="The unique identifier for the message.")
def delete_message(message_id):
    """This argument deletes a message"""
    response = chat.delete_message(message_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--message_id", required=True, help="The unique identifier for the message.")
@click.option("--limit", required=False, default=0, help="The limit to apply to the query. (e.g. 3)")
@click.option("--offset", required=False, default=0, help="The offset to apply to the query. (e.g. 1)")
def get_replies(channel_type, channel_name, message_id, limit, offset):
    """This argument gets replies for a message"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.get_replies(message_id, limit=limit, offset=offset)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--event_type", required=False, default="typing.start", help="The event type you would like to send. (e.g. typing.start)")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def send_event(channel_type, channel_name, event_type, user_id):
    """This argument sends an event"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.send_event({ "type": event_type }, user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--message_id", required=True, help="The unique identifier for the message.")
@click.option("--reaction_type", required=True, help="The type of the reaction (e.g. love).")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def send_reaction(channel_type, channel_name, message_id, reaction_type, user_id):
    """This argument sends a reaction"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.send_reaction(message_id, { "type": reaction_type }, user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--message_id", required=True, help="The unique identifier for the message.")
@click.option("--limit", required=False, default=0, help="The limit to apply to the query (e.g. 3)")
@click.option("--offset", required=False, default=0, help="The offset to apply to the query (e.g. 1)")
def get_reactions(channel_type, channel_name, message_id, limit, offset):
    """This argument gets all reactions for a message"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.get_reactions(message_id, limit=limit, offset=offset)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--message_id", required=True, help="The unique identifier for the message.")
@click.option("--reaction_type", required=True, help="The type of the reaction (e.g. love).")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def delete_reaction(channel_type, channel_name, message_id, reaction_type, user_id):
    """This argument deletes a reaction"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.delete_reaction(message_id, { "type": reaction_type }, user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def mark_read(channel_type, channel_name, user_id):
    """This argument marks all notifications as read"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.mark_read(user_id)

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
def truncate_channel(channel_type, channel_name):
    """This argument truncates a channel"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.truncate()

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def add_member(channel_type, channel_name, user_id):
    """This argument adds a member to a channel"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.add_members([user_id])

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def remove_member(channel_type, channel_name, message_id, user_id):
    """This argument removes a member from a channel"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.remove_members([user_id])

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def add_moderator(channel_type, channel_name, user_id):
    """This argument adds a user as a moderator"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.add_moderators([user_id])

    click.echo(json.dumps(response, indent=4))

@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
def remove_moderator(channel_type, channel_name, user_id):
    """This argument removes a user as a moderator"""
    channel = chat.channel(channel_type, channel_name)
    response = channel.add_moderators([user_id])

    click.echo(json.dumps(response, indent=4))

if __name__ == "__main__":
    main()