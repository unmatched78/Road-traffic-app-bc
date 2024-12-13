from django.shortcuts import render  
from django.contrib.auth.models import User  
from rest_framework import generics, status  
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated, AllowAny  
from .serializers import UserSerializer, QuizSerializer  
from .models import Aquiz, Zanswer, CorrectQuestion  
import random  
from rest_framework import generics, status  
from rest_framework.response import Response  
from rest_framework.permissions import IsAuthenticated  
import random  

class QuizViewSet(generics.ListCreateAPIView):  
    permission_classes = [IsAuthenticated]  # Protect this view  
    serializer_class = QuizSerializer  # Specify your serializer class if required  

    def list(self, request):  
        # Get questions that the user has not answered correctly  
        answered_questions = CorrectQuestion.objects.filter(user=request.user).values_list('question', flat=True)  
        questions = Aquiz.objects.exclude(id__in=answered_questions)  
        #print(questions)
        if not questions.exists():  
            return Response({'error': 'No more questions available'}, status=status.HTTP_404_NOT_FOUND)  

        # Randomly select questions, making sure to limit the count  
        random_questions = random.sample(list(questions), min(20, questions.count()))
        print(random_questions)
        serializer = QuizSerializer(random_questions, many=True)  
        return Response(serializer.data)  

    def create(self, request):  
        user = request.user  
        answered_questions = CorrectQuestion.objects.filter(user=user).values_list('question', flat=True)  
        response_data = []  # To store the results for each question  
        print(response_data) 
        # Validate incoming data  
        answers = request.data.get('answers', [])
        print(answers) 
        if not isinstance(answers, list):  
            return Response({'error': 'Answers should be a list.'}, status=status.HTTP_400_BAD_REQUEST)  

        for answer in answers:  
            question_id = answer.get('question_id')  
            selected_answer_id = answer.get('selected_answer_id')  

            # Validation: check if the user has already answered this question correctly  
            if question_id in answered_questions:  
                return Response({'error': f'You have already answered question {question_id} correctly.'},   
                                status=status.HTTP_400_BAD_REQUEST)  

            # Find the correct answer for the question  
            correct_answer = Zanswer.objects.filter(question_id=question_id, is_correct=True).first()  

            if not correct_answer:  
                return Response({'error': f'No correct answer found for question {question_id}'},   
                                status=status.HTTP_400_BAD_REQUEST)  

            # Determine if the selected answer is correct
            print(f"Correct answer ID: {correct_answer.id} (type: {type(correct_answer.id)})")  
            print(f"Selected answer ID: {selected_answer_id} (type: {type(selected_answer_id)})")
            # Save the user's answer if it was correct
             # Convert selected_answer_id to int if it's a string  
            #selected_answer_id_as_int = int(selected_answer_id) if selected_answer_id.isdigit() else None 
            #is_correct if correct_answer.id == selected_answer_id else False
            is_correct = True if correct_answer.id == selected_answer_id else False
            response_data.append({  
                'question_id': question_id,  
                'selected_answer_id': selected_answer_id,  
                'correct_answer_id': correct_answer.id,
                #'correct_answer_image_base64': correct_answer.answer_image_base64,  
                'is_correct': is_correct  
            })  

            if is_correct:  
                CorrectQuestion.objects.get_or_create(question=correct_answer.question, user=user)  

        return Response({  
            'status': 'Answers submitted',  
            'results': response_data  
        }, status=status.HTTP_201_CREATED)
class CreateUserView(generics.CreateAPIView):  
    queryset = User.objects.all()  
    serializer_class = UserSerializer  
    permission_classes = [AllowAny]
def aquiz(request):
    list=Zanswer.objects.all()

    return render(request, 'home.html',{"list": list})