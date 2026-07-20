from django.urls import path
from . import views

urlpatterns = [
    path("best9ja-music-studio/", views.home, name="music_index"),
  
     # 💳 Checkout (guest email → Paystack init)
    path("checkout/<slug:slug>/", views.checkout, name="checkout"),

    # 🔁 Paystack verification callback
    path("payment/verify/", views.verify_payment, name="verify_payment"),

    # # 🎉 Success page after payment
    path("success/<str:reference>/", views.success, name="success"),
    path(
    "category/<int:pk>/",
    views.category_beats,
    name="category_beats"
),
]