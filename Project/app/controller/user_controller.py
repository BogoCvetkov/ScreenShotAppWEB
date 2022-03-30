from Project.model.all_models import UserModel
from Project.app.schemas.user_chema import UserSchema
from Project.app.controller.controller_factory import *

# /
get_all_users = get_all_factory( UserModel, UserSchema( many=True, exclude=["password"] ) )
create_user = create_factory( UserModel, UserSchema() )

# /<int:id>
get_user = get_one_factory( UserModel, UserSchema( exclude=["password"] ) )
update_user = update_factory( UserModel,
                              UserSchema( exclude=["password", "confirm_password"], partial=True ) )
delete_user = delete_factory( UserModel )