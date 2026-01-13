from api import CF_USER_API
import requests
import json

user_dict = {}

with open('user_dtb.json', 'r') as file:
    user_dict = json.load(file)

Verifier = CF_USER_API(686600687899246625, "Sunnyyyy")



if Verifier.verify() == True:
    print("Account linked!")
    user_dict[686600687899246625] = "Sunnyyyy"
    json_string = json.dumps(user_dict, indent=4)
    with open('user_dtb.json', 'w') as file:
        file.write(json_string)
else:
    print("Try again")