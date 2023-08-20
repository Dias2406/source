from django.urls import reverse
from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from account.models import Account
from student.models import Module, ModuleInfo, Behavioural, Cognitive, Affective
from teacher.models import Teacher
from teacher.views import behavioural_view, cognitive_view, affective_view

class TestUrls (SimpleTestCase):

    def test_behavioural_url_is_resolved(self):
        url = reverse('teacher:behavioural', kwargs={'slug': 'ecm2332'})
        self.assertEquals(resolve(url).func, behavioural_view)
    
    def test_cognitive_url_is_resolved(self):
        url = reverse('teacher:cognitive', kwargs={'slug': 'ecm2332'})
        self.assertEquals(resolve(url).func, cognitive_view)
    
    def test_affective_url_is_resolved(self):
        url = reverse('teacher:affective', kwargs={'slug': 'ecm2332'})
        self.assertEquals(resolve(url).func, affective_view)


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
        
        self.client.force_login(self.user)
        
    def test_behavioural_view(self):
        behavioural = reverse('teacher:behavioural', kwargs={'slug': 'ecm3442'})
        auth_user_response = self.client.get(behavioural)
        not_auth_user_response = self.notClient.get(behavioural)
        self.assertEquals(auth_user_response.status_code, 200)
        self.assertEquals(not_auth_user_response.status_code, 302)

    def test_cognitive_view(self):
        cognitive = reverse('teacher:cognitive', kwargs={'slug': 'ecm3442'})
        auth_user_response = self.client.get(cognitive)
        not_auth_user_response = self.notClient.get(cognitive)
        self.assertEquals(auth_user_response.status_code, 200)
        self.assertEquals(not_auth_user_response.status_code, 302)

    def test_affective_view(self):
        affective = reverse('teacher:affective', kwargs={'slug': 'ecm3442'})
        auth_user_response = self.client.get(affective)
        not_auth_user_response = self.notClient.get(affective)
        self.assertEquals(auth_user_response.status_code, 200)
        self.assertEquals(not_auth_user_response.status_code, 302)


    def test_404_on_nonexistent_module(self):
        response = self.client.get(reverse('teacher:behavioural', args=['nonexistent-module']))
        self.assertEqual(response.status_code, 404)