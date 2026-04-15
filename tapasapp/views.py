
#Mikaela Lauren Sytin 244321
#Sebastian O. Mangilit 242880
#Hans Gabrielle V. Lorbes 242699

#We hereby attest to the truth of the following facts:
#We have not discussed the HTML code in my program with anyone
#other than my instructor or the teaching assistants assigned to this course.
#We have not used HTML code obtained from another student, or
#any other unauthorized source, whether modified or unmodified.
#If any HTML code or documentation used in my program was
#obtained from another source, it has been clearly noted with citations in the
#comments of my program.


from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Dish


logged_in_id = 0 #tracks the logged in user


# LOGIN
def login(request):
    global logged_in_id

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Account.objects.get(username=username, password=password)
            logged_in_id = user.id
            return redirect('better_menu', pk=user.id)

        except Account.DoesNotExist:
            return render(request, 'tapasapp/login.html', {
                'error': 'Invalid login'
            })

    return render(request, 'tapasapp/login.html')


# SIGNUP
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


# LOGOUT
def logout(request):
    global logged_in_id
    logged_in_id = 0
    return redirect('login')


# MENU LIST
def better_menu(request, pk):
    global logged_in_id

    if logged_in_id == 0 or logged_in_id != pk:
        return redirect('login')

    user = get_object_or_404(Account, id=pk)
    dishes = Dish.objects.all()

    return render(request, 'tapasapp/better_list.html', {
        'dishes': dishes,
        'pk': pk,
        'user': user,
    })


# ADD DISH
def add_menu(request, pk):
    global logged_in_id

    if logged_in_id == 0 or logged_in_id != pk:
        return redirect('login')

    user = get_object_or_404(Account, id=pk)

    if request.method == "POST":
        name = request.POST.get('dname')
        cook = int(request.POST.get('ctime'))
        prep = int(request.POST.get('ptime'))

        if cook <= 0 and prep <= 0:
            return render(request, 'tapasapp/add_menu.html', {
                'pk': pk,
                'error': 'Cook time and prep time must be greater than 0',
                'dname': name, 'ctime': cook, 'ptime': prep
            })

        if cook <= 0:
            return render(request, 'tapasapp/add_menu.html', {
                'pk': pk,
                'error': 'Cook time cannot be 0 or anegative value',
                'dname': name, 'ctime': cook, 'ptime': prep
            })

        if prep <= 0:
            return render(request, 'tapasapp/add_menu.html', {
                'pk': pk,
                'error': 'Prep time cannot be 0 or a negative value',
                'dname': name, 'ctime': cook, 'ptime': prep
            })

        Dish.objects.create(name=name, cook_time=cook, prep_time=prep)
        return redirect('better_menu', pk=pk)

    return render(request, 'tapasapp/add_menu.html', {'pk': pk})


# VIEW DETAILS
def view_detail(request, pk, dish_id):
    global logged_in_id

    if logged_in_id == 0 or logged_in_id != pk:
        return redirect('login')

    user = get_object_or_404(Account, id=pk)
    dish = get_object_or_404(Dish, id=dish_id)

    return render(request, 'tapasapp/view_detail.html', {
        'd': dish,
        'pk': pk,
    })


# UPDATE DISH
def update_dish(request, pk, dish_id):
    global logged_in_id

    if logged_in_id == 0 or logged_in_id != pk:
        return redirect('login')

    user = get_object_or_404(Account, id=pk)
    dish = get_object_or_404(Dish, id=dish_id)

    if request.method == "POST":
        cook = int(request.POST.get('ctime'))
        prep = int(request.POST.get('ptime'))

        if cook <= 0 and prep <= 0:
            return render(request, 'tapasapp/update_dish.html', {
                'd': dish, 'pk': pk,
                'error': 'Cook time and prep time cannot be 0 or negative values'
            })

        if cook <= 0:
            return render(request, 'tapasapp/update_dish.html', {
                'd': dish, 'pk': pk,
                'error': 'Cook time cannot be 0 or a negative value'
            })

        if prep <= 0:
            return render(request, 'tapasapp/update_dish.html', {
                'd': dish, 'pk': pk,
                'error': 'Prep time cannot be 0 or a negative value'
            })

        dish.cook_time = cook
        dish.prep_time = prep
        dish.save()
        return redirect('view_detail', pk=pk, dish_id=dish_id)

    return render(request, 'tapasapp/update_dish.html', {
        'd': dish,
        'pk': pk,
    })


# DELETE DISH
def delete_dish(request, pk, dish_id):
    global logged_in_id

    if logged_in_id == 0 or logged_in_id != pk:
        return redirect('login')

    dish = get_object_or_404(Dish, id=dish_id)
    dish.delete()
    return redirect('better_menu', pk=pk)



# MANAGE ACCOUNT
def manage_account(request, pk):
    global logged_in_id

    if logged_in_id == 0 or logged_in_id != pk:
        return redirect('login')

    user = get_object_or_404(Account, id=pk)

    return render(request, 'tapasapp/manage_account.html', {
        'user': user,
        'pk': pk,
    })



# CHANGE PASSWORD
def change_password(request, pk):
    global logged_in_id

    if logged_in_id == 0 or logged_in_id != pk:
        return redirect('login')

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

        if current == new:
            return render(request, 'tapasapp/change_password.html', {
                'error': 'New password must be different from current password',
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



# DELETE ACCOUNT
def delete_account(request, pk):
    global logged_in_id

    if logged_in_id == 0 or logged_in_id != pk:
        return redirect('login')

    user = get_object_or_404(Account, id=pk)
    user.delete()
    logged_in_id = 0
    return redirect('login')