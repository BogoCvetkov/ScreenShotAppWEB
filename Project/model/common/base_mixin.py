from sqlalchemy import select, update, cast, String, VARCHAR
from Project.model.features.searching import filter_sort


class BaseMixin:

	def create( self, session ):
		session.add( self )
		return

	@classmethod
	def update( cls, session, id, data ):
		stmt = update( cls ).where( cls.id == id ).values(
			**data ).execution_options( synchronize_session="fetch" )
		result = session.execute( stmt )

		if result.rowcount < 1:
			raise Exception("Record not found")

	@classmethod
	def get_by_id( cls, session, id ):
		result = session.get( cls, id )
		return result

	@classmethod
	def search( cls, session, queries ):
		# Filter and sort results
		stmt = filter_sort(cls,queries)
		result = session.execute( stmt )
		return result.scalars().all()

	@classmethod
	def get_all( cls, session ):
		result = session.execute( select( cls ) )
		result = result.scalars().all()
		return result

	def delete( self, session ):
		session.delete( self )
		return