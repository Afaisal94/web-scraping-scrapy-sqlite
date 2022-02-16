# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import sqlite3

class SQLlitePipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect("coronavirus.db")
        self.c = self.connection.cursor()
        try:
            self.c.execute('''
                CREATE TABLE coronavirus(
                    country_name TEXT,
                    coronavirus_cases TEXT,
                    deaths TEXT,
                    recovered TEXT
                )

            ''')
            self.connection.commit()
        except sqlite3.OperationalError:
            pass

    def close_spider(self, spider):
        self.connection.close()

    def process_item(self, item, spider):
        self.c.execute('''
            INSERT INTO coronavirus (country_name,coronavirus_cases,deaths,recovered) VALUES(?,?,?,?)

        ''', (
            item.get('country_name'),
            item.get('coronavirus_cases'),
            item.get('deaths'),
            item.get('recovered')
        ))
        self.connection.commit()
        return item
