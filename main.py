[i] Establishing console session…
[✓] Console connected
Python 3.12.13
container~ pip install discord.py && python3 -u main.py
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: discord.py in ./.local/lib/python3.12/site-packages (2.7.1)
Requirement already satisfied: aiohttp<4,>=3.7.4 in ./.local/lib/python3.12/site-packages (from discord.py) (3.14.3)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (2.7.1)
Requirement already satisfied: aiosignal>=1.4.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.4.0)
Requirement already satisfied: attrs>=17.3.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (26.1.0)
Requirement already satisfied: frozenlist>=1.1.1 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.8.0)
Requirement already satisfied: multidict<7.0,>=4.5 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (6.7.1)
Requirement already satisfied: propcache>=0.2.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (0.5.2)
Requirement already satisfied: typing_extensions>=4.4 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (4.16.0)
Requirement already satisfied: yarl<2.0,>=1.17.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.24.5)
Requirement already satisfied: idna>=2.0 in ./.local/lib/python3.12/site-packages (from yarl<2.0,>=1.17.0->aiohttp<4,>=3.7.4->discord.py) (3.18)
[notice] A new release of pip is available: 25.0.1 -> 26.2.1
[notice] To update, run: pip install --upgrade pip
2026-08-11 01:37:28 INFO     discord.client logging in using static token
2026-08-11 01:37:30 INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: 45d2837de172d278e6af986ea55de79f).
logged in as /ponyo#4334
2026-08-11 02:13:00 ERROR    discord.app_commands.tree Ignoring exception in command tree
Traceback (most recent call last):
  File "/home/container/.local/lib/python3.12/site-packages/discord/app_commands/tree.py", line 1138, in wrapper
    await self._call(interaction)
  File "/home/container/.local/lib/python3.12/site-packages/discord/app_commands/tree.py", line 1270, in _call
    command, options = self._get_app_command_options(data)
                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/container/.local/lib/python3.12/site-packages/discord/app_commands/tree.py", line 1174, in _get_app_command_options
    raise CommandNotFound(name, parents)
discord.app_commands.errors.CommandNotFound: Application command 'cmds' not found
[Bot-Hosting Daemon]: Checking server disk space usage, this could take a few seconds...
[Bot-Hosting Daemon]: Updating process configuration files...
[Bot-Hosting Daemon]: Ensuring file permissions are set correctly, this could take a few seconds...
[Bot-Hosting Daemon]: Pulling Docker container image, this could take a few minutes to complete...
[Bot-Hosting Daemon]: Finished pulling Docker container image
Python 3.12.13
container~ pip install discord.py && python3 -u main.py
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: discord.py in ./.local/lib/python3.12/site-packages (2.7.1)
Requirement already satisfied: aiohttp<4,>=3.7.4 in ./.local/lib/python3.12/site-packages (from discord.py) (3.14.3)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (2.7.1)
Requirement already satisfied: aiosignal>=1.4.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.4.0)
Requirement already satisfied: attrs>=17.3.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (26.1.0)
Requirement already satisfied: frozenlist>=1.1.1 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.8.0)
Requirement already satisfied: multidict<7.0,>=4.5 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (6.7.1)
Requirement already satisfied: propcache>=0.2.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (0.5.2)
Requirement already satisfied: typing_extensions>=4.4 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (4.16.0)
Requirement already satisfied: yarl<2.0,>=1.17.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.24.5)
Requirement already satisfied: idna>=2.0 in ./.local/lib/python3.12/site-packages (from yarl<2.0,>=1.17.0->aiohttp<4,>=3.7.4->discord.py) (3.18)
[notice] A new release of pip is available: 25.0.1 -> 26.2.1
[notice] To update, run: pip install --upgrade pip
2026-08-11 02:14:36 INFO     discord.client logging in using static token
Traceback (most recent call last):
  File "/home/container/.local/lib/python3.12/site-packages/discord/http.py", line 844, in static_login
    data = await self.request(Route('GET', '/users/@me'))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/container/.local/lib/python3.12/site-packages/discord/http.py", line 778, in request
    raise HTTPException(response, data)
discord.errors.HTTPException: 401 Unauthorized (error code: 0): 401: Unauthorized
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/home/container/main.py", line 49, in <module>
    bot.run("MTUzNDk2OTMxNjkyMTgzNTcxMA.GXZbka.Y9vEGjE3DHRQBq2iAZIDhGcwb4EwK7s8bI-M7U")
  File "/home/container/.local/lib/python3.12/site-packages/discord/client.py", line 933, in run
    asyncio.run(runner())
  File "/usr/local/lib/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/home/container/.local/lib/python3.12/site-packages/discord/client.py", line 922, in runner
    await self.start(token, reconnect=reconnect)
  File "/home/container/.local/lib/python3.12/site-packages/discord/client.py", line 850, in start
    await self.login(token)
  File "/home/container/.local/lib/python3.12/site-packages/discord/client.py", line 679, in login
    data = await self.http.static_login(token)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/container/.local/lib/python3.12/site-packages/discord/http.py", line 848, in static_login
    raise LoginFailure('Improper token has been passed.') from exc
