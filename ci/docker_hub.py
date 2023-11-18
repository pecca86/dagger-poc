import sys

import anyio

import dagger

import sys


async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # Cache
        python_cache = client.cache_volume("python")
        # set secret from argument
        password_argument = sys.argv[1]
        # set secret as string value
        secret = client.set_secret("password", password_argument)
        # create container
        source = (
            client.container()
            # .from_("python:3.11.0-slim-buster")
            .from_("ubuntu:latest")
            .with_directory("/app", client.host().directory("."))
            .with_workdir("/app")
            .with_exec(["echo", "hello world"])
            .with_exec(["/bin/sh", "setup.sh"])
            .with_entrypoint(
                ["python3", "project_gin.py", "-t", "theme", "-p", "twitter"]
            )
            .with_mounted_cache("./py_cache", python_cache)
        )

        # use secret for registry authentication
        addr = await source.with_registry_auth("docker.io", "pecca86", secret).publish(
            "pecca86/poc:2"
        )

    print(f"Published at: {addr}")


anyio.run(main)
