from .models import Dht11
from .serializers import DHT11serialize
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from twilio.rest import Client
import requests
# Définir la fonction pour envoyer des messages Telegram


@api_view(["GET", "POST"])
def Dlist(request):
    if request.method == "GET":
        all_data = Dht11.objects.all()
        data_ser = DHT11serialize(all_data, many=True)  # Les données sont sérialisées en JSON
        return Response(data_ser.data)

    elif request.method == "POST":
        serial = DHT11serialize(data=request.data)

        if serial.is_valid():
            serial.save()
            derniere_temperature = Dht11.objects.last().temp
            print(derniere_temperature)

            if serial.is_valid():
                serial.save()
                derniere_temperature = Dht11.objects.last().temp
                print(derniere_temperature)

                if derniere_temperature > 25:
                    # Alert Email
                    subject = 'Alerte'
                    message = f'La température dépasse le seuil de 25 °C ({derniere_temperature} °C), veuillez intervenir immédiatement pour vérifier et corriger cette situation.'
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = ['francolegends47@gmail.com']
                    send_mail(subject, message, email_from, recipient_list)

                    # Alert WhatsApp


                    account_sid = 'AC8f4f2f2b7ad60607ac537919957b4003'
                    auth_token = 'ce3678d81eb83d4a49506f7ffafe90b7'
                    client = Client(account_sid, auth_token)

                    message = client.messages.create(
                        from_='whatsapp:+14155238886',
                        body=f'La température dépasse le seuil de 25 °C ({derniere_temperature} °C), veuillez intervenir immédiatement pour vérifier et corriger cette situation.',
                        to='whatsapp:+212716048820'
                    )


                    token = '7821527335:AAF7arSrEGTRy53jQocA3uFmrt3LPWakRlc'
                    chat_id = '1438368303'
                    message = f'La température dépasse le seuil de 25 °C ({derniere_temperature} °C), veuillez intervenir immédiatement pour vérifier et corriger cette situation.'

                    # Envoi du message sur Telegram
                    url = f"https://api.telegram.org/bot{token}/sendMessage"
                    params = {
                        'chat_id': chat_id,
                        'text': message
                    }
                    response = requests.get(url, params=params)

                    # Retour de la réponse en fonction du statut
                    if response.status_code == 200:
                        return Response(serial.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serial.errors, status=status.HTTP_400_BAD_REQUEST)