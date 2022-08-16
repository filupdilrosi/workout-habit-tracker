import os
import requests
from datetime import datetime

passw = os.environ["password"]
username = os.environ["username"]
APP_ID = os.environ["APP_ID"]
API_KEY = os.environ["API_KEY"]
SHEETY_TOKEN = os.environ["TOK"]
EXERCISE_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
SHEETY_ENDPOINT = "https://api.sheety.co/13ffaf62d9ead423c70b142f8effafe6/mySpread/sheet1"
date = str(datetime.today().date().strftime("%d/%m/%Y"))
time = str(datetime.today().time().strftime("%X"))


def add_row(sheety_update_doc_post_request):
    sheety_post_response = requests.post(url=SHEETY_ENDPOINT, json=sheety_update_doc_post_request,
                                         headers=header_sheety)
    print(sheety_post_response.text)


exercise_header = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "x-remote-user-id": "0",
}
header_sheety = {
    "Content-Type": "application/json",
    "Authorization": SHEETY_TOKEN,
}

query = input("Tell me which exercises you did: ")
weight = int(input("Tell me your weight in kilograms: "))
gender = input("What is your gender? ")
height = int(input("Tell me your height in centimeters: "))
age = int(input("What is your age? "))

exercise_post_request = {
    "query": query,
    "gender": gender,
    "weight_kg": weight,
    "height_cm": height,
    "age": age,
}
exercise_post_info = requests.post(url=EXERCISE_ENDPOINT, json=exercise_post_request, headers=exercise_header)
print(exercise_post_info.text)
workout_info = exercise_post_info.json()
exercise_bank = []
for workouts in workout_info["exercises"]:
    exercise_bank.append(workouts)
print(exercise_bank)
for i in range(len(exercise_bank)):
    sheety_update_doc_post_request = {
        "sheet1": {
            "date": date,
            "time": time,
            "exercise": exercise_bank[i]["user_input"],
            "duration": exercise_bank[i]["duration_min"],
            "calories": exercise_bank[i]["nf_calories"],
        }
    }
    add_row(sheety_update_doc_post_request)

sheety_get_response = requests.get(url=SHEETY_ENDPOINT, headers=header_sheety)
print(sheety_get_response.text)
