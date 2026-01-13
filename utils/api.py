import requests
import json

class CF_API:
    def __init__(self):
        self.url = "https://codeforces.com/api/problemset.problems"

    def fetch(self):
        try:
            response = requests.get(self.url)
            if response.status_code == 200:
                data = response.json()
                problem_list = data["result"]["problems"]
                json_string = json.dumps(problem_list, indent=4)
                return(json_string)
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")



class CF_USER_API:
    def __init__(self):
        self.baseURL = "https://codeforces.com/api/user.status?handle="
        self.userID = None
        self.CF_Handle = None
        self.contestID = 809
        self.index = "A"

    def __init__(self, userID, CFHandle):
        self.baseURL = "https://codeforces.com/api/user.status?handle="
        self.userID = userID
        self.CF_Handle = CFHandle
        self.contestID = 809
        self.index = "A"

    def check_ID_and_Handle(self):
        return (self.userID, self.CF_Handle)

    def verify(self):
        url = self.baseURL + self.CF_Handle + "&from=1&count=1"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()

                status = (data["result"][0]["problem"]["contestId"], data["result"][0]["problem"]["index"], data["result"][0]["verdict"])
                #print(status)
                if status != (809, "A", "COMPILATION_ERROR"):
                    return False
                else: 
                    return True

            else:
                print(f"Error: {response.status_code} - {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return False
    
