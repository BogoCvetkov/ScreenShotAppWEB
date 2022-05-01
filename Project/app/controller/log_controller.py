from Project.model.all_models import LogModel
from Project.app.schemas.log_schema import LogSchema
from Project.app.controller.controller_factory import *

# /
get_all_logs = get_all_factory(LogModel,LogSchema(many=True))

# /<int:id>
delete_log = delete_factory(LogModel)