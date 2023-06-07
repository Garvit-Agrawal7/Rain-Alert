import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient


APPID = os.environ["APPID"]
lat = os.environ["LAT"]
long = os.environ["LONG"]
account_sid = os.environ["ACC_SID"]
auth_token = os.environ["AUTH_TOKEN"]
NUMBER = os.environ["NUMBER"]
twilio_client_phone_no = os.environ["TWILIO_CLIENT"]


response = requests.get(f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}"
                        f"&lon={long}&exclude=current,minutely,daily&appid={APPID}")
weather_data = response.json()
weather_forecast = weather_data["hourly"][:12]

will_rain = False

for hourly_forecast in weather_forecast:
    weather = hourly_forecast["weather"][0]["id"]
    if weather < 700:
        will_rain = True
        break
    else:
        will_rain = False

proxy_client = TwilioHttpClient()
proxy_client.session.proxies = {"https": os.environ['https_proxy']}
client = Client(account_sid, auth_token, http_client=proxy_client)

if will_rain:
    message = client.messages.create(
        body='Hey\nTake an umbrella with you, it might rain today☔️!',
        from_=twilio_client_phone_no,
        to=NUMBER
    )
    print(message.status)
else:
    message = client.messages.create(
        body='Hey\nYour day will be bright and shinny☀️😎!',
        from_=twilio_client_phone_no,
        to=NUMBER
    )
    print(message.status)
