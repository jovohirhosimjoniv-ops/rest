from django.contrib.auth.models import User
from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="thumbnails/")
    channel = models.CharField(max_length=100, default="Unknown")
    views = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Profile(models.Model):
    ROLE_CHOICES = (
        ("mijoz", "Mijoz"),
        ("usta", "Usta"),
        ("admin", "Admin"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefon = models.CharField(max_length=20, blank=True)
    rasm = models.ImageField(upload_to="profiles/", blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLE_CHOICES, default="mijoz")
    viloyat = models.CharField(max_length=100, blank=True)
    shahar = models.CharField(max_length=100, blank=True)

    # Usta uchun qo'shimcha maydonlar
    haqida = models.TextField(blank=True)
    tajriba = models.IntegerField(default=0)
    kategoriya = models.CharField(max_length=100, blank=True)
    konikma = models.TextField(blank=True)
    vaqt = models.CharField(max_length=50, blank=True)
    narx = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


class Portfolio(models.Model):
    profile = models.ForeignKey(
        Profile, related_name="portfolio", on_delete=models.CASCADE
    )
    rasm = models.ImageField(upload_to="portfolio/")

    def __str__(self):
        return f"{self.profile.user.username} - Portfolio ({self.id})"


class Buyurtma(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="buyurtmalar"
    )
    usta = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="usta_buyurtmalari"
    )
    xizmat_turi = models.CharField(max_length=255)
    sana = models.CharField(max_length=50, blank=True, null=True)  # <-- CharField ga o'zgartirildi
    vaqt = models.CharField(max_length=50, blank=True, null=True)  # <-- CharField ga o'zgartirildi
    manzil = models.CharField(max_length=255, blank=True, null=True)
    izoh = models.TextField(blank=True, null=True)
    
    # YANGI QO'SHILGAN MAYDON:
    status = models.CharField(max_length=50, default="pending") 
    
    yaratilgan_vaqt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Buyurtma #{self.id} — {self.user.username} ({self.xizmat_turi})"