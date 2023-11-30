from django.test import TestCase
from django.contrib.auth import get_user_model


from .models import *

# Create your tests here.
class GroupCRUDTest(TestCase):
    def setUp(self) -> None:
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
        self.user = get_user_model().objects.create(
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
    
    def test_create_group_view(self):
        path = reverse('new_group', args=[])
        response = self.client.post(path, data={
            'name': 'ES-31mn',
            'email': 'es31@mail.com',
            'university': self.user.university,
        })

        self.assertEqual(response.status_code, 302)

    def test_detail_group_view(self):
        path = reverse('detail_group', args=[1,])
        response = self.client.get(path=path)

        self.assertEqual(response.status_code, 200)

    def test_edit_group_view(self):
        path = reverse('edit_group', args=[1,])
        response = self.client.post(path=path, data={
            'name': 'ES-31mp',
            'email': 'es31@mail.com',
            'university': self.user.university,
        })

        self.assertEqual(response.status_code, 302)

    def test_delete_group_view(self):
        path = reverse('delete_group', args=[1,])
        response = self.client.post(path=path)

        self.assertEqual(response.status_code, 302)

class TeacherCRUDTest(GroupCRUDTest, TestCase):

    def setUp(self):
        super().setUp()
    
    def test_create_teacher_view(self):
        path = reverse('new_teacher', args=[])
        response = self.client.post(path, data={
            'name': 'Kyryk',
            'postion': 'prof',
            'hyper_link': 'kyryk@mail.com',
            'university': self.user.university,
        })

        self.assertEqual(response.status_code, 302)

    def test_detail_teacher_view(self):
        path = reverse('detail_teacher', args=[1,])
        response = self.client.get(path=path)

        self.assertEqual(response.status_code, 200)

    def test_edit_teacher_view(self):
        path = reverse('edit_teacher', args=[1,])
        response = self.client.post(path=path, data={
            'name': 'Kyryk Mudachok',
            'postion': 'st. vyk',
            'hyper_link': 'kyryk@mail.com',
            'university': self.user.university,
        })

        self.assertEqual(response.status_code, 302)

    def test_delete_teacher_view(self):
        path = reverse('delete_teacher', args=[1,])
        response = self.client.post(path=path)

        self.assertEqual(response.status_code, 302)



class PagesViewsTest(GroupCRUDTest, TestCase):

    def setUp(self):
        super().setUp()


    def test_get_group_schedules_view(self):
        path = reverse('get_group')
        response = self.client.get(path=path, data={
            'is_session': 1,
            'university': 'KPI',
            'group': "ES-31",
        })

        self.assertEqual(response.status_code, 200)

    def test_get_teacher_schedules_view(self):
        path = reverse('get_teacher')
        response = self.client.get(path=path, data={
            'is_session': 1,
            'university': 'KPI',
            'teacher': "Test_teacher",
        })

        self.assertEqual(response.status_code, 200)

    def test_check_instanse_view(self):
        path = reverse('search_model')
        response = self.client.get(path=path, data={
            'name': "Test_teacher",
            'model': 'Teacher',
        })

        self.assertEqual(response.status_code, 200)

    def test_get_table_view(self):
        path = reverse('get_table')
        response = self.client.get(path=path, data={
            'model': 'Teacher',
        })

        self.assertEqual(response.status_code, 200)

    def test_week_config_view(self):
        path = reverse('week_config')
        response = self.client.post(path=path, data={
            'week': '2',
        })
        from .views import NUM_WEEK
        self.assertEqual(NUM_WEEK, 2)
        self.assertEqual(response.status_code, 200)