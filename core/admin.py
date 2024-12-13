from django.contrib import admin  
from .models import *

class AnswerInline(admin.TabularInline):  
    model = Zanswer  
    extra = 4 # Number of empty answer forms to display by default  
    fields = ('answer_text', 'is_correct', 'answer_image')  
    # You can customize the fields displayed in the admin here  

class QuizAdmin(admin.ModelAdmin):  
    inlines = [AnswerInline]  
    list_display = ('question',)  # Customize as needed  

# Register the Quiz model with the custom admin  

admin.site.register(Zanswer) # Register this model as needed
admin.site.register(Aquiz, QuizAdmin)  
admin.site.register(CorrectQuestion)  # Register this model as needed