thermostat_status = True

Temp = int(input("Enter the temp: "))
thermostat_status = int(input("What is the status of the Thermostat(0/1): "))

if thermostat_status==True:
    if Temp>35:
        print("High Temp alert!!")
    else:
        print("Temp normal!")
else:
    print("Device is offline")