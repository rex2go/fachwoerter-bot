#!/usr/bin/python3
import sys

from fachwoerter_bot import FachwoerterBot
from command_handler import CommandHandler


if __name__ == '__main__':
    bot = FachwoerterBot()

    if '--tweet' in sys.argv:
        word = bot.get_fachwort(bot.cursor)
        bot.tweet(word)
        quit()

    print('Fachwörter Bot v0.1')

    command_handler = CommandHandler(bot)

    while True:
        command_input = input('> ').lower()
        command_parts = command_input.split(' ')
        command = command_parts[0]
        args = command_parts[1:]

        command_handler.handle_command(command, args)

