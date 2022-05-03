from Project.model.all_models import KeywordModel
from Project.app.schemas.keyword_schema import KeywordSchema
from Project.app.controller.controller_factory import *

# /
get_all_pages = get_all_factory( KeywordModel, KeywordSchema( many=True ) )
create_page = create_factory( KeywordModel, KeywordSchema() )

# /<int:id>
get_page = get_one_factory( KeywordModel, KeywordSchema() )
update_page = update_factory( KeywordModel, KeywordSchema( partial=True ) )
delete_page = delete_factory( KeywordModel )