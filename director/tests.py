from django.test import TestCase
import random
import string

# Create your tests here.
key = ''.join(random.choices(string.digits + string.ascii_letters, k=12)).encode()
print(key)
