from flask.views import MethodView
from Project.app.controller import keyword_controller
from Project.app.auth.jwt import verify_jwt

class KeywordsRouter( MethodView ):

	decorators = [verify_jwt]

	def get( self ):
		return keyword_controller.get_all_pages()

	def post( self ):
		return keyword_controller.create_page()


class KeywordRouter( MethodView ):

	decorators = [verify_jwt]

	def get( self, id ):
		return keyword_controller.get_page( id )

	def patch( self, id ):
		return keyword_controller.update_page( id )

	def delete( self, id ):
		return keyword_controller.delete_page( id )