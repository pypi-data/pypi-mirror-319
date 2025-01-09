# Pssecret server

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/pssecret-server?label=PyPI%20downloads)](https://pypi.org/project/pssecret-server/)

Pssecret is self-hosted service to share secrets (like passwords) with somebody
over the network, but don't want them to appear in chats, unencrypted e-mails, etc.

This service tries to be as anonymous as possible. The only personal information that will be stored
on a server will be IP address of the client that made request to the server.

Service is built with Python, FastAPI and is using Redis for data storage.

## Installation

### Requirements

- Python 3.11+
- Redis
- Python development libraries (optional, only needed for `hiredis` module installation)

### How to install

#### Quick way

If you don't need to configure a lot of things, you can install from [pipx](https://pipx.pypa.io/stable/)

```console
$ pipx install pssecret-server
```

For better performance, install application with [hiredis](https://github.com/redis/hiredis) support.

```console
$ pipx install pssecret-server[hiredis]
```

After that just run the app with

```console
$ pssecret-server
```

This will start the [uvicorn](https://www.uvicorn.org/) server on `127.0.0.1:8000`.
Available configuration options:

```
--host TEXT        Bind socket to this host.  [default: 127.0.0.1]
--port INTEGER     Bind socket to this port. If 0, an available port will be
                   picked.  [default: 8000]
--uds TEXT         Bind to a UNIX domain socket.
--workers INTEGER  Number of worker processes.  Defaults to the
                   $WEB_CONCURRENCY environment variable if available, or 1.
--help             Show this message and exit.
```

#### If you'd like more control

Create virtual environment, install application, run using [uvicorn](https://www.uvicorn.org/) directly.

```console
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install pssecret-server
$ uvicorn pssecret_server.main:app --workers 4 --uds /path/to/socket.sock
```

You can also run [uvicorn](https://www.uvicorn.org/) without activating virtualenv, e.g. from SystemD service

```console
$ /path/to/your/.venv/bin/python -m uvicorn pssecret_server.main:app --workers 4 --uds /path/to/socket.sock
```

### Running Pssecret server

Make sure you have the Redis service running.

After installation is done, you can start pssecret server with `pssecret-server` command.
The web server will be started with [uvicorn](https://www.uvicorn.org/) ASGI web server.

```console
$ pssecret-server
```

### Configuration

Configuration is done via environment variables.

Environment variables:

- `REDIS_URL`: URL for Redis access. Check what values are supported [here](https://redis.readthedocs.io/en/stable/connections.html#redis.Redis.from_url).
- `SECRETS_ENCRYPTION_KEY`: Key used for encrypting stored data.

You can also declare these variables in a `.env` file in the working directory.
Protect this file (or other source from where `SECRETS_ENCRYPTION_KEY` is read by application)
from being read by unauthorized parties.
