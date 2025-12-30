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


    class Room:

        def __init__(self, room_name, data):
            self.room_name = room_name
            self.data = data
            self.solved_puzzles = set()  # track solved puzzles (used only in Analytic Lab)

        def get_description(self, data):  # prints room desc
            room = data["rooms"]
            room_data = room[self.room_name]
            description = room_data["description"]
            print("\n=== " + self.room_name + " ===")
            time.sleep(1)
            print(description)
            time.sleep(3)

        def analytic_all_solved(self, room_data):
            required = set()

            for main_choice in room_data.get("choice", {}).values():
                if "choice" in main_choice:
                    for sub in main_choice["choice"].values():
                        if sub.get("type") == "puzzle" and "id" in sub:
                            required.add(sub["id"])

            return required and self.solved_puzzles == required

        def action(self, data):  # runs through user choices and nested choices
            room = data["rooms"]
            room_data = room[self.room_name]

            directions = room_data["directions"]
            print(directions)
            time.sleep(1)

            choices = room_data["choice"]
            choice_keys = choices.keys()

            choice1 = input("> ").strip()

            # show room hint
            if choice1.lower() == "hint":
                print(room_data.get("hint", "No hint for this room."))
                time.sleep(1)
                return False

            if choice1 not in choice_keys:
                print("Invalid input.")
                time.sleep(1)
                return False

            # main choice (left / forward / right)
            option = choices[choice1]

            if "text" in option:
                print(option["text"])
                time.sleep(3)

            if "item" in option:
                item = option["item"]
                self.inventory_add(item)

            # if there is a nested choice (e.g. keypad / cable choice)
            if "choice" in option:
                subchoices = option["choice"]

                # stay here until puzzle solved or player goes back
                while True:
                    sub_choice = input("> ").strip()

                    if sub_choice not in subchoices:
                        print("Invalid input. Try again.")
                        time.sleep(1)
                        continue

                    option2 = subchoices[sub_choice]

                    choice_type = option2.get("type", "")

                    # PUZZLE type (keypad / password / red cable puzzle)
                    if choice_type == "puzzle":

                        #  make comparison case-insensitive for codes/passwords
                        if "code" in option2:
                            user_input = input(option2["text"]).strip()
                            code = str(option2["code"])
                            if user_input.lower() == code.lower():
                                print(option2["success"])
                                time.sleep(1)

                                # For Analytic Lab, track solved puzzles
                                if self.room_name == "Analytic Lab":
                                    puzzle_id = option2.get("id")
                                    if puzzle_id:
                                        self.solved_puzzles.add(puzzle_id)
                                        print(f"[Solved: {puzzle_id}]")
                                        time.sleep(1)
                                    if self.analytic_all_solved(room_data):
                                        return True  # room completed
                                    else:
                                        print(f"[{self.room_name} not complete yet — solve the remaining puzzles.]")
                                        time.sleep(1)
                                        return False
                                return True  # room completed

                            else:
                                print(option2["fail"])
                                time.sleep(1)
                                # stay in this nested loop to try again
                                continue

                        elif "key" in option2:
                            room_win = self.search_inventory(option2["key"])
                            if room_win == True:
                                print(option2["success"])
                                time.sleep(1)
                            else:
                                print(option2["fail"])
                                time.sleep(1)

                            return room_win

                        else:
                            if "text" in option2:
                                print(option2["text"])
                                time.sleep(3)



                    # NON-puzzle type (wrong cable, go back, etc.)
                    else:
                        if "text" in option2:
                            print(option2["text"])
                            time.sleep(3)

                        if "item" in option2:
                            item = option2["item"]
                            self.inventory_add(item)

                        if "choice" in option2:
                            subchoices2 = option2["choice"]

                            # stay here until puzzle solved or player goes back
                            while True:
                                sub_choice2 = input("> ").strip()

                                if sub_choice2 not in subchoices2:
                                    print("Invalid input. Try again.")
                                    time.sleep(1)
                                    continue

                                option3 = subchoices2[sub_choice2]

                                choice_type2 = option3.get("type", "")

                                # PUZZLE type (keypad / password / red cable puzzle)
                                if choice_type2 == "puzzle":

                                    #  make comparison case-insensitive for codes/passwords
                                    if "code" in option3:
                                        user_input2 = input(option3["text"]).strip()
                                        code2 = str(option3["code"])
                                        if user_input2.lower() == code2.lower():
                                            print(option3["success"])
                                            time.sleep(1)
                                            room_win = True

                                            return room_win  # room completed

                                        else:
                                            print(option3["fail"])
                                            time.sleep(1)
                                            # stay in this nested loop to try again
                                            continue

                                    # checks for key / item in inventory
                                    elif "key" in option3:
                                        room_win = self.search_inventory(option3["key"])
                                        if room_win == True:
                                            print(option3["success"])
                                            time.sleep(1)
                                        else:
                                            print(option3["fail"])
                                            time.sleep(1)

                                        return room_win

                                    else:
                                        if "text" in option3:
                                            print(option3["text"])
                                            time.sleep(3)




                                # NON-puzzle type (wrong cable, go back, etc.)
                                else:
                                    if "text" in option3:
                                        print(option3["text"])
                                        time.sleep(3)

                                    if "item" in option3:
                                        item2 = option3["item"]
                                        self.inventory_add(item2)

                                    # If this text is a "go back" message, leave nested loop
                                    text_lower2 = option3.get("text", "").lower()
                                    if "back at the entrance" in text_lower2 or "go back" in text_lower2:
                                        return False  # back to main room directions

                                    # otherwise (e.g. wrong cable), stay in cable/keypad menu
                                    continue

                            # no nested choice → room not finished yet
                        return False

                        # If this text is a "go back" message, leave nested loop
                    text_lower = option2.get("text", "").lower()
                    if "back at the entrance" in text_lower or "go back" in text_lower:
                        return False  # back to main room directions

                        # otherwise (e.g. wrong cable), stay in cable/keypad menu
                    continue

            # no nested choice → room not finished yet
            return False

        def inventory_add(self, item):  # adds items to the inventory list
            with open("inventory.txt", "a") as f:
                f.write(f" - {item}\n")
            with open("inventory.txt", "r") as f:
                lines = f.readlines()
                print(lines)

        def search_inventory(self, search_item):  # searches inventory for specific item
            with open("inventory.txt", "r") as f:
                lines = f.read()
                if search_item.strip(",") in lines:
                    return True
                else:
                    return False