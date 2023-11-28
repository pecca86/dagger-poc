import os

file_path = "./.twurlrc"

content = f"""
---
profiles:
    {os.environ.get('TWITTER_USERNAME')}:
        {os.environ.get('TWITTER_CONSUMER_KEY')}:
            username: {os.environ.get('TWITTER_USERNAME')}
            consumer_key: {os.environ.get('TWITTER_CONSUMER_KEY')}
            consumer_secret: {os.environ.get('TWITTER_CONSUMER_SECRET')} 
            token: {os.environ.get('TWITTER_ACCESS_TOKEN')}
            secret: {os.environ.get('TWITTER_ACCESS_TOKEN_SECRET')}
configuration:
    default_profile:
    - {os.environ.get('TWITTER_USERNAME')}
    - {os.environ.get('TWITTER_CONSUMER_KEY')}
bearer_tokens:
    {os.environ.get('TWITTER_CONSUMER_KEY')}: {os.environ.get('TWITTER_BEARER_TOKEN')}"""

with open(file_path, "w") as file:
    file.write(content)
    pass