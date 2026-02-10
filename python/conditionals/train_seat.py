seat = input("Enter the seat type(ac/sleeper/general/luxury): ").lower()

match seat:
    case "sleeper":
        print("sleeper - sleep all night")
    case "ac":
        print("ac - sleep all night with ac")
    case "general":
        print("general - cheapest")
    case "luxury":
        print("luxury - way luxurious")
    case _:
        print("Invalid choice")
