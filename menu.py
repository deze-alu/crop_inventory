
def show_menu(title, options):

    while True:
        print()
        print("=========", title, "=========")

        for key in options:
            print(key + ". " + options[key])

        choice = input("Choose an option: ")
        choice = choice.strip()

        if choice in options:
            return choice
        else:
            print("Invalid option, please try again.")


def get_text(prompt):
    # Keeps asking until the user types something that is not empty.

    while True:
        text = input(prompt)
        text = text.strip()

        if text != "":
            return text
        else:
            print("This can't be blank, please try again.")


def get_number(prompt):
    # Keeps asking until the user types something that is a real number.

    while True:
        text = input(prompt)
        text = text.strip()

        try:
            number = float(text)
            return number
        except ValueError:
            print("That's not a number, please try again.")

# It lets you test the three functions on their own, without the
# rest of the program.
if __name__ == "__main__":
    options = {"1": "Say hello", "2": "Say goodbye", "0": "Exit"}

    choice = show_menu("DEMO MENU", options)
    print("You chose:", choice)

    name = get_text("Enter your name: ")
    print("Hello,", name)

    quantity = get_number("Enter a quantity: ")
    print("You entered:", quantity)
