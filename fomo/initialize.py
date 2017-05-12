import os, os.path, sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'fomo.settings'
import django
django.setup()


#imports for our project
from django.core import management
from django.db import connection
from account import models as amod
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from catalog import models as cmod
from account.models import FomoUser



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

for p in Permission.objects.all():
    print(p.codename)



#you are always checking permissions
######does u1 have "add_fomouser" permission###################
g1 = Group()
g1.name = 'Owner'
g1.save()

g1.permissions.add(Permission.objects.get(codename=('add_product')))
g1.permissions.add(Permission.objects.get(codename=('change_product')))
g1.permissions.add(Permission.objects.get(codename=('delete_product')))

g1.permissions.add(Permission.objects.get(codename=('add_fomouser')))
g1.permissions.add(Permission.objects.get(codename=('change_fomouser')))
g1.permissions.add(Permission.objects.get(codename=('delete_fomouser')))


g1.save()

g2 = Group()
g2.name = 'Salesperson'
g2.save()

g2.permissions.add(Permission.objects.get(codename=('add_product')))
g2.permissions.add(Permission.objects.get(codename=('change_product')))
g2.permissions.add(Permission.objects.get(codename=('delete_product')))

g2.save()

g3 = Group()
g3.name = 'Admin'
g3.save()

g3.permissions.add(Permission.objects.get(codename=('add_fomouser')))
g3.permissions.add(Permission.objects.get(codename=('change_fomouser')))
g3.permissions.add(Permission.objects.get(codename=('delete_fomouser')))

g3.save()

g4 = Group()
g4.name = 'Customer'
g4.save()



#create a Category
cat1 = cmod.Category()
cat1.codename = 'Access'
cat1.name = 'Accessories'
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
p1 = cmod.UniqueProduct()
p1.name = 'Guitar'
p1.category = cat3
p1.price = Decimal('300')#'' makes it a decimal,
p1.serial_number = 'ADI383'
p1.picture = '/static/homepage/media/pic/guitar1.png'
p1.desc = 'This is a guitar that will give you the power to influence many. The strings can be plucked as fast as you can move them. Be prepared to rise above all others.'
p1.save()

pp1 = cmod.ProductPicture()
pp1.path1 = '/static/homepage/media/pic/guitar1.png'
pp1.path2 = '/static/homepage/media/pic/guitar2.png'
pp1.path3 = '/static/homepage/media/pic/guitar3.png'
pp1.path4 = '/static/homepage/media/pic/guitar4.png'
pp1.path5 = '/static/homepage/media/pic/guitar5.png'
pp1.product = p1
pp1.save()

p2 = cmod.UniqueProduct()
p2.name = 'Violin'
p2.category = cat3
p2.price = Decimal('1000')#'' makes it a decimal,
p2.serial_number = 'IDFJOI'
p2.picture = '/static/homepage/media/pic/violin1.png'
p2.desc = 'Has anybody ever told you, let me play you a sad song on my little Violin? Well now it is your turn to play them an amazing song on your normal size Violin.'
p2.save()


pp2 = cmod.ProductPicture()
pp2.path1 = '/static/homepage/media/pic/violin1.png'
pp2.path2 = '/static/homepage/media/pic/violin2.png'
pp2.path3 = '/static/homepage/media/pic/violin3.png'
pp2.path4 = '/static/homepage/media/pic/violin4.png'
pp2.product = p2
pp2.save()


p3 = cmod.UniqueProduct()
p3.name = 'Banjo'
p3.category = cat3
p3.price = Decimal('100')#'' makes it a decimal,
p3.serial_number = '48548D'
p3.picture = '/static/homepage/media/pic/banjo1.png'
p3.desc = '''Is there a better way to become more popular than to use a Banjo? I don't think so! Pick up this beauty and show it off to your friends in Arkansas.'''
p3.save()

