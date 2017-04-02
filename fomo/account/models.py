from django.db import models
from django.contrib.auth.models import AbstractUser
from catalog import models as cmod
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
# Create your models here.
class FomoUser(AbstractUser):

#username
#password
#firstname
#lastname
#email
#birthdate


    birthdate = models.DateField(null=True)
    gender = models.CharField(max_length=1, null=True)
    shipping_address = models.CharField(max_length=100, null=True)
    zip_code = models.CharField(null=True, max_length=10)
    country = models.CharField(null=True, max_length=50)
    billing_address = models.CharField(max_length=100, null=True)
    credit_card = models.CharField(max_length=20, null=True)
    cc_exp_date = models.DateField(null=True)
    cc_code = models.CharField(max_length=4, null=True)


    def get_cart(self):
        cart = ShoppingItem.objects.filter(fomouser__id=self.id)
        return cart

    def get_cart_count(self):
        cart = self.get_cart()
        count = 0
        for c in cart:
            print('item')
            count = count + 1
        return count

    def clear_cart(self):
        print('This are the items', self.get_cart())
        self.get_cart().delete()
        print('this is the cart after cleared', self.get_cart())
        return self.get_cart()

    # def remove_cart_item(self, id):

    def product_history(self):
        history = ProductHistory.objects.all()
        return history


    def get_age(self):
        age = datetime.datetime.now() - self.birthdate
        return age.days

    def last5(self):

        last5 = ProductHistory.objects.filter(fomouser__id=self.id).order_by('-view_datetime')
        # products = cmod.Product.objects.filter(id__in=last5)
        last_viewed = []

        for vh in last5:
            if vh.product not in last_viewed:
                last_viewed.append(vh.product)
            if len(last_viewed) >= 6:
                break

        return last_viewed

    def calc_subtotal(self):
        cart = self.get_cart()
        subtotal = Decimal(0)
        for c in cart:
            print('product price', c.product.price)
            print('product qty', c.qty_ordered)
            subtotal += (c.product.price * c.qty_ordered)
            print('subtotal', subtotal)
        print('subtotal amount', subtotal)
        return subtotal

    def calc_tax(self):
        tax_rate = Decimal(.075)
        subtotal = self.calc_subtotal()

        tax_amount = (subtotal * tax_rate)
        print('TAX AMOUNT', tax_amount)
        return tax_amount

    def calc_shipping(self):
        cart = self.get_cart()
        count = 0
        for c in cart:
            count = 1
        if count == 1:
            shipping_rate = Decimal(10)
        else:
            shipping_rate = 0
        print('SHIPPING RATE', shipping_rate)
        return shipping_rate

    def calc_total(self):
        subtotal = self.calc_subtotal()
        tax_amount = self.calc_tax()
        shipping_rate = self.calc_shipping()
        total = (subtotal + tax_amount + shipping_rate)
        print('TOTAL FOR ORDER', total)
        return total

    def record_sale(self, stripe_token):
        sale = Sale()
        sale.fomouser = self
        sale.save()
        cart = self.get_cart()
        for c in cart:
            sale_item = SaleItem()
            sale_item.sale = sale
            sale_item.product = c.product
            sale_item.qty = c.qty_ordered
            sale_item.price = (c.product.price * sale_item.qty)
            sale.total_cost += sale_item.price
            sale_item.save()
            print(sale_item.product.name)
            print(sale_item.qty)
            print(sale_item.price)
            print(sale.total_cost)
            print('>>>>>>>>>>>sale item product', sale_item.product)

            shipping_sale_item = SaleItem()
            shipping_sale_item.sale = sale
            shipping_sale_item.price = self.calc_shipping()
            shipping_sale_item.product = sale_item.product
            print('>>>>>>>>>>>>shi', shipping_sale_item.product)
            shipping_sale_item.save()

            tax_sale_item = SaleItem()
            tax_sale_item.sale = sale
            tax_sale_item.price = self.calc_tax()
            tax_sale_item.product = sale_item.product
            print('>>>>>>>>>>tsi', tax_sale_item.product)
            tax_sale_item.save()


            update_product = cmod.Product.objects.get(id=c.product_id)
            print('>>>>>>>>>>>', update_product)

            if hasattr(update_product, 'quantity'):
                print('>>>>>>>>has quant')
                update_product.quantity -= sale_item.qty
            else:
                update_product.status = False
            update_product.save()

        # shipping_sale_item = SaleItem()
        # shipping_sale_item.sale = sale
        # shipping_sale_item.price = self.calc_shipping()
        # shipping_sale_item.product = sale_item.product #was sale_item.product
        # print('>>>>>>>>>>>>shi', shipping_sale_item.product)
        # shipping_sale_item.save()

        # tax_sale_item = SaleItem()
        # tax_sale_item.sale = sale
        # tax_sale_item.price = self.calc_tax()
        # tax_sale_item.product = sale_item.product #was sale_item.product
        # print('>>>>>>>>>>tsi', tax_sale_item.product)
        # tax_sale_item.save()

        payment = Payment()
        payment.sale = sale
        payment.stripe_charge_token = stripe_token
        payment.total_amount_paid = self.calc_total()
        payment.save()
        sale.save()




        self.clear_cart()
        return sale


##################################################################

class ShoppingItem(models.Model):
    product = models.ForeignKey(cmod.Product)
    fomouser = models.ForeignKey('FomoUser')
    qty_ordered = models.IntegerField(null=True, default=1)

class ProductHistory(models.Model):
    product = models.ForeignKey(cmod.Product)
    fomouser = models.ForeignKey('FomoUser')
    qty_ordered = models.IntegerField(null=True, default=1)
    view_datetime = models.DateTimeField(auto_now_add=True)
    viewed = models.BooleanField(default=True)
    added = models.BooleanField(default=False)
    purchased = models.BooleanField(default=False)
    in_cart = models.BooleanField(default=False)

####################################################################

class Sale(models.Model):
    fomouser = models.ForeignKey('FomoUser')
    date_sold = models.DateTimeField(auto_now_add=True)
    total_cost = models.DecimalField(default=0, max_digits=8, decimal_places=2)

class SaleItem(models.Model):
    sale = models.ForeignKey('Sale')
    product = models.ForeignKey(cmod.Product)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    qty = models.IntegerField(default=1)


class Payment(models.Model):
    sale = models.ForeignKey('Sale')
    stripe_charge_token = models.TextField(null=True, max_length=200)
    date_paid = models.DateTimeField(auto_now_add=True)
    total_amount_paid = models.DecimalField(default=0, max_digits=8, decimal_places=2)


##################################################################
def record_sale(self):
    print("this is record sale")