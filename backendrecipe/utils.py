from recipes.models import RecipeRating, Recipe
from backendrecipe.settings import API_HUNTER_KEY, API_CLEARBIT_KEY
import requests
import clearbit
from rest_framework import serializers, status

def hunter_verify(email):
    api_key = API_HUNTER_KEY
    response = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}")
    if response.status_code != status.HTTP_200_OK:
        raise serializers.ValidationError(f"Check mail error {response.status_code}")
    response_status = response.json()['data']['status']
    if response_status == 'invalid' or response_status == "disposable":
        return False
    return True

def clearbit_info(email):
    clearbit.key = API_CLEARBIT_KEY
    response = clearbit.Enrichment.find(email=email, stream=True)
    if response is not None:
        return response
    else:
        return "There is no additional information"