pp3 = cmod.ProductPicture()
pp3.path1 = '/static/homepage/media/pic/banjo1.png'
pp3.path2 = '/static/homepage/media/pic/banjo2.png'
pp3.path3 = '/static/homepage/media/pic/banjo3.png'
pp3.path4 = '/static/homepage/media/pic/banjo4.png'
pp3.path5 = '/static/homepage/media/pic/banjo5.png'
pp3.product = p3
pp3.save()

#create a BulkProduct
p4 = cmod.BulkProduct()
p4.name = 'Amplifier'
p4.category = cat1
p4.price = Decimal('250')#'' makes it a decimal,
p4.quantity = 20
p4.reorder_trigger = 5
p4.reorder_quantity = 30
p4.picture = '/static/homepage/media/pic/amplifier1.png'
p4.desc = 'Get ready to plug your newly purchased electrical instrument into this magical Amplifier. You will ruins peoples ear drums...in a good way.'
p4.save()

pp4 = cmod.ProductPicture()
pp4.path1 = '/static/homepage/media/pic/amplifier1.png'
pp4.path2 = '/static/homepage/media/pic/amplifier2.png'
pp4.path3 = '/static/homepage/media/pic/amplifier3.png'
pp4.path4 = '/static/homepage/media/pic/amplifier4.png'
pp4.product = p4
pp4.save()

p5 = cmod.BulkProduct()
p5.name = 'Mic'
p5.category = cat1
p5.price = Decimal('115')#'' makes it a decimal,
p5.quantity = 25
p5.reorder_trigger = 2
p5.reorder_quantity = 20
p5.picture = '/static/homepage/media/pic/mic1.png'
p5.desc = '''You can record your lovely voice with this Mic. It's a microphone that captures all that is beautiful in your voice. '''
p5.save()

pp5 = cmod.ProductPicture()
pp5.path1 = '/static/homepage/media/pic/mic1.png'
pp5.path2 = '/static/homepage/media/pic/mic2.png'
pp5.path3 = '/static/homepage/media/pic/mic3.png'
pp5.path4 = '/static/homepage/media/pic/mic4.png'
pp5.product = p5
pp5.save()

p6 = cmod.BulkProduct()
p6.name = 'Case'
p6.category = cat1
p6.price = Decimal('20')#'' makes it a decimal,
p6.quantity = 50
p6.reorder_trigger = 3
p6.reorder_quantity = 15
p6.picture = '/static/homepage/media/pic/case1.png'
p6.desc = 'This is a Case, what more can we say. Keep your insturment looking fresh and new, as long as you put it in here.'
p6.save()

pp6 = cmod.ProductPicture()
pp6.path1 = '/static/homepage/media/pic/case1.png'
pp6.path2 = '/static/homepage/media/pic/case2.png'
pp6.path3 = '/static/homepage/media/pic/case3.png'
pp6.path4 = '/static/homepage/media/pic/case4.png'
pp6.product = p6
pp6.save()

#create a RentalProduct
p7 = cmod.RentalProduct()
p7.name = 'Saxophone'
p7.category = cat2
p7.price = Decimal('600')
p7.serial_number = '903ERO'
p7.picture = '/static/homepage/media/pic/saxophone1.png'
p7.desc = 'This Saxophone is for everyone. It will make you a better person, brother, mother or hedge fund account manager.'
p7.save()

pp7 = cmod.ProductPicture()
pp7.path1 = '/static/homepage/media/pic/saxophone1.png'
pp7.path2 = '/static/homepage/media/pic/saxophone2.png'
pp7.path3 = '/static/homepage/media/pic/saxophone3.png'
pp7.path4 = '/static/homepage/media/pic/saxophone4.png'
pp7.path5 = '/static/homepage/media/pic/saxophone5.png'
pp7.product = p7
pp7.save()

p8 = cmod.RentalProduct()
p8.name = 'Trumpet'
p8.category = cat2
p8.price = Decimal('550')
p8.serial_number = '343DFO'
p8.picture = '/static/homepage/media/pic/trumpet1.png'
p8.desc = 'There is not a high school band without a Trumpet. So pick up the best quality for the lowest price right here at FOMO.'
p8.save()

