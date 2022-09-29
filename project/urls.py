from django.contrib import admin
from django.urls import path, include
from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from epic_event import views

router = routers.SimpleRouter()
router.register("clients", views.ClientViewset, basename="clients")

client_router = routers.NestedSimpleRouter(router, "clients", lookup="client")
client_router.register("contracts", views.ContractViewset, basename="contract")

contract_router = routers.NestedSimpleRouter(
    client_router, "contracts", lookup="contract"
)
contract_router.register("event", views.EventViewset, basename="event")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/token/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("", include(router.urls)),
    path("", include(client_router.urls)),
    path("", include(contract_router.urls)),
]
