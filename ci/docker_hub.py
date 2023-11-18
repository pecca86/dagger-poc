import sys

import anyio

import dagger

import sys


async def main():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # Cache
        python_cache = client.cache_volume("python")
        password_argument = sys.argv[1]
        # set secret as string value
        secret = client.set_secret("password", password_argument)

        # create container
        source = (
            client.container()
            .from_("ubuntu:latest")
            .with_directory("/app", client.host().directory("."))
            .with_workdir("/app")
            # .WithEnvVariable('PATH', '/root/.nvm/versions/node/v16.17.0/bin:$PATH')
            # .with_exec(["pip", "install", "-r", "requirements.txt"])
            # .with_exec(["pip", "install", "--upgrade", "openai==1.1.1"])
            # .with_exec(["apt", "install", "curl", "-y"])
            .with_exec(["./setup.sh"])
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
