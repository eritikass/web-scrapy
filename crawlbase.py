import mysql.connector
from mysql.connector import errorcode
import scrapy
import config

try:
    db = mysql.connector.connect(user=config.mysql_username, database=config.mysql_database, password=config.mysql_password, host=config.mysql_hostname)
except mysql.connector.Error as err:
    print "mysql connect error"
    print(err)
    exit(1)


class BaseSpider(scrapy.Spider):

    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,
        'CONCURRENT_REQUESTS_PER_IP': 1,

        'DOWNLOAD_DELAY': 3,
        'RANDOMIZE_DOWNLOAD_DELAY': True
    }

#    def __init__(self):

    def used(self, provider_id):
        query = "SELECT COUNT(id) FROM exploits WHERE provider = %s AND provider_id = %s "
        cursor = db.cursor()
        cursor.execute(query, (self.name, provider_id))
        for (res) in cursor:
            print "x:" + provider_id + ":" + self.name + ">" # + res[0]
            print res[0]
            return res[0] > 0

        print "db error select value(" + self.name + ", " + provider_id + ")"
        exit(1)

    def insert(self, provider_id, link, module, exploit, version):

        query = ("INSERT INTO `exploits` "
            " (`provider`, `provider_id`, `module`, `exploit`, `version`, `link`) "
            " VALUES (%(provider)s, %(provider_id)s, %(module)s, %(exploit)s, %(version)s, %(link)s) ")

        cursor = db.cursor()
        cursor.execute(query, {
            'provider': self.name,
            'provider_id': provider_id,
            'module': module,
            'exploit': exploit,
            'version': version,
            'link': link
        })

        db.commit()
        cursor.close()