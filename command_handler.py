import message_list
import insult_generator
import ron_swanson_quotes


def handle_command(cmd, author=None):
    print(f"Handling command '{cmd}'")
    msg = None
    cmd = cmd.strip()
    if cmd.lower() in message_list.GREETINGS:
        msg = "Hi :wave:"

    elif "insult" in cmd:
        cmd = cmd.split()
        try:
            if cmd[1] == message_list.MY_ID_MENTION:
                msg = "\"I love traps :heart:\" - " + author.mention
                # msg = insult_generator.get_random_insult() + " " + author.mention
            elif cmd[1] == message_list.SARA_MENTION:
                msg = "What was that? i might end up getting a technical glitch and banning you " + author.mention
            else:
                msg = insult_generator.get_random_insult() + " " + cmd[1]
        except IndexError:
            msg = "Good job retard, you are supposed to give a name as well... " + author.mention

    elif cmd == "swanson":
        msg = ron_swanson_quotes.get_swanson_quote()

    # elif "quote" in cmd:
    #   msg = message_list.QUOTES[rr.randint(0, len(message_list.QUOTES) - 1)]

    return msg


def mention_to_id(inp):
    inp = inp.replace("<@!", '')
    inp = inp.replace(">", '')
    inp = int(inp)
    return inp
