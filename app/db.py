import os
import psycopg2

DATABASE_URL = 'postgres://hjvcpodskvyekp:497c476c89ed75e0ba9acf191963af65d63613f1d33069ec55d71ca97549f8c5@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/d2849pcb8trs9s'
    # os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
