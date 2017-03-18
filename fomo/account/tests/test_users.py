from django.test import TestCase
from django.test import Client
from account import models as amod


class FomoUserTestCase(TestCase):
        # python manage.py test account/tests/

    def test_create_a_user(self):
        #test underscore very important
        u1 = amod.FomoUser()
        u1.username = 'Cougar'
        u1.first_name = 'Ricky'
        u1.last_name = 'Bobby'
        u1.email = 'email'
        u1.save()

        u2 = amod.FomoUser.objects.get(id=u1.id)

        self.assertEqual(u2.username, 'Cougar')
        self.assertEqual(u2.first_name, 'Ricky')
        self.assertEqual(u2.last_name, 'Bobby')
        self.assertEqual(u2.email, 'email')

    def test_login_a_user(self):
        u1 = amod.FomoUser()
        u1.username = "Jimmy"
        u1.set_password('1234')
        u1.save()

        c = Client()
        response = c.post('/account/login/', {'username': 'Jimmy', 'password': '1234'})
        response.status_code

        response = c.get('/account/myinfo')
        response.content

    def test_edit_a_user(self):
        u1 = amod.FomoUser()
        u1.username = 'Cougar'
        u1.first_name = 'Ricky'
        u1.last_name = 'Bobby'
        u1.email = 'email'
        u1.save()

        u1 = amod.FomoUser.objects.get(id=u1.id)

        u1.first_name = 'Cameron'
        u1.save()

        u1 = amod.FomoUser.objects.get(id=u1.id)

        self.assertEqual(u1.first_name, 'Cameron')

    def test_delete_a_user(self):
        u1 = amod.FomoUser()
        u1.username = 'Cougar'
        u1.first_name = 'Ricky'
        u1.last_name = 'Bobby'
        u1.email = 'email'
        u1.save()

        u1 = amod.FomoUser.objects.get(id=u1.id)

        u1.delete()

        if u1.DoesNotExist:
            print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>User Deleted')
        else:
            print('>>>>>USER NOT DELETED HAHA')



