from Project.app.model.common.base_mixin import BaseMixin
from Project.app.model import Base
from sqlalchemy import Column, String, Integer, DateTime, select
from datetime import datetime, timedelta
from Project.app.auth.security import hashed_token


class ResetPassModel( Base, BaseMixin ):
	__tablename__ = "reset_pass"

	id = Column( Integer, primary_key=True )
	token = Column( String, unique=True, nullable=False )
	expires_at = Column( DateTime, nullable=False )
	email = Column( String, unique=True, nullable=False )

	@classmethod
	def generate_token( cls, session, email ):
		cur_token = session.scalars( select( cls ).where( cls.email == email ) ).first()
		new_token = hashed_token()
		exp = datetime.now() + timedelta( minutes=10 )
		if cur_token:
			cur_token.token = new_token
			cur_token.expires_at = exp
		else:
			cls( token=new_token, expires_at=exp, email=email ).create( session )

		return new_token

	@classmethod
	def find_by_token( cls, session, token ):
		result = session.scalars( select( cls ).where( cls.token == token ) ).first()
		return result

	def has_expired( self ):
		return datetime.now() > self.expires_at