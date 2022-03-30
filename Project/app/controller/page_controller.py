from Project.model.all_models import PageModel
from Project.app.schemas.page_schema import PageSchema
from Project.app.controller.controller_factory import *

# /
get_all_pages = get_all_factory( PageModel, PageSchema( many=True ) )
create_page = create_factory( PageModel, PageSchema() )

# /<int:id>
get_page = get_one_factory( PageModel, PageSchema() )
update_page = update_factory( PageModel, PageSchema( partial=True ) )
delete_page = delete_factory( PageModel )