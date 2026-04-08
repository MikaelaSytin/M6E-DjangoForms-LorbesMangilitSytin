from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Dish


# ======================
# LOGIN
# ======================
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(username=username, password=password)
            return redirect('better_menu', pk=user.id)

        except Account.DoesNotExist:
            return render(request, 'tapasapp/login.html', {
                'error': 'Invalid login'
            })

    return render(request, 'tapasapp/login.html')


# ======================
# SIGNUP
# ======================
def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if Account.objects.filter(username=username).exists():
            return render(request, 'tapasapp/signup.html', {
                'error': 'Account already exists'
            })

        Account.objects.create(username=username, password=password)

        return render(request, 'tapasapp/login.html', {
            'success': 'Account created successfully'
        })

    return render(request, 'tapasapp/signup.html')


# ======================
# LOGOUT
# ======================
def logout(request):
    return redirect('login')


# ======================
# MENU LIST
# ======================
def better_menu(request, pk):
    user = get_object_or_404(Account, id=pk)
    dishes = Dish.objects.all()

    return render(request, 'tapasapp/better_list.html', {
        'dishes': dishes,
        'pk': pk,
        'user': user,
    })


# ======================
# ADD DISH
# ======================
def add_menu(request, pk):
    user = get_object_or_404(Account, id=pk)

    if request.method == "POST":
        name = request.POST.get('dname')
        cook = request.POST.get('ctime')
        prep = request.POST.get('ptime')

        Dish.objects.create(name=name, cook_time=cook, prep_time=prep)

        return redirect('better_menu', pk=pk)

    return render(request, 'tapasapp/add_menu.html', {'pk': pk})


# ======================
# VIEW DETAILS
# ======================
def view_detail(request, pk, dish_id):
    user = get_object_or_404(Account, id=pk)
    dish = get_object_or_404(Dish, id=dish_id)

    return render(request, 'tapasapp/view_detail.html', {
        'd': dish,
        'pk': pk,
    })


# ======================
# UPDATE DISH
# ======================
def update_dish(request, pk, dish_id):
    user = get_object_or_404(Account, id=pk)
    dish = get_object_or_404(Dish, id=dish_id)

    if request.method == "POST":
        dish.cook_time = request.POST.get('ctime')  # name is intentionally skipped
        dish.prep_time = request.POST.get('ptime')
        dish.save()
        return redirect('view_detail', pk=pk, dish_id=dish_id)

    return render(request, 'tapasapp/update_dish.html', {
        'd': dish,
        'pk': pk,
    })


# ======================
# DELETE DISH
# ======================
def delete_dish(request, pk, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    dish.delete()
    return redirect('better_menu', pk=pk)


# ======================
# MANAGE ACCOUNT
# ======================
def manage_account(request, pk):
    user = get_object_or_404(Account, id=pk)

    return render(request, 'tapasapp/manage_account.html', {
        'user': user,
        'pk': pk,
    })


# ======================
# CHANGE PASSWORD
# ======================
def change_password(request, pk):
    user = get_object_or_404(Account, id=pk)

    if request.method == "POST":
        current = request.POST.get('current')
        new = request.POST.get('new')
        confirm = request.POST.get('confirm')

        if user.password != current:
            return render(request, 'tapasapp/change_password.html', {
                'error': 'Incorrect current password',
                'pk': pk,
            })

        if new != confirm:
            return render(request, 'tapasapp/change_password.html', {
                'error': 'New passwords do not match',
                'pk': pk,
            })

        user.password = new
        user.save()

        return redirect('manage_account', pk=pk)

    return render(request, 'tapasapp/change_password.html', {'pk': pk})


# ======================
# DELETE ACCOUNT
# ======================
def delete_account(request, pk):
    user = get_object_or_404(Account, id=pk)
    user.delete()
    return redirect('login')
