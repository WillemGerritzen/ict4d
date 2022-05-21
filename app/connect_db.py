import psycopg2
import subprocess
import json
from sqlalchemy.engine.create import create_engine
from datetime import datetime
from app.get_weather_info import *


class PostgresBaseManager:

    def __init__(self):

        self.database = 'dbf1adkng10ggr'
        self.user = 'tfwfynysjgpino'
        self.password = '7f967ef134475cba151b575567c9e79aba100923130517dfe674c12f6fca4a23'
        self.host = 'ec2-34-247-72-29.eu-west-1.compute.amazonaws.com'
        self.port = '5432'
        self.conn = self.connectServerPostgresDb()
        self.engine = create_engine("postgresql+psycopg2://" + '{username}:{password}@{host}:{port}/{database}'.format(username=self.user, password=self.password,
                                                                                                                       host=self.host, port=self.port, database=self.database))

    def connectServerPostgresDb(self):
        """
        :return: Connect Heroku Postgres SQL 
        """

        conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port)
        return conn

    def closePostgresConnection(self):
        """
        :return: 關閉資料庫連線使用
        """
        self.conn.close()

    def runServerPostgresDb(self):
        """
        :return: Test if connect Heroku Postgres SQL success
        """
        cur = self.conn.cursor()
        cur.execute('SELECT VERSION()')
        results = cur.fetchall()
        print("Database version : {0} ".format(results))
        self.conn.commit()
        cur.close()

    def runsql(self, sql):
        """
        :return: Test if connect Heroku Postgres SQL success
        """
        cur = self.conn.cursor()
        cur.execute(sql)

        self.conn.commit()
        cur.close()

    def create_table(self, sql):
        self.runsql(sql)

    def insert_data_locationDate(self, location, date):
        sql = """ INSERT INTO location_date_combine (LOCATION, DATE ) VALUES (%s,%s) RETURNING id """ 
        record_to_insert = (location, date)
        cur=self.conn.cursor()
        self.conn.commit()
        cur.execute(sql, record_to_insert)
        self.conn.commit()
        count = cur.rowcount
        print(count, "Record inserted successfully into LocationDate table")
        id = cur.fetchone()[0]
        return id

    def get_alert_info(self):
        today = str(datetime.now().date())
        sql = """ SELECT * FROM weather_alert \
                    WHERE DATE = '%s'
                    """ %(today)
        cur = self.conn.cursor()
        cur.execute(sql)
        info = cur.fetchone()
        if not info:
            info = self.check_alert_info()
        return info[2]

    def check_alert_info(self):
        init_database()
        info = process_alert_info()
        return info


    def select_data_locationDate(self, id):
        sql = """ SELECT * FROM location_date_combine \
            WHERE ID = %s
            """ % (id)
        cur = self.conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()
        return row

    def select_data_day_weather(self,location,date):
        sql = """ SELECT * FROM day_weather \
            WHERE Location = %s AND Date = %s
            """
        record_to_insert = (location, date)
        cur = self.conn.cursor()
        cur.execute(sql,record_to_insert)
        self.conn.commit()
        row = cur.fetchone()
        count = cur.rowcount
        print(count, "Record inserted successfully into LocationDate table")
        return row


#
if __name__ == '__main__':
    postgres_manager = PostgresBaseManager()
    postgres_manager.runServerPostgresDb()
    info = postgres_manager.get_alert_info()
    print(info)


    # locationDateTableSql = '''
    # CREATE TABLE location_date_combine
    #               (ID SERIAL PRIMARY KEY  NOT NULL,
    #               DATE           TEXT    NOT NULL,
    #               LOCATION         TEXT    NOT NULL); '''
    # postgres_manager.create_table(sql=locationDateTableSql)

    # AlertSql = '''CREATE TABLE weather_alert
    #                   (ID SERIAL PRIMARY KEY  NOT NULL,
    #                   DATE      text   NOT NULL,
    #                   Info        VARCHAR    NOT NULL); '''

    # AlertSql = """ALTER TABLE day_weather ALTER COLUMN date TYPE text;"""
    # sql = """delete from day_weather"""
    # postgres_manager.create_table(sql=sql)

    postgres_manager.closePostgresConnection()


    # postgres_manager.select_data(2)
    # postgres_manager.closePostgresConnection()
    #
    # get-config
    # heroku_app_name = "hows-the-weather-tmmr"
    # raw_db_url = subprocess.run(
    #     ["heroku", "config:get", "DATABASE_URL", "--app", heroku_app_name],
    #     capture_output=True  # capture_output arg is added in Python 3.7
    # ).stdout.decode('utf8')
    # print(raw_db_url)
