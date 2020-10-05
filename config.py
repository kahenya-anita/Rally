import os

class Config:
    '''
    General configuration parent class
    '''
    QUOTE_API_BASE_URL = 'http://quotes.stormconsultancy.co.uk/random.json'
    QUOTE_API_KEY = os.environ.get('QUOTE_API_KEY')
    SECRET_KEY = ('e1cb1d88ff8e0b')
    SQLALCHEMY_DATABASE_URI = 'postgres+psycopg2://yunidfbnwrdsxo:688063753c46cc99c32a873c4ebf92117fd5f70aaf7f3286fb278904bf4bd891@ec2-52-87-22-151.compute-1.amazonaws.com:5432/ddnsjnb7s86ukt'
    UPLOADED_PHOTOS_DEST ='app/static/photos'


class ProdConfig(Config):
    '''
    Production  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''
    pass


class DevConfig(Config):
    '''
    Development  configuration child class

    Args:
        Config: The parent configuration class with General configuration settings
    '''

    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig
}