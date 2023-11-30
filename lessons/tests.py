from django.test import TestCase
from django.db.models import QuerySet


from .models import Lesson
from pages.models import *
from users.models import CustomUser
# Create your tests here.
class LessonCRUDTest(TestCase):

    def setUp(self):
        self.num_lesson = 1
        self.num_week = 1
        self.is_session = False,
        
        self.day = DayOfWeek.objects.create(
            name = "Mon",
            order_number = 1,
        )
        self.university = University.objects.create(
            name = 'KPI',
            hyper_link = "test@gmail.com",
        )
        self.user = CustomUser.objects.create(
            university = self.university,
            is_stuff = True,
        )
        self.teacher = Teacher.objects.create(
            name = "Test_teacher",
            postion = "prof",
            hyper_link = "test@mail.com",
            university = self.university,
        )
        self.group = Group.objects.create(
            name = "ES-31",
            email = "es31@mail.com",
            university = self.university,
        )
        self.lesson = Lesson.objects.create(
            title = "Test",
            hyper_link = "test@gmail.com",
            lesson_type = 'Лек',
            university = self.user.university,
            author = self.user,
            day = self.day,
            num_lesson = self.num_lesson,
            num_week = self.num_week,
            is_session = False,         
        )
        self.lesson.group.set([self.group])
        self.lesson.teacher.set([self.teacher])
    
    def test_repeted_lessons(self):
        response = self.client.post(reverse('new_lesson'), data={
            'title':"Test2",
            'hyper_link':"test2@gmail.com",
            'lesson_type':'Прак',
            'university':self.user.university,
            'author': self.user,
            'day':self.day,
            'num_lesson':self.num_lesson,
            'num_week':self.num_week,
            'is_session':self.is_session,
            'group': self.group,
            'teacher':self.teacher,
        })
        self.assertRedirects(response, expected_url=reverse('new_lesson'), 
                             status_code=response.status_code, target_status_code=302)

    def test_delete_form(self):
        response = self.client.post(reverse('delete_lesson', args=[1,]))
        self.assertEqual(response.status_code, 302)
        self.assertRaises(callable=Lesson.objects.get(pk=1), 
                          expected_exception=Lesson.DoesNotExist)
        
    def test_creation_form(self):
        response = self.client.post(reverse('new_lesson'), data={
            'title':"Test2",
            'hyper_link':"test2@gmail.com",
            'lesson_type':'Прак',
            'university':self.user.university,
            'author':self.user,
            'day':self.day,
            'num_lesson':self.num_lesson + 1,
            'num_week':self.num_week + 1,
            'is_session':str(self.is_session),
            'group': self.group,
            'teacher':self.teacher,
        })
        self.assertEqual(response.status_code, 200)

    def test_detail_view(self):
        response = self.client.get(reverse('detail_lesson', args=[1,]))  
        self.assertEqual(response.status_code, 200)

    def test_edit_view(self):
        response = self.client.get(reverse('update_lesson', args=[1,]))  
        self.assertEqual(response.status_code, 200)
    