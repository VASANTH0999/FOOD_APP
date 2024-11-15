import json
from random import random

from allauth.account.views import login
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib import messages
from django.http import JsonResponse
from .models import MenuItem, Category, OrderModel, Restaurant  # Import Cart model
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required


class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # Get every item from each category
        Biryanis = MenuItem.objects.filter(category__name__contains='Biryanis')
        frys = MenuItem.objects.filter(category__name__contains='frys')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        context = {
            'Biryanis': Biryanis,
            'frys': frys,
            'desserts': desserts,
            'drinks': drinks,

        }

        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')
        price = 0
        item_ids = []

        for item in items:
            menu_item = MenuItem.objects.get(pk=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)
            price += menu_item.price
            item_ids.append(menu_item.pk)

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code
        )
        order.items.add(*item_ids)

        body = ('Thank you for your order! Your food is being made and will be delivered soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')

        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [email],
            fail_silently=False
        )

        context = {
            'items': order_items['items'],
            'price': price
        }

        return redirect('order-confirmation', pk=order.pk)


class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = OrderModel.objects.get(pk=pk)

        context = {
            'pk': order.pk,
            'items': order.items.all(),
            'price': order.price,

        }

        return render(request, 'customer/order_confirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)

        if data['isPaid']:
            order = OrderModel.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('payment-confirmation')


class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/order_pay_confirmation.html')


class Menu(View):
    def get(self, request, *args, **kwargs):
        category_name = request.GET.get("category")
        menu_items = None
        categories = Category.objects.all()

        if category_name:
            # Show items from the selected category
            menu_items = MenuItem.objects.filter(category__name__icontains=category_name)

        context = {
            'menu_items': menu_items,
            'categories': categories,
            'selected_category': category_name,
        }

        return render(request, 'customer/menu.html', context)


class MenuSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get("q")
        category_name = self.request.GET.get("category")

        menu_items = MenuItem.objects.all()

        if query:
            menu_items = menu_items.filter(
                Q(name__icontains=query) |
                Q(price__icontains=query) |
                Q(description__icontains=query)
            )

        if category_name:
            menu_items = menu_items.filter(category__name__icontains=category_name)

        context = {
            'menu_items': menu_items,
            'query': query,
            'category': category_name,

        }

        return render(request, 'customer/menu.html', context)


class GetStarted(View):
    def get(self, request, *args, **kwargs):
        # Render the Get Started page
        return render(request, 'customer/get_started.html')


class weblogin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/weblogin.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'customer/weblogin.html')


class websigin(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/websigin.html')

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if the username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('websigin')

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        messages.success(request, "Account created successfully! You can log in now.")
        return redirect('weblogin')


def feedback_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = FeedbackForm(data)

            if form.is_valid():
                form.save()  # Save the feedback
                return JsonResponse({'message': 'Feedback submitted successfully!'}, status=200)

            return JsonResponse({'errors': form.errors}, status=400)

        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON data'}, status=400)

    else:
        form = FeedbackForm()

    return render(request, 'feedback.html', {'form': form})


def login_selection(request):
    return render(request, 'customer/login_selection.html')


from django.shortcuts import get_object_or_404, redirect
from .models import MenuItem, Cart
from django.contrib.auth.decorators import login_required


@login_required
def add_to_cart(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart.items.add(item)
    cart.update_total_price()

    return redirect('view_cart')  # Redirect to the cart page after adding an item


@login_required
def view_cart(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            order_id = cart.order.pk if hasattr(cart, 'order') else None
            total_price = sum(item.price for item in cart.items.all())  # Calculate the total price
        except Cart.DoesNotExist:
            cart = None
            order_id = None
            total_price = 0  # Default total price if cart doesn't exist
    else:
        cart = None
        order_id = None
        total_price = 0  # Default total price if user is not authenticated

    return render(request, 'customer/view_cart.html', {'cart': cart, 'order_id': order_id, 'total_price': total_price})


ORDER_STATUSES = ['Order Placed', 'Preparing', 'Out for Delivery', 'Delivered']

import random

ORDER_STATUSES = [
    "Order Placed",
    "Food Preparation Started",
    "Packing",
    "On the Way",
    "Out for Delivery",
    "Delivered"
]

def get_order_status(request):
    # Randomly select a status
    current_status = random.choice(ORDER_STATUSES)
    return render(request, 'customer/track_order.html', {'status': current_status})


@login_required
def clear_cart(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart.items.clear()  # Clears all items in the cart
    except Cart.DoesNotExist:
        pass  # Cart does not exist; nothing to clear
    return redirect('view_cart')


def base_view(request):
    cart_item_count = 0
    if request.user.is_authenticated:
        try:
            view_cart = Cart.objects.get(user=request.user)
            cart_item_count = view_cart.items.count()
        except Cart.DoesNotExist:
            pass  # No cart found for the user

    return render(request, 'customer/base.html', {'cart_item_count': cart_item_count})


class RestaurantListView(View):
    def get(self, request, *args, **kwargs):
        category = request.GET.get('category')
        restaurants = Restaurant.objects.filter(category=category) if category else Restaurant.objects.all()

        return render(request, 'customer/restaurant_list.html', {
            'restaurants': restaurants,
            'category': category
        })


class RestaurantDetailView(View):
    def get(self, request, restaurant_id=None, menu_item_id=None, *args, **kwargs):
        restaurant = get_object_or_404(Restaurant, id=restaurant_id)

        if menu_item_id and MenuItem.objects.filter(id=menu_item_id, restaurant=restaurant).exists():
            menu_items = MenuItem.objects.filter(id=menu_item_id, restaurant=restaurant)
        else:
            menu_items = MenuItem.objects.filter(restaurant=restaurant)

        return render(request, 'customer/restaurant_detail.html', {
            'restaurant': restaurant,
            'menu_items': menu_items,
            'restaurants': Restaurant.objects.all(),
        })


@login_required
def new_order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'customer/new_order_confirmation.html', {'order': order})


class OrderSuccessView(View):
    def get(self, request):
        # Your logic here
        return render(request, 'customer/order_success.html')


def order_summary(request):
    # Get cart items and total price from the POST request
    cart_items = request.POST.getlist('cart_items[]')  # Get list of item names
    total_price = request.POST.get('total_price')  # Get total price

    # Pass the data to the template
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'customer/order_summary.html', context)