pp8 = cmod.ProductPicture()
pp8.path1 = '/static/homepage/media/pic/trumpet1.png'
pp8.path2 = '/static/homepage/media/pic/trumpet2.png'
pp8.path3 = '/static/homepage/media/pic/trumpet3.png'
pp8.path4 = '/static/homepage/media/pic/trumpet4.png'
pp8.product = p8
pp8.save()

p9 = cmod.RentalProduct()
p9.name = 'Trombone'
p9.category = cat2
p9.price = Decimal('750')
p9.serial_number = '454DFO'
p9.picture = '/static/homepage/media/pic/trombone1.png'
p9.desc = 'There are so many things I could say about this Trombone. But I will say you cannot find a better deal on the internet.'
p9.save()

pp9 = cmod.ProductPicture()
pp9.path1 = '/static/homepage/media/pic/trombone1.png'
pp9.path2 = '/static/homepage/media/pic/trombone2.png'
pp9.path3 = '/static/homepage/media/pic/trombone3.png'
pp9.path4 = '/static/homepage/media/pic/trombone4.png'
pp9.path5 = '/static/homepage/media/pic/trombone5.png'
pp9.product = p9
pp9.save()


#########SHOPPING CART U3##########

cart1 = amod.ShoppingItem()
cart1.fomouser = u3
cart1.product = p5
cart1.qty_ordered = 2
cart1.save()


cart2 = amod.ShoppingItem()
cart2.fomouser = u3
cart2.product = p1
cart2.save()

cart3 = amod.ShoppingItem()
cart3.fomouser = u3
cart3.product = p7
cart3.save()

cart4 = amod.ShoppingItem()
cart4.fomouser = u3
cart4.product = p6
cart4.qty_ordered = 4
cart4.save()

sc = amod.ShoppingItem.objects.filter(fomouser=3)


################################################
#########SHOPPING ITEM##########

cart11 = amod.ShoppingItem()
cart11.fomouser = u1
cart11.product = p5
cart11.qty_ordered = 10
cart11.save()

cart12 = amod.ShoppingItem()
cart12.fomouser = u1
cart12.product = p4
cart12.qty_ordered = 15
cart12.save()

sc = amod.ShoppingItem.objects.filter(fomouser=1)

#################################################

###########PRODUCT HISTORY FOR USER 1############################
phis11 = amod.ProductHistory()
phis11.product = p5
phis11.fomouser = u1
phis11.added = True
phis11.qty_ordered = 10
phis11.save()

phis12 = amod.ProductHistory()
phis12.product = p4
phis12.fomouser = u1
phis12.added = True
phis12.qty_ordered = 15
phis12.save()





########PRODUCT HISTORY FOR USER 3##############

phis1 = amod.ProductHistory()
phis1.product = p5
phis1.fomouser = u3
phis1.added = True
phis1.qty_ordered = 10
phis1.save()

phis2 = amod.ProductHistory()
phis2.product = p1
phis2.fomouser = u3
phis2.added = True
phis2.save()

phis3 = amod.ProductHistory()
phis3.product = p7
phis3.fomouser = u3
phis3.added = True
phis3.save()

phis4 = amod.ProductHistory()
phis4.product = p6
phis4.fomouser = u3
phis4.added = True
phis4.qty_ordered = 6
phis4.save()

###VIEWED BUT NOT ADDED#######
phis5 = amod.ProductHistory()
phis5.product = p4
phis5.fomouser = u3
phis5.added = True
phis5.save()


phis6 = amod.ProductHistory()
phis6.product = p9
phis6.fomouser = u3

phis6.added = True
phis6.save()

########VIEWED, ADDED, AND PURCHASED#######
phis7 = amod.ProductHistory()
phis7.product = p4
phis7.fomouser = u3
phis7.qty_ordered = 2
phis7.purchased = True
phis7.save()



history = amod.ProductHistory.objects.filter(fomouser=3)

