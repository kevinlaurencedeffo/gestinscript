from . import views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("Etudiant", views.EtudiantViewSet)
router.register("Filiere", views.FiliereViewSet)
router.register("Paiement", views.PaiementViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("InsetIntoFile", views.InsertToFile,name="InsetIntoFile"),
    path("InsertWithFile", views.InsertWithFile,name="InsertWithFile"),
    path('login/', views.LoginView.as_view()),
    path('logout', views.LogoutView.as_view()),
]