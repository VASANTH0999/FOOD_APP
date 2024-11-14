from django.contrib import admin
from .models import MenuItem, Category, OrderModel, Feedback, Cart, Restaurant

admin.site.register(MenuItem)
admin.site.register(Category)
admin.site.register(OrderModel)
admin.site.register(Cart)
admin.site.register(Restaurant)




class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('rating', 'comments', 'created_at')

admin.site.register(Feedback, FeedbackAdmin)


