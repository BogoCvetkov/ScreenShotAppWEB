from flask.views import MethodView
from Project.app.controller import page_controller
from Project.app.auth import verify_jwt

class PagesRouter( MethodView ):

	decorators = [verify_jwt]

	def get( self ):
		return page_controller.get_all_pages()

	def post( self ):
		return page_controller.create_page()


class PageRouter( MethodView ):

	decorators = [verify_jwt]

	def get( self, id ):
		return page_controller.get_page( id )

	def patch( self, id ):
		return page_controller.update_page( id )

	def delete( self, id ):
		return page_controller.delete_page( id )