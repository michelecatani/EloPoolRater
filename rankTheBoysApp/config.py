import os

class Config:
    SECRET_KEY = 'ef0009d6544657abfbcf4e318ee67d5d' ##os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db' ##os.environ.get('DATA_URI')
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mikecatanidev@gmail.com' ##os.environ.get('MAIL_USER')
    MAIL_PASSWORD = 'Figcjuve7&'  ##os.environ.get('MAIL_PASSWORD')
