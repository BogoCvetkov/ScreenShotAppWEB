import os
from datetime import timedelta


class DevelopmentConfig:
	TESTING = True
	DEBUG = True
	ENV = "development"
	JSON_SORT_KEYS = False
	JWT_SECRET_KEY = os.environ["JWT_SECRET"]
	JWT_TOKEN_LOCATION = "cookies"
	JWT_ACCESS_TOKEN_EXPIRES = timedelta( minutes=int( os.environ["JWT_EXP_TIME"] ) )
	JWT_COOKIE_SECURE = False
	JWT_COOKIE_SAMESITE = "Strict"
	JWT_ACCESS_COOKIE_NAME = "jwt"
	JWT_COOKIE_CSRF_PROTECT = False


class ProductConfig:
	TESTING = False
	DEBUG = False
	ENV = "production"
	JSON_SORT_KEYS = False
	JWT_SECRET_KEY = os.environ["JWT_SECRET"]
	JWT_TOKEN_LOCATION = "cookies"
	JWT_ACCESS_TOKEN_EXPIRES = timedelta( minutes=int( os.environ["JWT_EXP_TIME"] ) )
	JWT_COOKIE_SECURE = True
	JWT_COOKIE_SAMESITE = "Strict"
	JWT_ACCESS_COOKIE_NAME = "jwt"
	JWT_COOKIE_CSRF_PROTECT = True