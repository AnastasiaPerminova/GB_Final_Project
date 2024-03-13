from django import forms
from . import models


class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30, label='Имя')
    Email = forms.EmailField(label='Email')
    Message = forms.CharField(max_length=500, label='Сообщение', widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))


class CourseForm(forms.ModelForm):
    class Meta:
        model = models.Course
        fields = ['course_name']


class AdminQuestionForm(forms.ModelForm):
    courseID = forms.ModelChoiceField(queryset=models.Course.objects.all(), label='Тест', empty_label="Название теста",
                                      to_field_name="id")
    question = forms.CharField(max_length=500, label="Вопрос",
                               required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                           'placeholder': "Например: What is the relation calculus?"}))

    marks = forms.IntegerField(min_value=1, label="Баллы", required=True)

    option1 = forms.CharField(max_length=500, label="Вариант 1", required=True,
                              widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                           'placeholder': "It is a kind of procedural language"}))

    option2 = forms.CharField(max_length=500, label="Вариант 2",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is a non-procedural language"}))
    option3 = forms.CharField(max_length=500, label="Вариант 3",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is a high-level language"}))
    option4 = forms.CharField(max_length=500, label="Вариант 4",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is Data Definition language"}))
    answer = forms.ChoiceField(choices=models.Question.cat, label="Правильный ответ")

    class Meta:
        model = models.Question
        fields = ['marks', 'question', 'option1', 'option2', 'option3', 'option4', 'answer']


class AdminUpdateQuestionForm(forms.ModelForm):
    question = forms.CharField(max_length=500, label="Вопрос",
                               required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                           'placeholder': "Например: What is the relation calculus?"}))

    marks = forms.IntegerField(min_value=1, label="Баллы", required=True)

    option1 = forms.CharField(max_length=500, label="Вариант 1", required=True,
                              widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                           'placeholder': "It is a kind of procedural language"}))

    option2 = forms.CharField(max_length=500, label="Вариант 2",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is a non-procedural language"}))
    option3 = forms.CharField(max_length=500, label="Вариант 3",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is a high-level language"}))
    option4 = forms.CharField(max_length=500, label="Вариант 4",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is Data Definition language"}))
    answer = forms.ChoiceField(choices=models.Question.cat, label="Правильный ответ")

    courseID = forms.ModelChoiceField(queryset=models.Course.objects.all(), label='Поменять тест',
                                      empty_label="Название теста",
                                      to_field_name="id")

    class Meta:
        model = models.Question
        fields = ['marks', 'question', 'option1', 'option2', 'option3', 'option4', 'answer', 'course']


class TeacherQuestionForm(forms.ModelForm):
    question = forms.CharField(max_length=500, label="Вопрос",
                               required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                           'placeholder': "Например: What is the relation calculus?"}))

    marks = forms.IntegerField(min_value=1, label="Баллы", required=True)

    option1 = forms.CharField(max_length=500, label="Вариант 1", required=True,
                              widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                           'placeholder': "It is a kind of procedural language"}))

    option2 = forms.CharField(max_length=500, label="Вариант 2",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is a non-procedural language"}))
    option3 = forms.CharField(max_length=500, label="Вариант 3",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is a high-level language"}))
    option4 = forms.CharField(max_length=500, label="Вариант 4",
                              required=True, widget=forms.Textarea(attrs={'rows': 3, 'cols': 50,
                                                                          'placeholder': "It is Data Definition language"}))
    answer = forms.ChoiceField(choices=models.Question.cat, label="Правильный ответ")

    class Meta:
        model = models.Question
        fields = ['marks', 'question', 'option1', 'option2', 'option3', 'option4', 'answer']
