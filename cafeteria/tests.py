from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from cafeteria.models import FoodItem, Cart, CartItem

class CafeteriaViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')
        self.orderonline_url = reverse('orderonline')
        self.user = User.objects.create_user(username='testuser', password='testpass')
        
       
        self.food_item = FoodItem.objects.create(
            name='Burger', 
            description='Delicious burger',
            price=100,
            category='Fast Food'
        )

    def test_order_online_page_loads(self):
        response = self.client.get(self.orderonline_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafeteria/orderonline.html')

    def test_signup_success(self):
        response = self.client.post(self.signup_url, {
            'username': 'newuser',
            'email': 'newuser@gmail.com',
            'phone': '9800000000',
            'password': 'password123',
            'confirm_password': 'password123',
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_success(self):
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'testpass'
        })
        self.assertEqual(response.status_code, 302) 

    def test_view_cart_empty(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.get(reverse('view_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cafeteria/cart.html')

    def test_add_to_cart(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('add_to_cart', args=[self.food_item.id]), {
            'quantity': '2',
        })
        self.assertEqual(response.status_code, 302)
        cart = Cart.objects.get(user=self.user)
        cart_item = CartItem.objects.get(cart=cart, food_item=self.food_item)
        self.assertEqual(cart_item.quantity, 2)

    # def test_update_cart_item(self):
    #     self.client.login(username='testuser', password='testpass')
    #     cart = Cart.objects.create(user=self.user)
    #     cart_item = CartItem.objects.create(cart=cart, food_item=self.food_item, quantity=1)

    #     response = self.client.post(reverse('update_cart', args=[cart_item.id]), {
    #         'quantity': '5'
    #     })
    #     self.assertEqual(response.status_code, 302)
    #     cart_item.refresh_from_db()
    #     self.assertEqual(cart_item.quantity, 5)

    # def test_remove_from_cart(self):
    #     self.client.login(username='testuser', password='testpass')
    #     cart = Cart.objects.create(user=self.user)
    #     cart_item = CartItem.objects.create(cart=cart, food_item=self.food_item, quantity=1)

    #     response = self.client.get(reverse('remove_from_cart', args=[cart_item.id]))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertFalse(CartItem.objects.filter(id=cart_item.id).exists())

    # def test_clear_cart(self):
    #     self.client.login(username='testuser', password='testpass')
    #     cart = Cart.objects.create(user=self.user)
    #     CartItem.objects.create(cart=cart, food_item=self.food_item, quantity=2)

    #     response = self.client.get(reverse('clear_cart'))
    #     self.assertEqual(response.status_code, 302)
    #     self.assertEqual(cart.cart_items.count(), 0)

    # def test_cart_summary_empty(self):
    #     self.client.login(username='testuser', password='testpass')
    #     response = self.client.get(reverse('cartsummary'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Your cart is empty.")

