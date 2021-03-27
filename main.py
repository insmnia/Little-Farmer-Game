from Farmer import Farmer
from Manager import SaveManager

manager = SaveManager()


def start(save=None):
    farmer = Farmer()
    # если идет запуск игры с сохранением, подгружаем сессию из базы данных
    if save is not None:
        manager.show_save()
        data = manager.load_save()
        if data is not None:
            farmer.from_dict(data)
    return farmer


def game(save=None):
    farmer = start(save)
    while True:
        # использование лога
        with open("log.txt", "a") as log_file:
            print("\nВыберите пункт меню:\n"
                  "1)Вырастить яблоко потратив 1шт воды и 1 шт удобрений\n"
                  "2)Вырастить яблоко, потратив только воду\n"
                  "3)Вырастить яблоко, потратив только удобрения\n"
                  "4)Вырастить яблоко, ничего не потратив\n"
                  "5)Сходить за водой\n"
                  "6)Купить удобрения\n"
                  "7)Купить воду\n"
                  "8)Съесть яблоко на выбор\n"
                  "9)Покусать яблоко\n"
                  "10)Продать яблоко\n"
                  "11)Сыграть в монетку ( на деньги )\n"
                  "12)Посмотреть характеристики\n"
                  "0)Выйти в главное меню\n"
                  )
            menu = input(":")
            if menu == "1":
                farmer.grow_apple_with_water_and_plants()
                log_file.write("Выращено яблоко с использованием воды и удобрений\n")
            elif menu == "2":
                farmer.grow_apple_with_water()
                log_file.write("Выращено яблоко с использованием воды\n")
            elif menu == "3":
                farmer.grow_apple_with_plants()
                log_file.write("Выращено яблоко с использованием удобрений\n")
            elif menu == "4":
                farmer.grow_apple()
                log_file.write("Выращено яблоко\n")
            elif menu == "5":
                farmer.look_for_water()
                log_file.write("Отправился на поиск воды\n")
            elif menu == "6":
                farmer.buy_plants()
                log_file.write("Купил удобрение\n")
            elif menu == "7":
                farmer.buy_water()
                log_file.write("Купил воду\n")
            elif menu == "8":
                farmer.eat_apple()
                log_file.write("Съел яблоко\n")
            elif menu == "9":
                farmer.bite_apple()
                log_file.write("Откусил яблоко\n")
            elif menu == "10":
                farmer.sell_apple()
                log_file.write("Продал яблоко\n")
            elif menu == "11":
                farmer.play_coinflip()
                log_file.write("Сыграл в монетку\n")
            elif menu == "12":
                farmer.show_stats()
                continue
            elif menu == "0":
                farmer.show_stats()
                farmer.show_apples()
                manager.update_exit(exit=True)
                print("Игра окончена!")
                break
            else:
                print("Нет такого пункта меню!")
                continue
            farmer.apples_spoiling()
            # сохранение прогресса на каждом ходу для сохранности данных
            manager.save(farmer.to_dict())


if __name__ == "__main__":
    while True:
        if not manager.check_exit():
            print("Прошлая сессия была завершена некорректно. Данные были сохранены не полностью!")
        manager.update_exit()
        print(
            "Добро пожаловать в игру Маленький фермер!\n"
            "1. Начать новую игру\n"
            "2. Продолжить старую игру\n"
            "3. Посмотреть информацию о последней игре\n"
            "0. Выйти из игры\n"
        )
        menu = input(":")
        if menu == "1":
            game()
        elif menu == "2":
            game(save=True)
        elif menu == "3":
            manager.show_save()
        elif menu == "0":
            break
        else:
            print("Выберите существующий пункт меню!")
