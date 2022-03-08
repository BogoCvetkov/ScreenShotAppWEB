from Project.config import DevelopmentConfig
from dotenv import load_dotenv

load_dotenv( ".env" )

from Project.app import create_app, return_to_db_pool

app = create_app( DevelopmentConfig )

# Returning the database connection to the connection pool after every request
app.teardown_appcontext( return_to_db_pool )

if __name__ == "__main__":
	app.run()