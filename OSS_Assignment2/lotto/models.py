from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class LottoTicket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    numbers = models.JSONField()
    is_automatic = models.BooleanField(default=True)
    draw_round = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def check_winning(self):
        try:
            target_round = int(self.draw_round)
            draw = LottoDraw.objects.get(draw_number=target_round)
        except (LottoDraw.DoesNotExist, ValueError, TypeError):
            return "추첨 대기중"

        try:
            my_nums = set(int(n) for n in self.numbers)
            win_nums = set(int(n) for n in draw.winning_numbers)
        except (ValueError, TypeError):
            my_nums = set(self.numbers)
            win_nums = set(draw.winning_numbers)

        match_count = len(my_nums.intersection(win_nums))
        
        if isinstance(draw.bonus_number, (int, float)) or str(draw.bonus_number).isdigit():
            bonus_match = int(draw.bonus_number) in my_nums
        else:
            bonus_match = draw.bonus_number in my_nums

        if match_count == 6:
            return "1등"
        elif match_count == 5 and bonus_match:
            return "2등"
        elif match_count == 5:
            return "3등"
        elif match_count == 4:
            return "4등"
        elif match_count == 3:
            return "5등"
        else:
            return "낙첨"
class LottoDraw(models.Model):
    draw_number = models.IntegerField(unique=True, help_text="회차")
    winning_numbers = models.JSONField()
    bonus_number = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.draw_number}회차 추첨 결과"