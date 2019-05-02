import click
import json
import uuid
import sys
import os

from stream_chat import StreamChat


class MissingClient(object):
    def __call__(self, *args, **kwargs):
        api_key = click.prompt("Please enter your api_key", type=str)
        api_secret = click.prompt("Please enter your api_secret", type=str)
        with open(".credentials", "w") as f:
            json.dump({"api_key": api_key, "api_secret": api_secret}, f)
        sys.exit()

    def __get__(self, obj, type=None):
        return self

    def __getattr__(self, item):
        return self

    def __getitem__(self, item):
        return self


@click.group()
@click.pass_context
def main(ctx):
    """
    Stream Chat CLI built with Python
    """
    ctx.obj = MissingClient()

    if os.path.isfile(".credentials"):
        with open(".credentials") as f:
            data = json.load(f)
        ctx.obj = StreamChat(api_key=data["api_key"], api_secret=data["api_secret"])


@main.command()
def init():
    MissingClient()()


@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def token(client, user_id):
    """This argument generates a token for a user"""
    response = client.create_token(user_id)
    click.echo(response)


@main.command()
@click.pass_obj
def settings(client):
    """This argument gets app settings"""
    response = client.get_app_settings()
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.pass_obj
def channels(client, channel_type):
    """This argument gets channels with a provided channel type"""
    response = client.get_channel_types(channel_type)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def devices(client, user_id):
    """This argument gets a users devices"""
    response = client.get_devices()
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option(
    "--user_id",
    default=str(uuid.uuid4()),
    required=False,
    help="The unique identifier for the user.",
)
@click.option("--user_name", required=True, help="The name of the user.")
@click.pass_obj
def add_user(client, user_id, user_name):
    """This argument adds a new user"""
    response = client.update_user({"id": user_id, "name": user_name})
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def delete_user(client, user_id):
    """This argument deletes a user"""
    response = client.delete_user(user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def export_user(client, user_id):
    """This argument exports a user"""
    response = client.export_user(user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def deactivate_user(client, user_id):
    """This argument deactivates a user"""
    response = client.deactivate_user(user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option(
    "--user_id",
    default=uuid.uuid4(),
    required=False,
    help="The unique identifier for the user.",
)
@click.option(
    "--timeout",
    required=False,
    default=3600,
    help="The duration of the timeout for a user.",
)
@click.option(
    "--reason",
    required=False,
    default="Potty mouth!",
    help="The reason why you are banning this user.",
)
@click.pass_obj
def ban_user(client, user_id, timeout, reason):
    """This argument bans an existing user"""
    response = client.ban_user(user_id, timeout, reason)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def unban_user(client, user_id):
    """This argument unbans a user"""
    response = client.unban_user(user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def create_channel(client, channel_type, channel_name, user_id):
    """This argument creates a new channel"""
    channel = client.channel(channel_type, channel_name)
    response = channel.create(user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--json", required=True, help="The JSON to update the channel with.")
@click.pass_obj
def update_channel(client, channel_type, channel_name, json):
    """This argument creates a new channel"""
    channel = client.channel(channel_type, channel_name)
    response = channel.update(json)

    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.pass_obj
def delete_channel(client, channel_type, channel_name):
    """This argument deletes an existing channel"""
    channel = client.channel(channel_type, channel_name)
    response = channel.delete()
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.option("--text", required=True, help="The text to send to the channel.")
@click.pass_obj
def send_message(client, channel_type, channel_name, user_id, text):
    """This argument sends a new message"""
    channel = client.channel(channel_type, channel_name)
    response = channel.send_message({"text": text}, user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option(
    "--message_id", required=True, help="The unique identifier for the message."
)
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.option("--text", required=True, help="The text to send to the channel.")
@click.pass_obj
def update_message(client, message_id, user_id, text):
    """This argument updates a message"""
    response = client.update_message(
        {"id": message_id, "text": text, "user": {"id": user_id}}
    )
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option(
    "--message_id", required=True, help="The unique identifier for the message."
)
@click.pass_obj
def delete_message(client, message_id):
    """This argument deletes a message"""
    response = client.delete_message(message_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option(
    "--message_id", required=True, help="The unique identifier for the message."
)
@click.option(
    "--limit",
    required=False,
    default=0,
    help="The limit to apply to the query. (e.g. 3)",
)
@click.option(
    "--offset",
    required=False,
    default=0,
    help="The offset to apply to the query. (e.g. 1)",
)
@click.pass_obj
def get_replies(client, channel_type, channel_name, message_id, limit, offset):
    """This argument gets replies for a message"""
    channel = client.channel(channel_type, channel_name)
    response = channel.get_replies(message_id, limit=limit, offset=offset)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option(
    "--event_type",
    required=False,
    default="typing.start",
    help="The event type you would like to send. (e.g. typing.start)",
)
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def send_event(client, channel_type, channel_name, event_type, user_id):
    """This argument sends an event"""
    channel = client.channel(channel_type, channel_name)
    response = channel.send_event({"type": event_type}, user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option(
    "--message_id", required=True, help="The unique identifier for the message."
)
@click.option(
    "--reaction_type", required=True, help="The type of the reaction (e.g. love)."
)
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def send_reaction(
    client, channel_type, channel_name, message_id, reaction_type, user_id
):
    """This argument sends a reaction"""
    channel = client.channel(channel_type, channel_name)
    response = channel.send_reaction(message_id, {"type": reaction_type}, user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option(
    "--message_id", required=True, help="The unique identifier for the message."
)
@click.option(
    "--limit",
    required=False,
    default=0,
    help="The limit to apply to the query (e.g. 3)",
)
@click.option(
    "--offset",
    required=False,
    default=0,
    help="The offset to apply to the query (e.g. 1)",
)
@click.pass_obj
def get_reactions(client, channel_type, channel_name, message_id, limit, offset):
    """This argument gets all reactions for a message"""
    channel = client.channel(channel_type, channel_name)
    response = channel.get_reactions(message_id, limit=limit, offset=offset)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option(
    "--message_id", required=True, help="The unique identifier for the message."
)
@click.option(
    "--reaction_type", required=True, help="The type of the reaction (e.g. love)."
)
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def delete_reaction(
    client, channel_type, channel_name, message_id, reaction_type, user_id
):
    """This argument deletes a reaction"""
    channel = client.channel(channel_type, channel_name)
    response = channel.delete_reaction(message_id, {"type": reaction_type}, user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def mark_read(client, channel_type, channel_name, user_id):
    """This argument marks all notifications as read"""
    channel = client.channel(channel_type, channel_name)
    response = channel.mark_read(user_id)
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.pass_obj
def truncate_channel(client, channel_type, channel_name):
    """This argument truncates a channel"""
    channel = client.channel(channel_type, channel_name)
    response = channel.truncate()
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def add_member(client, channel_type, channel_name, user_id):
    """This argument adds a member to a channel"""
    channel = client.channel(channel_type, channel_name)
    response = channel.add_members([user_id])
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def remove_member(client, channel_type, channel_name, message_id, user_id):
    """This argument removes a member from a channel"""
    channel = client.channel(channel_type, channel_name)
    response = channel.remove_members([user_id])
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def add_moderator(client, channel_type, channel_name, user_id):
    """This argument adds a user as a moderator"""
    channel = client.channel(channel_type, channel_name)
    response = channel.add_moderators([user_id])
    click.echo(json.dumps(response, indent=4))


@main.command()
@click.option("--channel_type", required=True, help="The type of the channel.")
@click.option("--channel_name", required=True, help="The name of the channel.")
@click.option("--user_id", required=True, help="The unique identifier for the user.")
@click.pass_obj
def remove_moderator(client, channel_type, channel_name, user_id):
    """This argument removes a user as a moderator"""
    channel = client.channel(channel_type, channel_name)
    response = channel.add_moderators([user_id])
    click.echo(json.dumps(response, indent=4))


if __name__ == "__main__":
    main()
