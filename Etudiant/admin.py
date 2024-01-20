from django.contrib import admin
from .models import Etudiant,Filiere,Paiement
# Register your models here.
admin.site.register(Etudiant)
admin.site.register(Paiement)
admin.site.register(Filiere)