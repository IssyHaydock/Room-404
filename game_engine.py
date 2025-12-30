#Room 404
import json
import time


class Game:
    def __init__(self, data):
        self.start_room = data["start room"]
        with open("inventory.txt", "w") as f:
            f.write("==== Inventory ====\n")

    def start_room(self, data):  # prints out start room desc
        start_room = data["start room"]
        description = start_room["description"]
        print(description)
        time.sleep(1)

    def door_choice(self, data):  # takes user input to determine which room to go to
        start_room = data["start room"]
        choice = start_room["choice"]
        door_choice = input("> ").strip()
        if door_choice in choice:
            return choice[door_choice]  # returns name of chosen room
        else:
            print("Invalid input.")
            time.sleep(2)
            return 0

    def get_rooms_list(self, data):  # gets list of all rooms - used to proceed from chosen room --> research lab --> analytic lab
        return (list(data["rooms"].keys()))

    def win(self, data):  # gets win message
        print(data["success"])

   