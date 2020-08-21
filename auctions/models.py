from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.DecimalField(max_digits=6, decimal_places=2)
    def __str__(self):
        return f"{self.bid} by {self.bidder}"

class Auction(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings")
    title = models.CharField(max_length=420)
    description = models.CharField(max_length=2000)
    img = models.CharField(max_length=3000)
    listed = models.DateTimeField(auto_now_add=True)
    bid_starting = models.DecimalField(max_digits=6, decimal_places=2)
    bid_current = models.ForeignKey(Bid, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=100)
    winner = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True)
    active = models.BooleanField()
    def __str__(self):
        return f"{self.title}({self.pk}) listed by {self.seller} on {self.listed}"

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    content = models.CharField(max_length=2000)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return f"{self.author} comment on {self.auction}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    class Meta:
        unique_together=["auction", "user"]
    def __str__(self):
        return f"{self.user} watching {self.auction}"