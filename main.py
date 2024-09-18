import time

from dbConnect import setDB

employees = [
    ["Bar Shuv", "barsh2001@gmail.com"],
    ["Amnon Abaev", "amnonn122@gmail.com"]
]

setDB(employees)

try:
    while True:
        print("MongoDB server is running. Press Ctrl+C to stop.")
        time.sleep(60)  # Sleep for 60 seconds before the next print













except KeyboardInterrupt:
    print("Shutting down the server...")