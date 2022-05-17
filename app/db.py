import os
import psycopg2

DATABASE_URL = 'postgres://tfwfynysjgpino:7f967ef134475cba151b575567c9e79aba100923130517dfe674c12f6fca4a23@ec2-34-247-72-29.eu-west-1.compute.amazonaws.com:5432/dbf1adkng10ggr'

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
