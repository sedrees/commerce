from django.contrib import admin

from .models import Auction, Watchlist, Bid, Comment

# Register your models here.

admin.site.register(Auction)
admin.site.register(Watchlist)
admin.site.register(Bid)
admin.site.register(Comment)

class AuctionInline(admin.StackedInline):
    model = Auction
    readonly_fields=('id')

    def auction_id(self, obj):
        return obj.id