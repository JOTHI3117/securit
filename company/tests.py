from django.test import TestCase
import random


# Create your tests here.
def view_gk_question():
    global a
    global gk
    gk = {'Name the Father of the Indian Constitution?': 'Dr. B. R. Ambedkar',
          'Who was the first Prime Minister of India?': 'Jawaharlal Nehru',
          'Who was the first woman Prime Minister of India?': ' Indira Gandhi',
          'Name the deepest ocean in the world?': 'Pacific Ocean',
          'Name the gas which is filled in balloons?': 'Helium',
          'Aizawl is the capital of which state of India?': 'Mizoram',
          'Bucharest is the capital of which country?': 'Romania',
          'The deepest part of the ocean is called?': 'Challenger Deep',
          ' ........... is the capital of Andhra Pradesh.': 'Amaravati',
          'Baby of a horse is known as.........': 'Foal', ' Young one of a cow is known as .......': 'Calf'}
    a = random.choices(list(gk), k=5)
    return a


print(view_gk_question())


def check():
    global a
    global gk
    b = gk.keys()
    return b
print(check())
