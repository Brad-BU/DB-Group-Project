import os
import csi3335 as cfg


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    enginestr = "mysql+pymysql://" + cfg.mysql['user'] + ":" + cfg.mysql['password'] + "@" + cfg.mysql['location'] + ":3306/" + cfg.mysql['database']
    SQLALCHEMY_DATABASE_URI = enginestr
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
