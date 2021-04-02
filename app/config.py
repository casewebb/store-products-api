class Config(object):
    SECRET_KEY = '1234'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost/affiliate_store'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
