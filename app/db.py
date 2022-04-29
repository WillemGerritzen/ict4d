import os
import psycopg2

DATABASE_URL = 'postgres://tfwfynysjgpino:7f967ef134475cba151b575567c9e79aba100923130517dfe674c12f6fca4a23@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/dbf1adkng10ggr' \
               # 'postgres://hjvcpodskvyekp:497c476c89ed75e0ba9acf191963af65d63613f1d33069ec55d71ca97549f8c5@ec2-52-48-159-67.eu-west-1.compute.amazonaws.com:5432/d2849pcb8trs9s'
    # os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
