from Apple import Apple
from random import randint


class Farmer(object):
    @staticmethod
    def create_apple(water=None, plants=None, start=None) -> Apple:
        apple = Apple(water, plants, start)
        return apple

    def __init__(self):
        # по умолчанию здоровье = 100, голод = 0(макс - 30), запас воды = 9, запас удобрений = 5
        # денег нет, и на старте выдается 5 случайных яблок
        self.health = 100
        self.hunger = 0
        self.water = 9
        self.plants = 5
        self.money = 0
        self.apples = [Farmer.create_apple(start=1) for _ in range(5)]
        self.apple_count = 5

    # создание json объекта Фермера
    def to_dict(self) -> dict:
        farmer = {
            "health": self.health,
            "hunger": self.hunger,
            "water": self.water,
            "plants": self.plants,
            "money": self.money,
            "apples": [apple.to_dict() for apple in self.apples],
            "apple_count": self.apple_count,
        }
        return farmer

    # загрузка данных фермера из json ( словаря )
    def from_dict(self, data) -> None:
        self.health = data["data"]["health"]
        self.hunger = data["data"]["hunger"]
        self.water = data["data"]["water"]
        self.plants = data["data"]["plants"]
        self.money = data["data"]["money"]
        self.apple_count = data["data"]["apple_count"]
        self.apples = []
        for apple_json in data["data"]["apples"]:
            apple = Apple()
            apple.from_dict(apple_json)
            self.apples.append(apple)
        return None

    def show_stats(self) -> None:
        print(("Здоровье фермера : < {health} >\n"
               "Голод фермера : < {hunger} >\n"
               "Запас воды фермера : < {water} >\n"
               "Удобрения фермера : < {plants} >\n"
               "Деньги фермера : < {money} >\n"
               "Кол-во яблок фермера : < {apple_count} >\n").format(
                   health=self.health,
                   hunger=self.hunger,
                   water=self.water,
                   plants=self.plants,
                   money=self.money,
                   apple_count=self.apple_count))
        return None

    def show_apples(self) -> None:
        for number, apple in enumerate(self.apples):
            print(("--------------------------\n"
                   "{number})Apple color : {color}\n"
                   "{number})Apple smooth : {smooth}\n"
                   "{number})Apple size : {size}\n"
                   "{number})Apple taste : {taste}\n"
                   "{number})Apple state : {state}\n"
                   "--------------------------").format(number=number + 1,
                                                        color=apple.color,
                                                        smooth=apple.smooth,
                                                        size=apple.size,
                                                        taste=apple.taste,
                                                        state=apple.state))
        return None

    # вспомогательная функция проверки баланса при покупке воды и/или удобрений
    def check_balance(self, needed_amount_of_money: int) -> bool:
        return self.money >= needed_amount_of_money

    # проверка уровня здоровья и голода. Если здоровье опустилось ниже 0 или голод больше 30 - смерть
    def check_health(self) -> None:
        if self.health <= 0 or self.hunger >= 30:
            print("\nФермер умер... Конец игры!\n")
            self.show_stats()
            exit()
        return None

    def check_hunger(self) -> None:
        if self.hunger > 10:
            self.health -= 10
        elif self.hunger > 20:
            self.health -= 20

        self.check_health()
        return None

    # с каждым действием фермер голодает
    def hunger_up(self) -> None:
        self.hunger += 5
        self.check_hunger()
        return None

    # регулировка параметров персонажа ( голод и здоровье )
    def normalize(self) -> None:
        if self.health > 100:
            self.health = 100
        if self.hunger < 0:
            self.hunger = 0
        return None

    # вспомогательный метод для выборки яблока под определённую задачу ( параметр task )
    def choice(self, task) -> None or int:
        try:
            self.show_apples()
            apple_index = int(input(f"Введите номер яблока, чтобы {task}:"))
            if apple_index - 1 <= len(self.apples) and self.apples:
                return apple_index - 1
        except:
            return None

    def sell_apple(self) -> None:
        number_of_apple_to_sell = self.choice(task="продать")

        if number_of_apple_to_sell is not None:
            self.money += self.apples[number_of_apple_to_sell].price()
            self.apples.pop(number_of_apple_to_sell)
            self.apple_count -= 1
        else:
            print("У вас нет столько яблок!")
        return None

    # вырастить яблоко с использованием удобрений и воды - яблоко обязательно будет превосходным
    def grow_apple_with_water_and_plants(self) -> None:
        if self.water and self.plants:
            self.plants -= 1
            self.water -= 1
            self.apples.append(Farmer.create_apple(water=1, plants=1))
            self.apple_count += 1
            print("Вы вырастили новое яблоко!")
            self.hunger_up()
        else:
            print("У вас не хватает воды и/или удобрений. Навестите магазин!")
        return None

    # вырастить яблоко с использованием воды - яблоко будет либо огромным, либо большим
    def grow_apple_with_water(self) -> None:
        if self.water:
            self.water -= 1
            self.apples.append(Farmer.create_apple(water=1))
            self.apple_count += 1
            print("Вы вырастили новое яблоко!")
            self.hunger_up()
            self.check_hunger()
        else:
            print(
                "У вас не хватает воды. Сходите за ней или купить в магазине, хорошо?"
            )

        return None

    # вырастить яблоко с использованием удобрений - яблоко обязательно будет сладким
    def grow_apple_with_plants(self) -> None:
        if self.plants:
            self.plants -= 1
            self.apples.append(Farmer.create_apple(plants=1))
            self.apple_count += 1
            self.hunger_up()
            print("Вы вырастили новое яблоко!")
        else:
            print("У вас не хватает удобрений. Может стоит навестить магазин?")
        return None

    def grow_apple(self) -> None:
        self.apples.append(Farmer.create_apple())
        self.apple_count += 1
        self.hunger_up()
        print("Вы вырастили новое яблоко!")
        return None

    def look_for_water(self) -> None:
        self.water += 3
        print(f"Вы нашли воду!\nТекущий запас воды: <{self.water}>")
        self.hunger_up()
        return None

    def buy_plants(self) -> None:
        if self.check_balance(5):
            self.plants += 1
            self.money -= 5
            print(
                f"Вы купили удобрения!\nТекущий запас удобрений: <{self.plants}>"
            )
        else:
            print("Упс... Кажется у вас не хватает денег(")
        return None

    def buy_water(self) -> None:
        if self.check_balance(3):
            self.water += 3
            self.money -= 3
            print(f"Вы купили воду!\nТекущий запас воды: <{self.water}>")
        else:
            print("Упс... Кажется у вас не хватает денег(")
        return None

    def eat_apple(self) -> None:
        number_of_apple_to_eat = self.choice(task="съесть")
        if number_of_apple_to_eat is not None:
            apple = self.apples[number_of_apple_to_eat]
            health, hunger = apple.value()
            self.hunger -= hunger
            self.health -= health
            self.normalize()
            self.apple_count -= 1
            self.apples.pop(number_of_apple_to_eat)
        else:
            print("У вас нет столько яблок. Выберите из списка")
        return None

    # покусать можно только большое или огромное яблоко, но ТОЛЬКО 1 раз.
    # цена после "обгрызания" яблока снижается
    def bite_apple(self) -> None:
        number_of_apple_to_bite = self.choice(task="покусать")
        if number_of_apple_to_bite is not None:
            apple = self.apples[number_of_apple_to_bite]
            if apple.size in ("огромное",
                              "большое") and apple.state != "покусанное":
                self.hunger -= apple.bite()
                self.normalize()
            else:
                print("Можно покусать только целое яблоко")
        else:
            print("У вас нет столько яблок. Выберите из списка")
        return None

    # каждый ход яблоко должно портиться( исключением является просмотр статистики )
    def apples_spoiling(self) -> None:
        for number in range(len(self.apples)):
            apple = self.apples[number]
            states_of_spoiling = (("гладкое", "с морщинками"), ("с морщинками",
                                                                "сморщенное"))
            for state in states_of_spoiling:
                if apple.smooth == state[0]:
                    apple.smooth = state[1]
                    break
                elif apple.smooth == "сморщенное":
                    apple.color = "коричневое"
                    break
                elif apple.smooth == "сморщенное" and apple.color == "коричневое":
                    apple.color = "черное"
                    break

        return None

    # игра - монетка. Ставишь яблоко на кон. Выигрываешь - получаешь стоимость яблока на руки, проигрываешь - теряешь яблоко
    def play_coinflip(self) -> None:
        chosen_apple = self.choice(task="поставить на кон")
        if chosen_apple is not None:
            win_prize = self.apples[chosen_apple].price()
            print(f"Вы поставили на кон яблоко ценою {win_prize}")
            if randint(0, 1) == 1:
                print("И вы удвоили свою ставку!")
                self.money += win_prize
            else:
                print("Вы проиграли и потеряли своё яблоко")
                self.apples.pop(chosen_apple)
        else:
            print("У вас нет столько яблок!")
