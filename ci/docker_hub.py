import sys

import anyio

import dagger

import os
async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        #Cache
        python_cache = client.cache_volume("python")
        # set secret as string value
        secret = client.set_secret("password", os.environ["DOCKER_HUB_PASSWORD"])

        # create container
        source = (
            client.container()
            .from_("python:3.11-slim-buster")
            .with_directory("/app", client.host().directory("."))
            .with_workdir("/app")
            .with_exec(["pip", "install", "-r", "requirements.txt"])
            .with_exec(["pip", "install", "--upgrade", "openai==1.1.1"])
            .with_entrypoint(
                ["python3", "project_gin.py", "-t", "theme", "-p", "twitter"]
            )
            .with_mounted_cache("./py_cache", python_cache)
        )

        # use secret for registry authentication
        addr = await source.with_registry_auth(
            "docker.io", "pecca86", secret
        ).publish("pecca86/poc:2")

    print(f"Published at: {addr}")


anyio.run(main)
