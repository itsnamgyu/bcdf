monthes = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "Augest",
        "September",
        "October",
        "November",
        "December" ]

month, day = input("Try try! ").split("/")

print("It's {}, {}th!".format(monthes[int(month) - 1], day))
