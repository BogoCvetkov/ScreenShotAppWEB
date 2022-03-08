from datetime import timedelta


class DevelopmentConfig:
	TESTING = True
	DEBUG = True
	ENV = "development"
	JSON_SORT_KEYS = False


class ProductConfig:
	TESTING = False
	DEBUG = False
	ENV = "production"
	JSON_SORT_KEYS = False