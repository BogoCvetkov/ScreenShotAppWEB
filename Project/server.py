from dotenv import load_dotenv
import os
load_dotenv( ".env" )

from Project.config import DevelopmentConfig, ProductConfig
from Project.app.app import create_app, return_to_db_pool

if os.environ["ENV"] == "development":
	conf_file = DevelopmentConfig
else:
	conf_file = ProductConfig

app = create_app( conf_file )

# Returning the database connection to the connection pool after every request
app.teardown_appcontext( return_to_db_pool )

if __name__ == "__main__":
	app.run()