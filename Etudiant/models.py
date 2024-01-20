from django.db import models

# Create your models here.



class Etudiant(models.Model):
    id = models.IntegerField()
    matricule = models.CharField(max_length=255,primary_key=True)
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    dateNaiss = models.DateField()
    sexe = models.CharField(max_length=255)
    nationalite = models.CharField(max_length=255)
    idfiliere = models.ForeignKey(to="Filiere", on_delete=models.CASCADE)
    tel = models.IntegerField()
    mdp = models.CharField(max_length=255)
    def __str__(self):
        return self.nom

class Filiere(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=255)
    montant_inscript = models.IntegerField()
    montant_pension = models.IntegerField()
    def __str__(self):
        return self.nom

class Paiement(models.Model):
    id = models.AutoField(primary_key=True)
    idetudiant = models.ForeignKey(to="Etudiant",on_delete=models.CASCADE)
    motif_paiement = models.CharField(max_length=255)
    montant_paiement = models.IntegerField()
    date_paiement = models.DateField(auto_now=True)
    def __str__(self):
        return self.id