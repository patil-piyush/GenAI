userinput = input("Enter the size of the cup you want to order(small/medium/large): ").lower()

if userinput=="small":
    print("the price is 10 rupees")
elif userinput=="medium":
    print("the price is 20 rupees")
elif userinput=="large":
    print("the price is 30 rupees")
else:
    print("sorry! we dont have such size. ")
