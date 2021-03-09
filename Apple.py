import random


class Apple(object):

    def __init__(self, water=None, plants=None, start=False):
        COLOR = ("красное", "зеленое", "желтое", "коричневое", "черное")
        SIZE = ("огромное", "большое", "среднее", "маленькое")
        TASTE = ("сладкое", "горькое", "кислое")
        # None - отсутствие компонента
        # Если мы только начинаем играть, то яблоки могут быть любыми
        if start:
            self.size = SIZE[random.randint(0, 4 - 1)]
            self.taste = TASTE[random.randint(0, 3 - 1)]
        else:
            # если используем воду для выращивания, то размер будет либо большим, либо огромным
            if water is not None:
                self.size = SIZE[random.randint(0, 2-1)]
            else:
                self.size = SIZE[random.randint(2, 4-1)]
            # если используем удобрения для выращивания, то яблоко обязательно будет сладким
            if plants is not None:
                self.taste = "сладкое"
            else:
                self.taste = TASTE[random.randint(1, 3 - 1)]

        self.color = COLOR[random.randint(0, 5 - 1)]
        self.state = "целое"
        self.smooth = "гладкое"

    # создание json объекта Яблока
    def to_dict(self) -> dict:
        apple = {
            "size": self.size, "color": self.color, "state": self.state,
            "smooth": self.smooth, "taste": self.taste
        }
        return apple

    # загрузка информации о яблоке из json( словаря )
    def from_dict(self, data: dict):
        self.size = data["size"]
        self.color = data["color"]
        self.taste = data["taste"]
        self.smooth = data["smooth"]
        self.state = data["state"]

    # оценка качества яблока. Подсчет стоимость яблока для продажи
    def price(self) -> int:
        price = 10
        pricing_info = (
            ("красное", 2), ("зеленое", 1), ("коричневое", -1),
            ("черное", -2), ("гладкое", 1), ("сморщенное", -1),
            ("огромное", 2), ("большое", 1), ("маленькое", -1),
            ("сладкое", 1), ("кислое", -1),
            ("покусанное", -3),
        )
        for stats in pricing_info:
            if self.color == stats[0] or self.smooth == stats[0] or\
                self.size == stats[0] or self.taste == stats[0] or\
                    self.state == stats[0]:
                price += stats[1]

        return int(price*0.4)
    # оценка качества яблока. Подсчет кол-ва утоляемого голода и отнимаемого здоровья

    def value(self) -> tuple:
        hunger = 0
        health = 0
        apple_size_and_hunger = (
            ("огромное", 4, 2), ("большое", 3,
                                 1.5), ("среднее", 2, 1), ("маленькое", 1, 0.5)
        )
        for size in apple_size_and_hunger:
            if self.state == "целое" and self.size == size[0]:
                hunger -= size[1]
            elif self.state != "целое" and self.size == size[0]:
                hunger -= size[2]

        apple_state_and_health = (
            ("коричневое", 5), ("черное", 2)
        )
        for state in apple_state_and_health:
            if self.state == state[0]:
                health -= state[1]

        apple_taste_and_health = (
            ("кислое", .5), ("горькое", 1)
        )

        for taste in apple_taste_and_health:
            if self.taste == taste[0]:
                health -= taste[1]
        return (hunger if self.state != "покусанное" else int(hunger*.6), health)

    # оценка качества яблока. Подсчет кол-ва утоляемого голода при укусе яблока
    def bite(self) -> int:
        hunger = 0
        if self.size == "огромное" and self.state != "покусанное":
            hunger += 1.5
            self.state = "покусанное"
        if self.size == "большое" and self.state != "покусанное":
            hunger += 1
            self.state = "покусанное"
        return hunger
