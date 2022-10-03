from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from epic_event import views

router = routers.SimpleRouter()
router.register("clients", views.ClientViewset, basename="clients")
router.register("contracts", views.ContractViewset, basename="clients")
router.register("events", views.EventViewset, basename="events")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("", include(router.urls)),
]
