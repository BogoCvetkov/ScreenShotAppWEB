from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.orm import validates
from Project.model.common.base_mixin import BaseMixin
from sqlalchemy import select
from Project.model.DB import Base
from Project.app.auth import security

class UserModel( Base, BaseMixin ):
	__tablename__ = "users"

	id = Column( Integer, primary_key=True )
	email = Column( String, unique=True, nullable=False )
	username = Column( String, unique=True, nullable=False )
	password = Column( String, nullable=False )
	admin = Column( Boolean, default=False )
	last_changed = Column( DateTime )

	# Hash password upon instantiation
	@validates( "password" )
	def hash_password( self, key, value ):
		return security.bhash_value( value )

	def verify_password( self, submit_password ):
		return security.bcheck_hash( submit_password, self.password )

	@classmethod
	def find_by_email( cls, session, email ):
		user = session.scalars( select( cls ).where( cls.email == email ) ).first()
		return user