from import_export import resources
from .models import Assignment, Feedback

class AssignmentResource(resources.ModelResource):
    class Meta:
        model = Assignment

class FeedbackResource(resources.ModelResource):
    class Meta:
        model = Feedback