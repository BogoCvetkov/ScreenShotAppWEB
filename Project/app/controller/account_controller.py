from Project.model.all_models import AccountModel
from Project.app.schemas.account_schema import AccountSchema
from Project.app.controller.controller_factory import *

# /
get_all_accounts = get_all_factory(AccountModel,AccountSchema(many=True))
create_account = create_factory(AccountModel,AccountSchema())

# /<int:id>
get_account = get_one_factory(AccountModel,AccountSchema())
update_account = update_factory(AccountModel, AccountSchema(partial=True))
delete_account = delete_factory(AccountModel)