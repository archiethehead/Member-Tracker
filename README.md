# Member-Tracker
A Discord bot for a client that needs to be alerted when a member of their server leaves. It accomplishes this by checking every members name against an initialized file with the server members (adding new members), and seeing if any are missing. A part of the mandate was to make it cost effective, so this is all handled in on_ready(), and ran once every 24 hours in an Azure Virtual Machine.

# Installation
The repository (inlcuding the source and documentation) can be cloned with the folowing command:

> git clone https://github.com/archiethehead/Member-Tracker

The bot itself can be invited to servers with the following link:

> https://discord.com/oauth2/authorize?client_id=1449210899964366960&permissions=67584&integration_type=0&scope=bot

# Quick Start
Launching main.py creates a server connection, which runs an instance of the bot for every server it is in. The release build will handle this with Microsoft Azure, eliminating the need for local hosting.

# Contributors
Mr. Archie T. Healy - archiehealy06@gmail.com

# License
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <https://unlicense.org>