from django.urls import path 
from .views import QuizViewSet, aquiz

urlpatterns = [  
    path('quizzes/', QuizViewSet.as_view(), name='quiz-list-create'),  
    path('', aquiz, name='aquiz'),
]