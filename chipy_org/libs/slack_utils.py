import json

import requests


def post_message_to_slack(channel_key: str, channel_name: str, message: str):
    """
    This function is used to post messages from chipy.org to the chipy slack
    channel_key: secret key for slack channel
    channel_name: human readable description of the slack channel
    message: string formatted text to post to the slack channel
    """

    webhook_url = f"https://hooks.slack.com/services/{channel_key}"
    slack_data = {"text": message}

    response = requests.post(
        webhook_url,
        data=json.dumps(slack_data),
        headers={"Content-Type": "application/json"},
        allow_redirects=False,
    )

    if response.status_code != 200:
        raise requests.HTTPError(
            f"Failed to post message '{message[:25]}...' to slack channel '{channel_name}'. \
                Status code {response.status_code} != 200."
        )
