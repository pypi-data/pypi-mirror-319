from typing import Annotated

from arcade.sdk import ToolContext, tool
from arcade.sdk.auth import Slack
from arcade.sdk.errors import RetryableToolError
from slack_sdk import WebClient

from arcade_slack.tools.utils import format_channels, format_users


@tool(
    requires_auth=Slack(
        scopes=[
            "chat:write",
            "im:write",
            "users.profile:read",
            "users:read",
        ],
    )
)
def send_dm_to_user(
    context: ToolContext,
    user_name: Annotated[
        str,
        "The Slack username of the person you want to message. "
        "Slack usernames are ALWAYS lowercase.",
    ],
    message: Annotated[str, "The message you want to send"],
) -> Annotated[dict, "The response from the Slack API"]:
    """Send a direct message to a user in Slack."""
    slackClient = WebClient(
        token=context.authorization.token
        if context.authorization and context.authorization.token
        else ""
    )

    # Step 1: Retrieve the user's Slack ID based on their username
    userListResponse = slackClient.users_list()
    user_id = None
    for user in userListResponse["members"]:
        if user["name"].lower() == user_name.lower():
            user_id = user["id"]
            break

    if not user_id:
        raise RetryableToolError(
            "User not found",
            developer_message=f"User with username '{user_name}' not found.",
            additional_prompt_content=format_users(userListResponse),
            retry_after_ms=500,  # Play nice with Slack API rate limits
        )

    # Step 2: Retrieve the DM channel ID with the user
    im_response = slackClient.conversations_open(users=[user_id])
    dm_channel_id = im_response["channel"]["id"]

    # Step 3: Send the message as if it's from you (because we're using a user token)
    response = slackClient.chat_postMessage(channel=dm_channel_id, text=message)
    response.validate()

    if isinstance(response.data, dict):
        return response.data
    return {}


@tool(
    requires_auth=Slack(
        scopes=[
            "chat:write",
            "channels:read",
            "groups:read",
        ],
    )
)
def send_message_to_channel(
    context: ToolContext,
    channel_name: Annotated[
        str,
        "The Slack channel name where you want to send the message. "
        "Slack channel names are ALWAYS lowercase.",
    ],
    message: Annotated[str, "The message you want to send"],
) -> Annotated[dict, "The response from the Slack API"]:
    """Send a message to a channel in Slack."""

    slackClient = WebClient(
        token=context.authorization.token
        if context.authorization and context.authorization.token
        else ""
    )

    # Step 1: Retrieve the list of channels
    channels_response = slackClient.conversations_list()
    channel_id = None
    for channel in channels_response["channels"]:
        if channel["name"].lower() == channel_name.lower():
            channel_id = channel["id"]
            break

    if not channel_id:
        raise RetryableToolError(
            "Channel not found",
            developer_message=f"Channel with name '{channel_name}' not found.",
            additional_prompt_content=format_channels(channels_response),
            retry_after_ms=500,  # Play nice with Slack API rate limits
        )

    # Step 2: Send the message to the channel
    response = slackClient.chat_postMessage(channel=channel_id, text=message)
    response.validate()

    if isinstance(response.data, dict):
        return response.data
    return {}
