import mysql
import mysql.connector
import twitter

from dotenv import dotenv_values

config = dotenv_values(".env")


class FachwoerterBot:

    def __init__(self):
        self.connection = mysql.connector.connect(host=config['DB_HOST'], user=config['DB_USER'],
                                                  passwd=config['DB_PASSWORD'], db=config['DB_DATABASE'])
        self.cursor = self.get_cursor()

    def get_cursor(self):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT id FROM `cursor`")
        id = cursor.fetchall()[0]['id']
        cursor.close()

        return int(id)

    def update_cursor(self, id):
        cursor = self.connection.cursor(dictionary=True)
        sql = "UPDATE `cursor` SET id = %i" % int(id)

        cursor.execute(sql)
        self.connection.commit()

    def is_present(self, word):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `fachwoerter` WHERE word = '%s'" % word)
        cursor.fetchall()

        present = cursor.rowcount > 0

        cursor.close()

        return present

    def get_fachwort(self, id):
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM `fachwoerter` WHERE id = %i" % id)

        result = cursor.fetchall()

        if cursor.rowcount > 0:
            word = result[0]
        else:
            id = 1
            self.update_cursor(id)

            cursor.execute("SELECT * FROM `fachwoerter` WHERE id = '%s'" % id)
            word = cursor.fetchall()[0]

        cursor.close()

        self.update_cursor(id + 1)

        return word

    def tweet(self, word):
        content = word['word'] + " - " + word['description']

        api = twitter.Api(access_token_key=config['TWITTER_ACCESS_TOKEN_KEY'],
                          access_token_secret=config['TWITTER_ACCESS_TOKEN_SECRET'],
                          consumer_key=config['TWITTER_CONSUMER_KEY'],
                          consumer_secret=config['TWITTER_CONSUMER_KEY'])

        api.PostUpdate(content)

