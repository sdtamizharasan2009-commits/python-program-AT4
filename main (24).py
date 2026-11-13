import os

def save_returns(books):
    with open("returns.log", "a", encoding="utf-8") as log:
        for book in books:
            log.write(book + "\n")


def process(day_file):
    try:
        with open(day_file, "r", encoding="utf-8") as file:
            books = file.read().splitlines()

        save_returns(books)

    except FileNotFoundError as error:
        with open("error.log", "a", encoding="utf-8") as log:
            log.write(f"{day_file}: {error}\n")

    except PermissionError as error:
        with open("error.log", "a", encoding="utf-8") as log:
            log.write(f"{day_file}: {error}\n")


for day in range(1, 4):
    with open(f"day{day}.txt", "w", encoding="utf-8") as file:
        file.write(f"Book A - Day {day}\n")
        file.write(f"Book B - Day {day}\n")


open("returns.log", "w").close()
open("error.log", "w").close()

process("day1.txt")
process("day2.txt")
process("missing_day.txt")
process("day3.txt")

with open("returns.log", "r", encoding="utf-8") as file:
    print(file.read())

with open("error.log", "r", encoding="utf-8") as file:
    print(file.read())