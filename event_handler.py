import discord
import command_handler
import random as rr
import message_list
import random_meme


class SARA_SYSTEM(discord.Client):

    def __init__(self, *args, **options):
        super().__init__(*args, **options)

        self.quotes = []
        self.raw_quotes = None
        self.quotes_channel_id = message_list.QUOTES_CHANNEL_ID
        self.quotes_file = "quotes.txt"

        self.spam_id = message_list.BOT_SPAM_ID
        self.spam_ch = None

        self.general_id = message_list.CUCK_CHAT_ID
        self.general_ch = None

        self.logging = False

        self.COLOR_PINK = discord.Colour(0xFF00E9)

    async def on_ready(self):
        print(f"{self.user} - ready")

        print("Loading local quotes")
        self.open_quotes()

        print("Loading channels")
        self.general_ch = self.get_channel(self.general_id)
        self.spam_ch = self.get_channel(self.spam_id)

        print("ALL SYSTEMS LOADED...")

    async def on_member_join(self, member):
        ch = self.get_channel(message_list.CUCK_CHAT_ID)
        await ch.send(f"Welcome {member.mention}, i'd recommend you leave while you still can")

    async def on_member_remove(self, member):
        ch = self.get_channel(message_list.CUCK_CHAT_ID)
        await ch.send(f"Byee {member.mention}, you won't be missed")

    async def on_voice_state_update(self, member, before, after):

        if self.logging:
            msg = f"{member.mention} - Voice state update"
            msg += "\n"

            member_before_after = {"Deafened": [before.deaf, after.deaf],
                                   "Muted": [before.mute, after.mute],
                                   "Self-Muted": [before.self_mute, after.self_mute],
                                   "Streaming": [before.self_stream, after.self_stream],
                                   "Video": [before.self_video, after.self_video],
                                   "AFK": [before.afk, after.afk],
                                   "Channel": [before.channel, after.channel]
                                   }

            for k, v in member_before_after.items():
                if v[0] != v[1]:
                    msg += f"{k} : {v[0]} -> {v[1]}"

            await self.spam_ch.send(msg)

    async def on_typing(self, ch, user, when):
        # if user.id == 114547828650541057:
        #    await ch.send(f"Nobody cares {user.mention}, just stop typing.")
        return

    async def on_message(self, message):
        if message.author != self.user:
            if message.content.startswith("!SARA") or message.content.startswith("!sara"):
                if message.content.upper() == "!SARA":
                    await message.channel.send("Yes?")
                    return
                else:
                    cmd = message.content[6:]
                    print(f"Command from {message.author} - {message.author.mention}:\n->\t{cmd}")

                    reply = command_handler.handle_command(cmd, author=message.author)
                    if isinstance(reply, str):
                        await message.channel.send(reply)

                    cmd_s = cmd.split()

                    if cmd.lower() == "commands":

                        embed = self.generate_embed(title="COMMANDS",
                                                    desc="A list of available commands for the SARA-SYSTEM bot\n"
                                                         "All commands should start with the '!SARA' prefix;\n"
                                                         "ex: !SARA meme",
                                                    img=message_list.SARA_PIC,
                                                    footer="commands")

                        embed.add_field(name="insult", value="usage: '**insult {name}**',\n "
                                                             "generates a random shakespearean insult",
                                        inline=False)
                        embed.add_field(name="swanson", value="returns a random Ron Swanson quote "
                                                              "from 'Parks and Recreation'",
                                        inline=False)
                        embed.add_field(name="quote", value="Returns a random quote from our Hall Of Fame",
                                        inline=False)
                        embed.add_field(name="meme", value="Returns a random meme",
                                        inline=False)
                        embed.add_field(name="admin", value="Admin screen",
                                        inline=False)

                        await message.channel.send(embed=embed)

                    elif cmd.lower() == "quote":
                        await message.channel.send(self.quotes[rr.randint(0, len(self.quotes) - 1)])
                        return

                    elif cmd.lower() == "meme":
                        pic_location = random_meme.get_random_meme()

                        if pic_location is not None:
                            pic = discord.File(pic_location)
                            await message.channel.send(file=pic)

                    elif cmd.lower() == "admin" and (message.author.id != message_list.MY_ID or
                                                     message.author.id != message.guild.owner.id):
                        await message.channel.send(message.author.mention,
                                                   file=discord.File("replys\\supervisor.gif"))

                    elif message.author.id == message_list.MY_ID or message.author.id == message.guild.owner.id:
                        print("ADMIN COMMAND - executed by", message.author.name, message.author.id)

                        if cmd.lower() == "admin":
                            emb = self.generate_embed(title="Admin commands",
                                                      desc="All available admin commands",
                                                      footer="admin commands")

                            emb.add_field(name="Shutdown", value="Shuts down the bot, "
                                                                 "requires a manual restart on the server\n"
                                                                 "**Usage: **`!SARA shutdown`",
                                          inline=False)

                            emb.add_field(name="Update quotes", value="Updates the quotes "
                                                                      "received from the hall of fame and"
                                                                      "saves them locally on the server\n"
                                                                      "**Usage: **`!SARA update`",
                                          inline=False)

                            emb.add_field(name="get user", value=f"Gets available data from the requested user"
                                                                 f"\n**Usage: **"
                                                                 f"`!SARA get user @User`",
                                          inline=False)

                            emb.add_field(name="serverinfo", value="Gives a list of info "
                                                                   "on the server the command was executed on\n"
                                                                   "**Usage: **`!SARA serverinfo`",
                                          inline=False)

                            emb.add_field(name="deletemsg", value="Deletes x amount of messages from the channel "
                                                                  "the command was executed in\n"
                                                                  "**Limits: **max 100 messages, "
                                                                  "can not be older then 14 days\n"
                                                                  "**Usage : **`!SARA deletemsg 5`", inline=False)

                            await message.channel.send(embed=emb)

                        if cmd.lower() == "shutdown":
                            await message.channel.send("Shutting down...")
                            await message.channel.send(file=discord.File("replys\\out.gif"))
                            await self.logout()
                            return

                        elif cmd.lower() == "update quotes":
                            print("Updating quotes")
                            await self.load_quotes()
                            self.save_quotes()
                            await message.channel.send("QUOTES UPDATED")

                            print("QUOTES UPDATED")
                            print("RELOADING QUOTES")
                            self.open_quotes()
                            print("DONE")
                            return

                        elif cmd.lower()[:8] == "get user":
                            try:
                                username = cmd[8:].split()[0]
                                print(f"Getting info on user: {username}")
                                user_id = command_handler.mention_to_id(username)

                                user = self.get_user(user_id)

                                u = {'Name': user.name,
                                     'Display name': user.display_name,
                                     'ID': user.id,
                                     'Discriminator': user.discriminator,
                                     'Avatar': user.avatar,
                                     'Avatar animated?': user.is_avatar_animated(),
                                     'Avatar-url': user.avatar_url,
                                     'Is bot?': user.bot,
                                     'Is system?': user.system,
                                     'Date created': user.created_at
                                     }

                                embed = self.generate_embed(title="User info",
                                                            desc="All found info on requested user",
                                                            img=u['Avatar-url'],
                                                            footer=f"User info on {u['Name']}")

                                for k, v in u.items():
                                    # print(f"--> KEY: {k}\tVALUE: {v}")
                                    embed.add_field(name=k, value=v, inline=False)

                                await message.channel.send(embed=embed)

                            except IndexError:
                                await message.channel.send("No username provided " + message.author.mention)
                            return

                        elif cmd == "serverinfo":
                            guild = {
                                "Name": message.guild.name,  # str
                                "Owner": message.guild.owner,  # Member
                                "ID": message.guild.id,  # int
                                "Icon_url": message.guild.icon_url,  # str
                                "Banner": message.guild.banner,  # str
                                "Member_count": message.guild.member_count,  # int
                                "Members": message.guild.members,  # list[Member]
                                "Emojis": message.guild.emojis  # tuple
                            }

                            embed = self.generate_embed(title="Server info",
                                                        desc="Basic info on requested server",
                                                        img=guild['Icon_url'],
                                                        footer='Server info')

                            for k, v in guild.items():
                                print(f"KEY: {k}\tVALUE: {v}\n\t"
                                      f"V Type {type(v)} \tint/str: {isinstance(v, str) or isinstance(v, int)}")

                                if isinstance(v, str) or isinstance(v, int):
                                    v = str(v)
                                    embed.add_field(name=k, value=v, inline=False)

                                elif isinstance(v, discord.member.Member):
                                    embed.add_field(name="Owner", value=guild['Owner'].mention)

                                elif isinstance(v, list):
                                    txt = "```"
                                    for member in v:
                                        txt += f"Member Name: {member.name}\n\t" \
                                               f"Member ID: {member.id}\n\t" \
                                               f"Discriminator: {member.discriminator}\n"

                                    txt += "```"

                                    if len(txt) > 1024:
                                        txt = txt[:1017] + "...```"

                                    embed.add_field(name=k, value=txt, inline=False)
                                else:
                                    pass

                            await message.channel.send(embed=embed)
                            return

                        elif cmd_s[0] == "deletemsg":
                            try:
                                x = int(cmd_s[1])
                                msg = []
                                async for y in message.channel.history(limit=x):
                                    msg.append(y)
                                print(f"DELETING {x} MESSAGES IN {message.channel.name}")
                                await message.channel.delete_messages(msg)
                                print("DELETED")
                            except IndexError:
                                print("No number given")
                                await message.channel.send(f"{message.author.mention}, I require a number"
                                                           " for how many messages you want me to delete\n"
                                                           "**Usage:** `!SARA deletemsg 5`")

                    else:
                        await message.channel.send(f"I dont understand your gibberish {message.author.mention}")
                        print(f"Command {cmd} has no reply value")

    async def load_quotes(self):
        ch = self.get_channel(self.quotes_channel_id)
        self.raw_quotes = await ch.history().flatten()

    def save_quotes(self):
        with open(self.quotes_file, 'w+', encoding='utf-8') as f:
            for q in self.raw_quotes:
                # print(f"{q.content}", type(q.content), q.content == '')
                if q.content != '':
                    f.write(q.content)
                    f.write('\n+=+=+=+=+=+=+=+=+=+=+=+=\n')

    def open_quotes(self):
        x = 0
        self.quotes = []
        with open(self.quotes_file, 'r', encoding='utf-8') as f:
            for line in f:
                if "+=+=+=+=+=+=+=+=+=+=+=+=" not in line:
                    try:
                        self.quotes[x] += line
                    except IndexError:
                        self.quotes.append(line)
                elif "+=+=+=+=+=+=+=+=+=+=+=+=" in line:
                    x += 1
        # print(len(self.quotes))
        # print(self.quotes[5])
        return

    def get_quotes(self):
        return self.quotes

    def generate_embed(self, title, desc, footer, img=message_list.SARA_PIC):
        embed = discord.Embed(title=f"SARA-SYSTEM - {title}",
                              colour=self.COLOR_PINK,
                              description=desc)

        embed.set_image(url=img)
        embed.set_thumbnail(url=message_list.SARA_PIC)
        embed.set_author(name="Sara", icon_url=message_list.SARA_PIC)
        embed.set_footer(text=f"SARA-SYSTEM - {footer}", icon_url=message_list.SARA_PIC)

        return embed


# Tuple, ICON LOOP
"""
                                elif isinstance(v, tuple):
                                    # ICON TUPLE
                                    txt = ""
                                    # print("type", type(v))
                                    if len(v) == 0:
                                        pass
                                    if len(v) > 8:
                                        x = 8
                                    else:
                                        x = len(v)

                                    for i in v[:x]:
                                        icon = {'name': i.name,
                                                'id': i.id,
                                                'available': i.available,
                                                'usable': i.is_usable,
                                                'url': i.url
                                                }

                                        if icon['usable']:
                                            txt += f"<:{icon['name']}:{icon['id']}>\n"
                                        else:
                                            txt += f":{icon['name']}:"

                                        txt += f"```" \
                                            f"Name: {icon['name']}\n" \
                                            f"URL: {icon['url']}\n" \
                                            f"```\n"

                                    print("txt:", txt)

                                    embed.add_field(name=k, value=txt, inline=False)
"""
