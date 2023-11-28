import sys

import anyio

import dagger

import sys

import os

from decouple import config


async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # Cache
        python_cache = client.cache_volume("python")
        # set secret from argument
        password_argument = os.environ.get("DOCKER_HUB_PASSWORD")
        # set secret as string value
        secret = client.set_secret("password", password_argument)
        # create container
        source = (
            client.container()
            .from_("amd64/ubuntu")
            .with_directory(
                "/app", client.host().directory("."), exclude=["ci/", "configs/.env"]
            )
            .with_workdir("/app")
            .with_exec(["/bin/bash", "setup.sh"])
            .with_mounted_cache("./py_cache", python_cache)
            .with_(
                env_variables(
                    {
                        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
                        "TWITTER_CONSUMER_KEY": os.environ.get("TWITTER_CONSUMER_KEY"),
                        "TWITTER_CONSUMER_SECRET": os.environ.get(
                            "TWITTER_CONSUMER_SECRET"
                        ),
                        "TWITTER_ACCESS_TOKEN": os.environ.get("TWITTER_ACCESS_TOKEN"),
                        "TWITTER_ACCESS_TOKEN_SECRET": os.environ.get(
                            "TWITTER_ACCESS_TOKEN_SECRET"
                        ),
                        "TWITTER_BEARER_TOKEN": os.environ.get("TWITTER_BEARER_TOKEN"),
                        "TWITTER_OAUTH2_CLIENT_ID": os.environ.get(
                            "TWITTER_OAUTH2_CLIENT_ID"
                        ),
                        "TWITTER_OAUTH2_CLIENT_SECRET": os.environ.get(
                            "TWITTER_OAUTH2_CLIENT_SECRET"
                        ),
                        "INSTAGRAM_LONG_TERM_ACCESS_TOKEN": os.environ.get(
                            "INSTAGRAM_LONG_TERM_ACCESS_TOKEN"
                        ),
                        "META_INSTAGRAM_APP_ID": os.environ.get(
                            "META_INSTAGRAM_APP_ID"
                        ),
                        "OPENAI_MODEL": os.environ.get("OPENAI_MODEL"),
                    }
                )
            )
            .with_exec(["env"])
            .with_exec(["python3", "./configs/setup_twurl.py"])
            .with_exec(["mv", ".twurlrc", "/root"])
            # .with_entrypoint(
            #     ["python3", "project_gin.py", "-p", "twitter", "instagram", "-a" "True"]
            # )
        )

        # use secret for registry authentication
        addr = await source.with_registry_auth("docker.io", "pecca86", secret).publish(
            "pecca86/poc:latest"
        )

    print(f"Published at: {addr}")


# all environment variables that are passed into GitHub actions, from the repository secrets
def env_variables(envs: dict[str, str]):
    def env_variables_inner(source: dagger.Container):
        for key, value in envs.items():
            source = source.with_env_variable(key, value)
        return source

    return env_variables_inner


anyio.run(main)
