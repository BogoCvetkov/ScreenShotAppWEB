from Project.model.all_models import ScheduleModel
from Project.app.schemas.schedule_schema import ScheduleSchema
from Project.app.controller.controller_factory import *

# /
get_all_schedules = get_all_factory(ScheduleModel, ScheduleSchema(many=True))
create_schedule = create_factory(ScheduleModel, ScheduleSchema())

# /<int:id>
get_schedule  = get_one_factory( ScheduleModel, ScheduleSchema() )
update_schedule  = update_factory( ScheduleModel, ScheduleSchema( partial=True ) )
delete_schedule  = delete_factory( ScheduleModel )