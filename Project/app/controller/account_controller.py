from Project.model.all_models import AccountModel
from Project.app.schemas.account_schema import AccountsSchema,AccountSchema
from Project.app.controller.controller_factory import *

# /
get_all_accounts = get_all_factory(AccountModel,AccountsSchema(many=True))
create_account = create_factory(AccountModel,AccountsSchema())

# /<int:id>
get_account = get_one_factory(AccountModel,AccountSchema())
update_account = update_factory(AccountModel, AccountSchema(partial=True))
delete_account = delete_factory(AccountModel)