import json


def load_data():
    try:
        with open("contacts.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_data(data):
    with open("contacts.json", "w") as json_file:
        json.dump(data, json_file)


def take_operation():
    print(
        """
        1. Add a Contact.
        2. Search for a Contact.
        3. Delete a Contact.
        4. Exit.
        """
    )
    while True:
        try:
            return int(input("What you want to do? (1/2/3/4): "))
        except ValueError:
            print("Enter a valid operation (1/2/3/4).")


def print_contacts_table(results):
    index_width = 5
    name_width = 15
    mail_width = 25
    address_width = 20

    print(
        f"{'Index':<{index_width}} | {'Name':<{name_width}} | {'Email':<{mail_width}} | {'Address':<{address_width}}"
    )
    print("-" * (index_width + name_width + mail_width + address_width + 9))
    for key, info in results:
        print(
            f"{key:<{index_width}} | {info['name']:<{name_width}} | {info['mail']:<{mail_width}} | {info['address']:<{address_width}}"
        )


def add_contact():
    name = input("Enter you name: ")
    mail = input("Enter you mail: ")
    address = input("Enter you address: ")
    return {"name": name, "mail": mail, "address": address}


def search_contact(name):
    data = load_data()
    results = []
    for key, info in enumerate(data):
        if not name or name.lower() in info["name"].strip().lower():
            results.append((key, info))
    if not results:
        print("No Contacts Found")
        return
    print_contacts_table(results)


def delete_contact(number, name):
    data = load_data()
    for key, info in enumerate(data):
        if key == int(number) and name.strip().lower() == info["name"].lower():
            print(f"{key},{info}")
            data.pop(key)
            save_data(data)
            return True
    return False


if __name__ == "__main__":
    print("Welcome to Contact Management System.")

    while True:
        match take_operation():
            case 1:
                contact = add_contact()
                save_data(load_data() + [contact])
                print(f"Contact {contact} saved")

            case 2:
                name = input("Enter the name: ")
                search_contact(name)
            case 3:
                name = input("Enter the name: ")
                try:
                    number = int(input("Enter the number: "))
                    deleted = delete_contact(number, name)
                    if deleted:
                        print(f"Contact: '{name}' deleted")
                    else:
                        print("No contact found with that number and name")
                except ValueError:
                    print(
                        "Failed to delete the contact, please try again with a valid number"
                    )
            case 4:
                break
            case _:
                continue
