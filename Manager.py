import os
import json





class SaveManager(object):

    def __init__(self):
        self.path = os.path.abspath(__file__)[:-9]

    def save(self, farmer_stats: dict) -> None:
        save = {}
        save["data"] = farmer_stats
        with open(self.path + "db.json", 'w') as db:
            json.dump(save, db)

    def show_save(self) -> None:
        with open(self.path + "db.json", 'r') as db:
            try:
                save = json.load(db)
            except json.decoder.JSONDecodeError:
                print("Нет информации о прошлой игре!")
                return
        print(
            ("Уровень здоровья :: {health}\n"
             "Уровень голода :: {hunger}\n"
             "Запас воды :: {water}\n"
             "Запас удобрений :: {plants}\n"
             "Количество денег :: {money}\n").format(
                health=save["data"]["health"], hunger=save["data"]["hunger"],
                water=save["data"]["water"], plants=save["data"]["plants"], money=save["data"]["money"]
            )
        )
        for number, apple in enumerate(save["data"]["apples"]):
            print(("--------------------------\n"
                   "{number})Apple color : {color}\n"
                   "{number})Apple smooth : {smooth}\n"
                   "{number})Apple size : {size}\n"
                   "{number})Apple taste : {taste}\n"
                   "{number})Apple state : {state}\n"
                   "--------------------------").format(
                number=number + 1, color=apple["color"], smooth=apple["smooth"],
                size=apple["size"], taste=apple["taste"], state=apple["state"])
            )
        return None

    def load_save(self) -> dict:
        with open(self.path + "db.json", 'r') as db:
            try:
                save = json.load(db)
            except json.decoder.JSONDecodeError:
                return None
        return save

    @staticmethod
    def check_exit() -> bool:
        with open("check.txt", "r") as exit_check_file:
            state = exit_check_file.read()
            if str(state) == "0":
                return False
        return True

    @staticmethod
    def update_exit(exit: bool = None) -> None:
        with open("check.txt", "w") as exit_check_file:
            if exit is not None:
                exit_check_file.write("0")
            else:
                exit_check_file.write("1")
