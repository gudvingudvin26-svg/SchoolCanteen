from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Review
from menu.models import Dish


@login_required
def review_list(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)
    reviews = Review.objects.filter(dish=dish).order_by('-created_at')
    user_review = Review.objects.filter(user=request.user, dish=dish).first()

    return render(request, 'reviews/review_list.html', {
        'dish': dish,
        'reviews': reviews,
        'user_review': user_review
    })


@login_required
def review_create(request, dish_id):
    dish = get_object_or_404(Dish, id=dish_id)

    if Review.objects.filter(user=request.user, dish=dish).exists():
        messages.error(request, 'Вы уже оставили отзыв на это блюдо')
        return redirect('review_list', dish_id=dish.id)

    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        Review.objects.create(
            user=request.user,
            dish=dish,
            rating=rating,
            comment=comment
        )

        messages.success(request, 'Отзыв успешно добавлен')
        return redirect('review_list', dish_id=dish.id)

    return render(request, 'reviews/review_create.html', {'dish': dish})