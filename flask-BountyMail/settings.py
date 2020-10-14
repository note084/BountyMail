import os 

DB_USERNAME = 'Bounty'
DB_PASSWORD = 'OnePiece'
DB_DATABASE_NAME = 'BountyMail'
DB_HOST = os.getenv('IP','127.0.0.1')
APPLICATION_DIR = os.path.dirname(os.realpath(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = True

DEBUG = True

SECRET_KEY = '<0n3P13c3>'
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://%s:%s@%s/%s" % (
	DB_USERNAME, DB_PASSWORD,DB_HOST, DB_DATABASE_NAME)
STATIC_DIR = os.path.join(APPLICATION_DIR, 'static')

