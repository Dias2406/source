from django.urls import reverse
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from account.models import Account
from student.models import Module, ModuleInfo, Behavioural, Cognitive, Affective
from teacher.models import Teacher
from personal.views import home_screen_view

class TestUrls (SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func, home_screen_view)

class TestViews (TestCase):

    def setUp(self):
        self.client = Client()
        self.notClient = Client()
        self.user = Account.objects.create(email='test@exeter.ac.uk', username='teacher',password='12345', account_id = "0912091", is_teacher = True)
        self.teacher = Teacher.objects.create(account = self.user)
        self.student = Account.objects.create(email='student@exeter.ac.uk', username='student', password='12345', account_id = "091209122")
        self.module = Module.objects.create(code='ecm3442', name='test', teacher = self.teacher,ca_weight = 0.5, exam_weight=0.5)
        self.module_info = ModuleInfo.objects.create(module = self.module, student = self.student)
        self.behavioural = Behavioural.objects.create(week = 1, attendance = 80, module = self.module, student = self.student)
        self.cognitive = Cognitive.objects.create(module = self.module, student = self.student, coursework = 90, exam = 50)
        self.affective = Affective.objects.create(week = 1, student = self.student, module = self.module, emoji = "1", text = "test")
        
        self.client.force_login(self.student)
        
    def test_home_view(self):
        behavioural = reverse('home')
        auth_user_response = self.client.get(behavioural)
        not_auth_user_response = self.notClient.get(behavioural)
        self.assertEquals(auth_user_response.status_code, 200)
        self.assertEquals(not_auth_user_response.status_code, 302)
