import random
from django.shortcuts import render, redirect
from .models import LottoTicket, LottoDraw
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

def index(request):
    last_draw = LottoDraw.objects.order_by('-draw_number').first()
    current_round = last_draw.draw_number + 1 if last_draw else 1
    
    if request.method == "POST":
        action_type = request.POST.get('action_type')

        if action_type == 'auto':
            numbers = sorted(random.sample(range(1, 46), 6))
            LottoTicket.objects.create(
                user=request.user, 
                numbers=numbers, 
                is_automatic=True, 
                draw_round=current_round
            )
            
        elif action_type == 'manual':
            try:
                nums = [
                    int(request.POST.get('n1')), int(request.POST.get('n2')),
                    int(request.POST.get('n3')), int(request.POST.get('n4')),
                    int(request.POST.get('n5')), int(request.POST.get('n6'))
                ]
                
                if len(set(nums)) != 6:
                    messages.error(request, "중복된 번호가 있습니다!")
                else:
                    LottoTicket.objects.create(
                        user=request.user, 
                        numbers=sorted(nums), 
                        is_automatic=False, 
                        draw_round=current_round
                    )
            except ValueError:
                messages.error(request, "올바른 숫자를 6개 입력해주세요.")

        return redirect('index')

    tickets = LottoTicket.objects.filter(user=request.user).order_by('-created_at') if request.user.is_authenticated else []
    
    for ticket in tickets:
        ticket.result_text = ticket.check_winning() 

    return render(request, 'lotto/index.html', {
        'tickets': tickets,
        'current_round': current_round
    })

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'lotto/signup.html', {'form': form})

@staff_member_required
def admin_draw(request):
    draw_nums = random.sample(range(1, 46), 7)
    winning_numbers = sorted(draw_nums[:6])
    bonus_number = draw_nums[6]

    last_draw = LottoDraw.objects.last()
    new_round = last_draw.draw_number + 1 if last_draw else 1

    LottoDraw.objects.create(
        draw_number=new_round,
        winning_numbers=winning_numbers,
        bonus_number=bonus_number
    )
    return redirect('/admin/lotto/lottodraw/')