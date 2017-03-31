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
# add_fomouser
# change_fomouser
# delete_fomouser
# add_logentry
# change_logentry
# delete_logentry
# add_group
# change_group
# delete_group
# add_permission
# change_permission
# delete_permission
# add_bulkproduct
# change_bulkproduct
# delete_bulkproduct
# add_category
# change_category
# delete_category
# add_product
# change_product
# delete_product
# add_rentalproduct
# change_rentalproduct
# delete_rentalproduct
# add_uniqueproduct
# change_uniqueproduct
# delete_uniqueproduct
# add_contenttype
# change_contenttype
# delete_contenttype
# add_session
# change_session
# delete_session


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




# for p in Permission.objects.all()
#     print(p.codename, '>', p.name)
#
#
#

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
p1.price = Decimal('100')#'' makes it a decimal,
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
p2.price = Decimal('100')#'' makes it a decimal,
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
p4.price = Decimal('1')#'' makes it a decimal,
p4.quantity = 100
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
p5.price = Decimal('1')#'' makes it a decimal,
p5.quantity = 13
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
p6.price = Decimal('1')#'' makes it a decimal,
p6.quantity = 10
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
p7.price = Decimal('50')
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
p8.price = Decimal('50')
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
p9.price = Decimal('50')
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

# imports for our project


u1 = amod.FomoUser()
u1.username = 'Cougar'
print(u1.first_name)
u1.first_name = 'Ricky'
u1.last_name = 'Bobby'
u1.set_password('1234')
u1.email = 'email'
u1.birthdate = datetime(2017, 1, 23, 1, 23)
u1.gender = 'M'
u1.shipping_address = 'shipping address'
u1.zip_code = '12345'
u1.country = 'USA'
u1.billing_address = 'billing address'
u1.last_login = datetime(2017, 1, 23, 1, 23)
u1.credit_card = '5678'
u1.cc_exp_date = datetime.now()
print('>>>>>>>>>', u1.cc_exp_date)
u1.cc_code = '123'
u1.date_joined = datetime.now()
# u1.is_staff = True
# u1.is_admin = True
# u1.is_superuser = True
u1.save()

u1.groups.add(g1)



# p = Permission.objects.get(codename=('add_fomouser'))
# u1.user_permissions.add(p)

# for p in Permission.objects.all():
#     u1.user_permissions.add(p)

# u11 = FomoUser.objects.exclude(last_name = 'Smith')
# print(u11.last_name)
# for c in u11:
#     print(c, c.first_name, c.last_name)


u2 = amod.FomoUser()
u2.first_name = 'Martha'
u2.last_name = 'Smith'
u2.username = 'admin'
u2.set_password('admin')
u2.email = 'mamaoffive@gmail.com'
u2.birthdate = datetime(2002, 12, 25, 0, 0)
u2.gender = 'F'
u2.shipping_address = '1234 Short Road'
u2.zip_code = '12345'
u2.country = 'USA'
u2.billing_address = '1234 Short Road'
u2.last_login = datetime(2017, 1, 15, 2, 33)
u2.date_joined = datetime(2017, 1, 1, 3, 14)
u2.credit_card = '12349841002'
u2.cc_code = '001'
u2.cc_exp_date = datetime(2019, 9, 1, 0, 0)
u2.save()

u2.groups.add(g3)
# print(u2.username)

u3 = amod.FomoUser()
u3.username = 'customer'
u3.first_name = 'Cameron'
u3.last_name = 'Spilker'
u3.set_password('customer')
u3.email = 'email2'
u3.last_login = datetime.now()
u3.date_joined = datetime.now()
u3.gender = 'M'
u3.birthdate = datetime.now()
u3.shipping_address = "1008 south 500 west provo, utah 84601"
u3.zip_code = '12345'
u3.country = 'USA'
u3.billing_address = "Billing address for number 2"
u3.credit_card = "1234567812345678"
u3.cc_exp_date = datetime.now()
u3.cc_code = "1234"
u3.save()

u3.groups.add(g4)

# print(u3.username)


u4 = amod.FomoUser()
u4.first_name = 'Tanner'
u4.last_name = 'Schmoekel'
u4.set_password('sales')
u4.username = 'sales'
u4.email = 'tschmoek@gmail.com'
u4.billing_address = '123 hello st'
u4.zip_code = '12345'
u4.country = 'USA'
u4.shipping_address = '483 mystreet'
u4.birthdate = datetime.now()
u4.cc_exp_date = datetime.now()
u4.gender = 'm'
u4.date_joined = datetime.now()
u4.last_login = datetime.now()
u4.cc_code = '123'
u4.credit_card = "5555555"
u4.save();

u4.groups.add(g2)

# print(u4.username)


#########SHOPPING ITEM##########

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
print('>>>>>>>>>>>>>>>>>>>>>>CART>>>>>>>>>>>>>>>>')
for p in sc:
  print(p.product.name)
  print(p.qty_ordered)
  print(p.id)


print('>>>>>>>>>>>>>>>>END CART<<<<<<<<<<<<<<<<<<')
  ########PRODUCT HISTORY##############

phis1 = amod.ProductHistory()
phis1.product = p5
phis1.fomouser = u3
phis1.added = True
phis1.qty_ordered = 10
phis1.in_cart = True
phis1.save()

phis2 = amod.ProductHistory()
phis2.product = p1
phis2.fomouser = u3
phis2.added = True
phis2.in_cart = True
phis2.save()

phis3 = amod.ProductHistory()
phis3.product = p7
phis3.fomouser = u3
phis3.added = True
phis3.in_cart = True
phis3.save()

phis4 = amod.ProductHistory()
phis4.product = p6
phis4.fomouser = u3
phis4.added = True
phis4.qty_ordered = 6
phis4.in_cart = True
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


for h in history:
  print('>>>>>>>>>>>>>>>>>>')
  print('first name: ', h.fomouser.first_name)
  print('product name: ', h.product.name)
  print('qty ordered: ', h.qty_ordered)
  print('viewed product: ', h.viewed)
  print('added product: ', h.added)
  print('purchased product: ', h.purchased)
  print('product in cart: ', h.in_cart)
  print('datetime viewed: ', h.view_datetime)
  print()


#######################Convienece Functions##########################


######CART############
cart = u3.get_cart()

for c in cart:
  print(c.product.name)
  print(c.qty_ordered)


########LAST5#########
last5 = u3.last5()

for l in last5:
  print(l.name)
  print('>>>end last5')


####SUBTOTAL############
print(u3.calc_subtotal())


#####Shipping#########
print(u3.calc_shipping())


########TAX########
print(u3.calc_tax())


#####TOTAL#########
print(u3.calc_total())

###Cart Count##
print(u3.get_cart_count())

# ###CLEAR CART###
# print(u3.clear_cart())

####RECORD SALE######
# print(u3.record_sale('stripe token'))
