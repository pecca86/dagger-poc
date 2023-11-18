import sys

import anyio

import dagger

import sys

import os


async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # Cache
        python_cache = client.cache_volume("python")
        # print all environment variables that are passed into GitHub actions, from the repository secrets
        print(os.environ)

        # set secret from argument
        password_argument = os.environ.get("DOCKER_HUB_PASSWORD")  # sys.argv[1]
        # set secret as string value
        secret = client.set_secret("password", password_argument)
        # create container
        source = (
            client.container()
            # .from_("python:3.11.0-slim-buster")
            .from_("ubuntu:latest")
            .with_directory(
                "/app", client.host().directory("."), exclude=["ci/", "configs/.env"]
            )
            .with_workdir("/app")
            .with_exec(["/bin/sh", "setup.sh"])
            .with_entrypoint(
                ["python3", "project_gin.py", "-t", "theme", "-p", "twitter"]
            )
            .with_mounted_cache("./py_cache", python_cache)
            .with_(
                env_variables(
                    {
                        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
                        "TWITTER_CONSUMER_KEY": os.environ.get("TWITTER_CONSUMER_KEY"),
                        "TWITTER_CONSUMER_SECRET": os.environ.get("TWITTER_CONSUMER_SECRET"),
                        "TWITTER_ACCESS_TOKEN": os.environ.get("TWITTER_ACCESS_TOKEN"),
                        "TWITTER_ACCESS_TOKEN_SECRET": os.environ.get("TWITTER_ACCESS_TOKEN_SECRET"),
                        "TWITTER_BEARER_TOKEN": os.environ.get("TWITTER_BEARER_TOKEN"),
                        "TWITTER_OAUTH2_CLIENT_ID": os.environ.get("TWITTER_OAUTH2_CLIENT_ID"),
                        "TWITTER_OAUTH2_CLIENT_SECRET": os.environ.get("TWITTER_OAUTH2_CLIENT_SECRET"),
                        "TWITTER_WITH_IMAGE": os.environ.get("TWITTER_WITH_IMAGE"),
                        "INSTAGRAM_LONG_TERM_ACCESS_TOKEN": os.environ.get("INSTAGRAM_LONG_TERM_ACCESS_TOKEN"),
                        "META_INSTAGRAM_APP_ID": os.environ.get("META_INSTAGRAM_APP_ID"),
                        "AUTOGEN_MODEL": os.environ.get("AUTOGEN_MODEL"),
                    }
                )
            )
        )

        # use secret for registry authentication
        addr = await source.with_registry_auth("docker.io", "pecca86", secret).publish(
            "pecca86/poc:2"
        )

    print(f"Published at: {addr}")


def env_variables(envs: dict[str, str]):
    def env_variables_inner(source: dagger.Container):
        for key, value in envs.items():
            source = source.with_env(key, value)
        return source
    return env_variables_inner


anyio.run(main)
