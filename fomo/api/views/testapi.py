from django.test import TestCase
import requests
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse, HttpResponseNotFound
import json


class Api_Test(TestCase):

    ret1 = requests.get('http://localhost:8000/api/product/?cat=acc')
    print('---------------------------------------------------')
    print('TEST 1, ?cat=acc SUCCESSFUL')
    print('---------------------------------------------------')
    print(ret1.json())
    print('---------------------------------------------------')

    ret2 = requests.get(
        'http://localhost:8000/api/product/?cat=222')
    print('---------------------------------------------------')
    print('TEST 2, ?cat=222 SUCCESSFUL')
    print('Expectation -- no category names nave 222, will return error')
    print('---------------------------------------------------')
    print(ret2.json())
    print('---------------------------------------------------')

    ret3 = requests.get(
        'http://localhost:8000/api/product/?cat=ren&min=1&max=1000&pname=s')
    print('---------------------------------------------------')
    print('TEST 3, ?cat=ren&min=1&max=1000&pname=s SUCCESSFUL')
    print('Expectation -- will return all products that have categories ren and min price 1 and max price 1000 with pname contains s')
    print('---------------------------------------------------')
    print(ret3.json())
    print('---------------------------------------------------')

    ret4 = requests.get(
        'http://localhost:8000/api/product/?pname=t&min_price=10')
    print('---------------------------------------------------')
    print('TEST 4, ?pname=t&min_price=10 SUCCESSFUL')
    print('Expectation -- will return all products that have t in the name with a min price of 10')
    print('---------------------------------------------------')
    print(ret4.json())
    print('---------------------------------------------------')

    ret5 = requests.get(
        'http://localhost:8000/api/product/?pname=trumpe&min_price=a')
    print('---------------------------------------------------')
    print('TEST 5, ?pname=trumpe&min_price=a ERROR')
    print('Expectation -- will not return any products because there is a letter in the min_price')
    print('---------------------------------------------------')
    print(ret5.json())
    print('---------------------------------------------------')

    ret6 = requests.get(
        'http://localhost:8000/api/product/?cat=i&max_price=500')
    print('---------------------------------------------------')
    print('TEST 6,?cat=i&max_price=500 SUCCESSFULL')
    print('Expectation --returns all products with categories with the letter i and max_price is 500')
    print('---------------------------------------------------')
    print(ret6.json())
    print('---------------------------------------------------')