discord.errors.LoginFailure: Improper token has been passed.
[Bot-Hosting Daemon]: ---------- Detected server process in a crashed state! ----------
[Bot-Hosting Daemon]: Exit code: 1
[Bot-Hosting Daemon]: Out of memory: false
[Bot-Hosting Daemon]: Checking server disk space usage, this could take a few seconds...
[Bot-Hosting Daemon]: Updating process configuration files...
[Bot-Hosting Daemon]: Ensuring file permissions are set correctly, this could take a few seconds...
[Bot-Hosting Daemon]: Pulling Docker container image, this could take a few minutes to complete...
[Bot-Hosting Daemon]: Finished pulling Docker container image
Python 3.12.13
container~ pip install discord.py && python3 -u main.py
Defaulting to user installation because normal site-packages is not writeable
Requirement already satisfied: discord.py in ./.local/lib/python3.12/site-packages (2.7.1)
Requirement already satisfied: aiohttp<4,>=3.7.4 in ./.local/lib/python3.12/site-packages (from discord.py) (3.14.3)
Requirement already satisfied: aiohappyeyeballs>=2.5.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (2.7.1)
Requirement already satisfied: aiosignal>=1.4.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.4.0)
Requirement already satisfied: attrs>=17.3.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (26.1.0)
Requirement already satisfied: frozenlist>=1.1.1 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.8.0)
Requirement already satisfied: multidict<7.0,>=4.5 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (6.7.1)
Requirement already satisfied: propcache>=0.2.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (0.5.2)
Requirement already satisfied: typing_extensions>=4.4 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (4.16.0)
Requirement already satisfied: yarl<2.0,>=1.17.0 in ./.local/lib/python3.12/site-packages (from aiohttp<4,>=3.7.4->discord.py) (1.24.5)
Requirement already satisfied: idna>=2.0 in ./.local/lib/python3.12/site-packages (from yarl<2.0,>=1.17.0->aiohttp<4,>=3.7.4->discord.py) (3.18)
[notice] A new release of pip is available: 25.0.1 -> 26.2.1
[notice] To update, run: pip install --upgrade pip
2026-08-11 02:14:48 INFO     discord.client logging in using static token
Traceback (most recent call last):
  File "/home/container/.local/lib/python3.12/site-packages/discord/http.py", line 844, in static_login
    data = await self.request(Route('GET', '/users/@me'))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/container/.local/lib/python3.12/site-packages/discord/http.py", line 778, in request
    raise HTTPException(response, data)
discord.errors.HTTPException: 401 Unauthorized (error code: 0): 401: Unauthorized
The above exception was the direct cause of the following exception:
Traceback (most recent call last):
  File "/home/container/main.py", line 49, in <module>
    bot.run("MTUzNDk2OTMxNjkyMTgzNTcxMA.GXZbka.Y9vEGjE3DHRQBq2iAZIDhGcwb4EwK7s8bI-M7U")
  File "/home/container/.local/lib/python3.12/site-packages/discord/client.py", line 933, in run
    asyncio.run(runner())
  File "/usr/local/lib/python3.12/asyncio/runners.py", line 195, in run
    return runner.run(main)
           ^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/asyncio/runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/local/lib/python3.12/asyncio/base_events.py", line 691, in run_until_complete
    return future.result()
           ^^^^^^^^^^^^^^^
  File "/home/container/.local/lib/python3.12/site-packages/discord/client.py", line 922, in runner
    await self.start(token, reconnect=reconnect)
  File "/home/container/.local/lib/python3.12/site-packages/discord/client.py", line 850, in start
    await self.login(token)
  File "/home/container/.local/lib/python3.12/site-packages/discord/client.py", line 679, in login
    data = await self.http.static_login(token)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/container/.local/lib/python3.12/site-packages/discord/http.py", line 848, in static_login
    raise LoginFailure('Improper token has been passed.') from exc
discord.errors.LoginFailure: Improper token has been passed.
[Bot-Hosting Daemon]: ---------- Detected server process in a crashed state! ----------
[Bot-Hosting Daemon]: Exit code: 1
[Bot-Hosting Daemon]: Out of memory: false
[Bot-Hosting Daemon]: Aborting automatic restart, last crash occurred less than 600 seconds ago.
