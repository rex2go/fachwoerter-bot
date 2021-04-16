class CommandHandler:

    def __init__(self, bot):
        self.bot = bot

    def handle_command(self, command, args=None):
        if command == 'exit':
            quit()

        # wip
        if args is None:
            args = []

        if command == 'add':
            word = input('Wort: ')

            if word == 'exit':
                return

            word = word.strip()

            if len(word) == 0:
                print('Ungültiges Wort')
                return

            if self.bot.is_present(word):
                print('Fehler: Duplikat')
                return

            description = input('Beschreibung: ')

            if description == 'exit':
                return

            description = description.strip()

            if len(description) == 0:
                print('Ungültige Beschreibung')
                return

            sql = "INSERT INTO `fachwoerter` (word, description) VALUES ('%s', '%s')" % (word, description)
            cursor = self.bot.connection.cursor(dictionary=True)
            cursor.execute(sql)
            self.bot.connection.commit()

            print('Hinzugefügt:')
            print(word + " - " + description)
