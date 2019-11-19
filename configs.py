class Development:
    DEBUG = True
    SECRET_KEY ='!fmfm5$^*lm754%$£2"!!!'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:Jonitez1@127.0.0.1:5432/NCK_DB'
    SQLALCHEMY_TRACK_MODIFICATIONS= False

class Production:
    pass

