#resources.py
from import_export import resources
from app.models import Site
 
class SiteListResource(resources.ModelResource):
    class Meta:
        model = Site

# class WorkPending_resource(resources.ModelResource):
#     class Meta:
#         model = WorkPending
#         skip_unchanged = True
#         report_skipped = False
#         fields = ('workorder','completedwork')

    
        


