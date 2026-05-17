from django.contrib import admin
from .models import LottoDraw, LottoTicket

@admin.register(LottoDraw)
class LottoDrawAdmin(admin.ModelAdmin):
    list_display = ('draw_number', 'winning_numbers', 'bonus_number',
                    'total_sales', 'winner_stats', 'created_at')
    change_list_template = "admin/lotto_draw_change_list.html"

    def total_sales(self, obj):
        count = LottoTicket.objects.filter(draw_round=obj.draw_number).count()
        return f"{count} 장"
    total_sales.short_description = '총 판매량'

    def winner_stats(self, obj):
        tickets = LottoTicket.objects.filter(draw_round=obj.draw_number)
        first = second = third = fourth = fifth = lose = 0
        
        for ticket in tickets:
            result = ticket.check_winning()
            if result == "1등": first += 1
            elif result == "2등": second += 1
            elif result == "3등": third += 1
            elif result == "4등": fourth += 1
            elif result == "5등": fifth += 1
            elif result == "낙첨": lose += 1
            
        return f"1등: {first}명 / 2등: {second}명 / 3등: {third}명 / 4등: {fourth}명 / 5등: {fifth}명 / 낙첨: {lose}명"
    winner_stats.short_description = '추첨 내역'

@admin.register(LottoTicket)
class LottoTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'draw_round', 'numbers', 'is_automatic', 'created_at')
    list_filter = ('draw_round', 'is_automatic')