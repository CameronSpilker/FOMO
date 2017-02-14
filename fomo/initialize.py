import os, os.path, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()


#imports for our project
from django.core import management
from django.db import connection
from account.models import FomoUser
from catalog import models as cmod

from datetime import datetime
from decimal import Decimal

# ensure the user really wants to do this
areyousure = input('''
  You are about to drop and recreate the entire database.
  All data are about to be deleted.  Use of this script
  may cause itching, vertigo, dizziness, tingling in
  extremities, loss of balance or coordination, slurred
  speech, temporary zoobie syndrome, longer lines at the
  testing center, changed passwords in Learning Suite, or
  uncertainty about whether to call your professor
  'Brother' or 'Doctor'.

  Please type 'yes' to confirm the data destruction: ''')
if areyousure.lower() != 'yes':
    print()
    print('  Wise choice.')
    sys.exit(1)

# initialize the django environment
os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()


# drop and recreate the database tables
print()
print('Living on the edge!  Dropping the current database tables.')
with connection.cursor() as cursor:
    cursor.execute("DROP SCHEMA public CASCADE")
    cursor.execute("CREATE SCHEMA public")
    cursor.execute("GRANT ALL ON SCHEMA public TO postgres")
    cursor.execute("GRANT ALL ON SCHEMA public TO public")

# make the migrations and migrate
management.call_command('makemigrations')
management.call_command('migrate')



#create a Category
cat1 = cmod.Category()
cat1.codename = 'Kids'
cat1.name = 'Kids Toy Products'
cat1.save()

cat2 = cmod.Category()
cat2.codename = 'Rentals'
cat2.name = 'Rental Instruments'
cat2.save()

cat3 = cmod.Category()
cat3.codename = 'Strings'
cat3.name = 'String Instruments'
cat3.save()


# this is a query you pull from database
#cat2 = Category.objects.get(codename='strings')


#create a UniqueProduct
p0 = cmod.UniqueProduct()
p0.name = 'Guitar'
p0.category = cat3
p0.price = Decimal('99.50')#'' makes it a decimal,
p0.serial_number = 'ADI3834B32434D3432175'
p0.save()

p1 = cmod.UniqueProduct()
p1.name = 'Violin'
p1.category = cat3
p1.price = Decimal('685.50')#'' makes it a decimal,
p1.serial_number = 'IDFJOI73492OIDF'
p1.save()

p3 = cmod.UniqueProduct()
p3.name = 'Cello'
p3.category = cat3
p3.price = Decimal('474.50')#'' makes it a decimal,
p3.serial_number = '48548DIUFHOS98454'
p3.save()

#create a BulkProduct
p4 = cmod.BulkProduct()
p4.name = 'Kazoo'
p4.category = cat1
p4.price = Decimal('9.50')#'' makes it a decimal,
p4.quantity = 20
p4.reorder_trigger = 5
p4.reorder_quantity = 30
p4.save()

p5 = cmod.BulkProduct()
p5.name = 'Harmonica'
p5.category = cat1
p5.price = Decimal('6.59')#'' makes it a decimal,
p5.quantity = 13
p5.reorder_trigger = 2
p5.reorder_quantity = 20
p5.save()

p6 = cmod.BulkProduct()
p6.name = 'Recorder'
p6.category = cat1
p6.price = Decimal('2.50')#'' makes it a decimal,
p6.quantity = 10
p6.reorder_trigger = 3
p6.reorder_quantity = 15
p6.save()

#create a RentalProduct
p7 = cmod.RentalProduct()
p7.name = 'Tuba'
p7.category = cat2
p7.price = Decimal('499.99')
p7.serial_number = '903EROID8034DF'

p8 = cmod.RentalProduct()
p8.name = 'Trumpet'
p8.category = cat2
p8.price = Decimal('122.99')
p8.serial_number = '343DFOIDNFD'

p9 = cmod.RentalProduct()
p9.name = 'Trombone'
p9.category = cat2
p9.price = Decimal('342.99')
p9.serial_number = '454DFOSDOINDF'

# imports for our project


u1 = FomoUser()
u1.username = 'Cougar'
print(u1.first_name)
u1.first_name = 'Ricky'
u1.last_name = 'Bobby'
u1.set_password('1234')
u1.email = 'email'
u1.birthdate = datetime(2017, 1, 23, 1, 23)
u1.gender = 'M'
u1.shipping_address = 'shipping address'
u1.billing_address = 'billing address'
u1.last_login = datetime(2017, 1, 23, 1, 23)
u1.credit_card = '5678'
u1.cc_exp_date = datetime.now()
u1.cc_code = '123'
u1.date_joined = datetime.now()
u1.is_staff = True
u1.is_admin = True
u1.is_superuser
u1.save()

# u11 = FomoUser.objects.exclude(last_name = 'Smith')
# print(u11.last_name)
# for c in u11:
#     print(c, c.first_name, c.last_name)


u2 = FomoUser()
u2.first_name = 'Martha'
u2.last_name = 'Smith'
u2.username = 'msmith'
u2.set_password('password')
u2.email = 'mamaoffive@gmail.com'
u2.birthdate = datetime(2002, 12, 25, 0, 0)
u2.gender = 'F'
u2.shipping_address = '1234 Short Road'
u2.billing_address = '1234 Short Road'
u2.last_login = datetime(2017, 1, 15, 2, 33)
u2.date_joined = datetime(2017, 1, 1, 3, 14)
u2.credit_card = '12349841002'
u2.cc_code = '001'
u2.cc_exp_date = datetime(2019, 9, 1, 0, 0)
u2.save()


# print(u2.username)

u3 = FomoUser()
u3.username = 'username2'
u3.first_name = 'first_name2'
u3.last_name = 'last_name2'
u3.set_password('password')
u3.email = 'email2'
u3.last_login = datetime.now()
u3.date_joined = datetime.now()
u3.gender = 'M'
u3.birthdate = datetime.now()
u3.shipping_address = "Address for Number 2"
u3.billing_address = "Billing address for number 2"
u3.credit_card = "1234567812345678"
u3.cc_exp_date = datetime.now()
u3.cc_code = "1234"
u3.save()

# print(u3.username)


u4 = FomoUser()
u4.first_name = 'Tanner'
u4.last_name = 'Schmoekel'
u4.set_password('hellothere')
u4.username = 'tttt'
u4.email = 'tschmoek@gmail.com'
u4.billing_address = '123 hello st'
u4.shipping_address = '483 mystreet'
u4.birthdate = datetime.now()
u4.cc_exp_date = datetime.now()
u4.gender = 'm'
u4.date_joined = datetime.now()
u4.last_login = datetime.now()
u4.cc_code = '123'
u4.credit_card = "5555555"
u4.save();

# print(u4.username)
