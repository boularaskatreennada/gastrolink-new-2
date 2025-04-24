from django.shortcuts import render, redirect, get_object_or_404
from .models import Dish, DishIngredient, Ingredient, MainMenu
from .forms import DishForm, IngredientForm, MainMenuForm
from django.forms import modelformset_factory
from restaurant.decorators import pdg_required, manager_required

DishIngredientFormSet = modelformset_factory(DishIngredient, fields=('ingredient', 'quantity'), extra=2, can_delete=True)

@pdg_required
def menu_view(request):
    categories = MainMenu.objects.all()
    selected_category_id = request.GET.get('category')
    dishes = Dish.objects.filter(menu_id=selected_category_id) if selected_category_id else Dish.objects.all()
    return render(request, 'pdg/menu.html', {'categories': categories, 'selected_category_id': selected_category_id, 'dishes': dishes})

@pdg_required
def add_plate(request):
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES)
        formset = DishIngredientFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            dish = form.save()
            for f in formset:
                if f.cleaned_data and not f.cleaned_data.get('DELETE'):
                    di = f.save(commit=False)
                    di.dish = dish
                    di.save()
            return redirect('menu')
    else:
        form = DishForm()
        formset = DishIngredientFormSet(queryset=DishIngredient.objects.none())
    return render(request, 'pdg/addPlate.html', {'form': form, 'formset': formset})

@pdg_required
def edit_plate(request, pk):
    dish = get_object_or_404(Dish, pk=pk)
    formset = DishIngredientFormSet(queryset=DishIngredient.objects.filter(dish=dish))
    if request.method == 'POST':
        form = DishForm(request.POST, request.FILES, instance=dish)
        formset = DishIngredientFormSet(request.POST, queryset=DishIngredient.objects.filter(dish=dish))
        if form.is_valid() and formset.is_valid():
            form.save()
            for f in formset:
                if f.cleaned_data:
                    di = f.save(commit=False)
                    di.dish = dish
                    if not f.cleaned_data.get('DELETE'):
                        di.save()
                    elif f.cleaned_data.get('DELETE'):
                        f.instance.delete()
            return redirect('menu')
    else:
        form = DishForm(instance=dish)
    return render(request, 'pdg/addPlate.html', {'form': form, 'formset': formset})

@pdg_required
def delete_plate(request, pk):
    get_object_or_404(Dish, pk=pk).delete()
    return redirect('menu')

@pdg_required
def ingredients_view(request):
    return render(request, 'pdg/ingredients.html', {'ingredients': Ingredient.objects.all()})

@pdg_required
def add_ingredient(request):
    form = IngredientForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('ingredients')
    return render(request, 'pdg/addIngred.html', {'form': form})

@pdg_required
def edit_ingredient(request, pk):
    instance = get_object_or_404(Ingredient, pk=pk)
    form = IngredientForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('ingredients')
    return render(request, 'pdg/addIngred.html', {'form': form})

@pdg_required
def delete_ingredient(request, pk):
    get_object_or_404(Ingredient, pk=pk).delete()
    return redirect('ingredients')

@pdg_required
def add_category(request):
    form = MainMenuForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('categories')
    return render(request, 'pdg/addCategory.html', {'form': form})

@pdg_required
def edit_category(request, pk):
    instance = get_object_or_404(MainMenu, pk=pk)
    form = MainMenuForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return redirect('categories')
    return render(request, 'pdg/addCategory.html', {'form': form})

@pdg_required
def delete_category(request, pk):
    get_object_or_404(MainMenu, pk=pk).delete()
    return redirect('menu')