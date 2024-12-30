# serializers.py  
from django.contrib.auth.models import User
from rest_framework import serializers  
from .models import Aquiz, Zanswer, CorrectQuestion  
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
 
from cloudinary.forms import CloudinaryFileField
class AnswerSerializer(serializers.ModelSerializer):  
    answer_image=CloudinaryFileField()

    class Meta:  
        model = Zanswer  
        fields = ['id', 'answer_text', 'is_correct', 'answer_image']  

class QuizSerializer(serializers.ModelSerializer):  
    answers = AnswerSerializer(many=True, read_only=True)  
    question_image=CloudinaryFileField()


    class Meta:  
        model = Aquiz  
        fields = ['id', 'question','question_image', 'answers']  

class CorrectQuestionSerializer(serializers.ModelSerializer):  
    class Meta:  
        model = CorrectQuestion  
        fields = ['question', 'user', 'created_at']
