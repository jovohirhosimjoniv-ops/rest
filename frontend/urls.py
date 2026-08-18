from django.urls import path
from .views import (
    ItemList,
    RegisterView,
    LoginView,
    UstaListView,
    UstaDetailView,
    MijozBuyurtmaView,
    MijozBuyurtmaDetailView,
    UstaBuyurtmaListView,
    UstaBuyurtmaDetailView, 
    statistika_view,
)

urlpatterns = [
    path("items/", ItemList.as_view(), name="item-list"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("ustalar/", UstaListView.as_view(), name="usta-list"),
    path("ustalar/<int:pk>/", UstaDetailView.as_view(), name="usta-detail"),
    
    # Yangi ajratilgan buyurtma yo'llari:
    path("mijoz/buyurtmalar/", MijozBuyurtmaView.as_view(), name="mijoz-buyurtmalar"),
    path("mijoz/buyurtmalar/<int:pk>/", MijozBuyurtmaDetailView.as_view(), name="mijoz-buyurtma-detail"),
    path("usta/buyurtmalar/", UstaBuyurtmaListView.as_view(), name="usta-buyurtmalar"),
    path("usta/buyurtmalar/<int:pk>/", UstaBuyurtmaDetailView.as_view(), name="usta-buyurtma-detail"),
    path('statistika/', statistika_view, name='statistika'),
]