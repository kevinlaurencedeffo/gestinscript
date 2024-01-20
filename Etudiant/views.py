from django.shortcuts import render
import pandas as pd
from rest_framework import serializers, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from .models import Etudiant,Filiere,Paiement
from django.contrib.auth import logout,authenticate
from django.contrib.auth.models import User
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import stripe



class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ('id', 'matricule', 'nom','prenom','adresse','email','dateNaiss','sexe','nationalite','idfiliere','tel','mdp')

class FiliereSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filiere
        fields = ('id', 'nom', 'montant_inscript','montant_pension')

class PaiementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paiement
        fields = ('id', 'idetudiant', 'motif_paiement','montant_paiement','date_paiement')

class EtudiantViewSet(viewsets.ModelViewSet):
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer

    def create_user(self, serializer):
        username = serializer.validated_data['matricule']
        email = serializer.validated_data['email']
        password = serializer.validated_data['mdp']
        user = User.objects.create_user(username=username, email=email, password=password)
        return user
    def perform_create(self, serializer):
        user = self.create_user(serializer)
        serializer.validated_data['id'] = user.pk
        serializer.save()            
        return Response({'success'})


class FiliereViewSet(viewsets.ModelViewSet):
    queryset = Filiere.objects.all()
    serializer_class = FiliereSerializer
    
class PaiementViewSet(viewsets.ModelViewSet):
    queryset = Paiement.objects.all()
    serializer_class = PaiementSerializer

@api_view(['GET'])
def InsertWithFile(request,*args, **kwargs):
    Etudiant.objects.all().delete()
    Filiere.objects.all().delete()
    Paiement.objects.all().delete()
    df1 = pd.read_excel('db.xlsx',sheet_name='Etudiant')
    df2 = pd.read_excel('db.xlsx',sheet_name='Filiere')
    df3 = pd.read_excel('db.xlsx',sheet_name='Paiement')
    data_dicts1 = df1.to_dict(orient='records')
    data_dicts2 = df2.to_dict(orient='records')
    data_dicts3 = df3.to_dict(orient='records')
    for item in data_dicts1:
        Etudiant.objects.create(matricule=item['matricule'],nom=item['nom'],prenom=item['prenom'],email=item['email'],
                                tel=item['tel'],adresse=item['adresse'],dateNaiss=item['dateNaiss'],
                                sexe=item['sexe'],nationalite=item['nationalite'],idfiliere=item['idfiliere'])
      
    for item in data_dicts2:
        Filiere.objects.create(nom=item['nom'],montant_inscript=item['montant_inscript'],montant_pension=item['montant_pension'])
    
    for item in data_dicts3:
        Paiement.objects.create(idetudiant=item['idetudiant'],motif_paiement=item['motif_paiement'],montant_paiement=item['montant_paiement'],
                                date_paiement=item['date_paiement'])
    
    return Response({"success to files into db"})

@api_view(['GET'])
def InsertToFile(request,*args, **kwargs):
    queryset1 = Etudiant.objects.all()
    queryset2 = Filiere.objects.all()
    queryset3 = Paiement.objects.all()
    df1 = pd.DataFrame(queryset1.values())
    df2 = pd.DataFrame(queryset2.values())
    df3 = pd.DataFrame(queryset3.values())
    df1.to_excel('db.xlsx',sheet_name='Etudiants',index=False)
    df2.to_excel('db.xlsx',sheet_name='Filieres',index=False)
    df3.to_excel('db.xlsx',sheet_name='Paiements',index=False)
    return Response({"success to db into file"})

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('nom')
        password = request.data.get('mdp')
        print(request.data)
        user = authenticate(username=username, password=password)
        if user is not None:
            result = Etudiant.objects.filter(id=user.pk)
            return Response({'result': user.is_authenticated,'donnees':result.all().values()})
        else:
            return Response({'result': False})
    
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response(status=204)
 
stripe.api_key = 'sk_test_51L5SZ1AUXuv32ejpEDDc3R1JR4Tyi78zunsftetLIRIo332Dl7OoMfFwYa2SkNvdZ6jerxGA4GOJPPRTodyIizhj00TlDKj1Rk'
@csrf_exempt
def create_payment_intent(request):
    if request.method == 'POST':
        try:
            # Obtenez les données du paiement depuis le frontend
            data = json.loads(request.body)
            amount = data['amount']
            # Créez une intention de paiement avec Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='eur',  # Changez selon votre devise
            )
            payment_intent.confirm(payment_intent.id,payment_method="pm_card_visa",return_url="https://www.example.com")
            return JsonResponse({'clientSecret': payment_intent.client_secret})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=400)
