import psycopg2
import subprocess
import json
from sqlalchemy.engine.create import create_engine


class PostgresBaseManager:

    def __init__(self):

        self.database = 'dbf1adkng10ggr'
        self.user = 'tfwfynysjgpino'
        self.password = '7f967ef134475cba151b575567c9e79aba100923130517dfe674c12f6fca4a23'
        self.host = 'ec2-34-247-72-29.eu-west-1.compute.amazonaws.com'
        self.port = '5432'
        self.conn = self.connectServerPostgresDb()
        self.engine = create_engine("postgresql+psycopg2://" + '{username}:{password}@{host}:{port}/{database}'.format(username = self.user, password =self.password,
                                                                                                                       host = self.host, port = self.port, database = self.database))

    def connectServerPostgresDb(self):
        """
        :return: 連接 Heroku Postgres SQL 認證用
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
        :return: 測試是否可以連線到 Heroku Postgres SQL
        """
        cur = self.conn.cursor()
        cur.execute('SELECT VERSION()')
        results = cur.fetchall()
        print("Database version : {0} ".format(results))
        self.conn.commit()
        cur.close()

    def runsql(self,sql):
        """
        :return: 測試是否可以連線到 Heroku Postgres SQL
        """
        cur = self.conn.cursor()
        cur.execute(sql)

        self.conn.commit()
        cur.close()

    def create_weather_table(self):
        sql = '''CREATE TABLE weather_day
          (ID INT PRIMARY KEY     NOT NULL,
          DATA           TEXT    NOT NULL,
          LOCATION         REAL); '''
        self.runsql(sql)

    def insert_data(self):
        sql=""" INSERT INTO weather_day (ID, DATA , LOCATION) VALUES (1, 'Iphone12', 1100)
        """
        self.runsql(sql)


if __name__ == '__main__':
    postgres_manager = PostgresBaseManager()
    postgres_manager.runServerPostgresDb()
    postgres_manager.closePostgresConnection()
    # postgres_manager.create_weather_table()
    # postgres_manager.insert_data()


    # get-config
    # heroku_app_name = "hows-the-weather-tmmr"
    # raw_db_url = subprocess.run(
    #     ["heroku", "config:get", "DATABASE_URL", "--app", heroku_app_name],
    #     capture_output=True  # capture_output arg is added in Python 3.7
    # ).stdout.decode('utf8')
    # print(raw_db_url)