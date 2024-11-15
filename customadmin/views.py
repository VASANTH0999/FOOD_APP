# views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import MenuItemForm, RestaurantForm
from customer.models import MenuItem, Cart, Restaurant
from .models import Profile  # Ensure Profile is imported


def add_menu_item(request):
    if request.method == "POST":
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customadmin:view_selected_items')  # Redirect to view selected items
    else:
        form = MenuItemForm()
    return render(request, 'customadmin/add_menu_item.html', {'form': form})


def add_restaurant(request):
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customadmin:restaurant_list')  # Or wherever you'd like to redirect
    else:
        form = RestaurantForm()
    return render(request, 'customadmin/add_restaurant.html', {'form': form})
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'customadmin/restaurant_list.html', {'restaurants': restaurants})


def view_selected_items(request):
    items = MenuItem.objects.all()  # Fetch all MenuItem entries
    return render(request, 'customadmin/view_selected_items.html', {'items': items})


def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:  # Check if user is staff/admin
            login(request, user)
            return redirect('customadmin:admin_dashboard')  # Redirect to the dashboard after login
        else:
            return render(request, 'customadmin/admin_login.html', {'error': 'Invalid credentials or not authorized.'})

    return render(request, 'customadmin/admin_login.html')

def order_review(request):
    # Get the user's cart; handle the case if the cart does not exist
    cart = get_object_or_404(Cart, user=request.user)

    # Ensure the user has a profile
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Collect user info from the profile
    user_info = {
        'name': request.user.get_full_name(),
        'email': request.user.email,
        'street': profile.street,
        'city': profile.city,
        'state': profile.state,
        'zip': profile.zip
    }

    context = {
        'cart': cart,
        'user_info': user_info
    }

    return render(request, 'customadmin/order_review.html', context)
def admin_dashboard(request):
    return render(request, 'customadmin/admin_dashboard.html')
