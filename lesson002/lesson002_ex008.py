import requests
import json
import time
import datetime


class LongTimeJob:

    def __init__(self, page):
        self.__page = page
        self.__token = None
        self.__seconds = None
        self.__status = None
        self.__error = None
        self.__result = None

    # return token
    def token(self):
        return self.__token

    # return seconds
    def seconds(self):
        return self.__seconds

    # return status
    def status(self):
        return self.__status

    # return result
    def result(self):
        return self.__result

    # return error
    def error(self):
        return self.__error

    # print main page
    def print_page(self):
        print(self.__page)

    # GET request
    def get_req(self, **kwargs):
        return requests.get(url=self.__page, **kwargs)

    # get token
    def get_token(self):
        temp_req = requests.get(self.__page)
        try:
            self.__token = temp_req.json()['token']
            self.__seconds = temp_req.json()['seconds']
        except json.JSONDecodeError:
            print(f"Invalid JSON in token")

    # erase token
    def erase_token(self):
        self.__token = None
        self.__seconds = None

    # print status, error, result
    def info(self):
        print(f"Status = {self.__status}; Result = {self.__result}; Error = {self.__error}.")

    # get status, error, result using token
    def get_status(self, token=True):
        if token:
            temp_req = requests.get(self.__page, params={"token": self.__token})
        else:
            temp_req = requests.get(self.__page)
        try:
            temp_json = temp_req.json()
            result = ""
            if "error" in temp_json:
                self.__error = temp_json["error"]
                if self.__error == "No job linked to this token":
                    result = self.__error
                else:
                    result = "Unexpected error"
            elif "status" in temp_json:
                self.__status = temp_json["status"]
                if self.__status == "Job is ready":
                    if "result" in temp_json:
                        self.__result = temp_json["result"]
                    else:
                        result = "Invalid result. Job is ready but result is empty"
                elif temp_json["status"] == "Job is NOT ready":
                    if "result" in temp_json and temp_json["result"] != "":
                        result = "Invalid result. Job is NOT ready but result is NOT empty"
            if result != "":
                print(result)
        except json.JSONDecodeError:
            print(f"Invalid JSON in status")


url1 = 'https://playground.learnqa.ru/ajax/api/longtime_job'
job1 = LongTimeJob(url1)

# 1) Get token and start job
job1.get_token()
start_time = datetime.datetime.now()
end_time = start_time + datetime.timedelta(seconds=job1.seconds())
# job1.get_status(False)
# job1.info()
print(f"1) Job started."
      f"Current token = {job1.token()}, current seconds = {job1.seconds()}")

# 2) Get status before end of job
job1.get_status()
print(f"2) Status before ending.")
current_time = datetime.datetime.now()
job1.info()
if current_time < end_time and job1.status() == "Job is NOT ready":
    print(f"Valid status. Status is '{job1.status()}'.")
else:
    print(f"Invalid status. Status is '{job1.status()}'.")

# 3) Sleep some seconds
sleep_time = 5.0
while sleep_time > job1.seconds():
    sleep_time -= 0.1
print(f"3) Sleep {sleep_time} seconds before ending and get status")
time.sleep(sleep_time)
job1.get_status()
job1.info()

# 4) Get status after ending job
print(f"4) Waiting end of job and get Status after ending job.")
current_time = datetime.datetime.now()
print(f"Waiting end of job...")
while current_time < end_time:
    current_time = datetime.datetime.now()
    time.sleep(0.5)
print(f"Job ended.")
job1.get_status()
if job1.status() == "Job is ready":
    print(f"Valid status. Result is '{job1.result()}'.")
else:
    print(f"Invalid status. Status is '{job1.status()}'.")
job1.info()
