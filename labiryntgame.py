import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_map(size):
    while True:
        map = [["#" if random.random() < 0.3 else " " for _ in range(size)] for _ in range(size)]
        start = (random.randint(0, size - 1), random.randint(0, size - 1))
        exit = (random.randint(0, size - 1), random.randint(0, size - 1))
        if start != exit and abs(start[0] - exit[0]) + abs(start[1] - exit[1]) > 3:
            map[start[0]][start[1]] = "P"
            map[exit[0]][exit[1]] = "E"
            if path_exists(map, start, exit):
                return map, start, exit

def path_exists(map, start, exit):
    size = len(map)
    visited = set()
    stack = [start]

    while stack:
        x, y = stack.pop()
        if (x, y) == exit:
            return True
        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < size and 0 <= ny < size and map[nx][ny] != "#":
                    stack.append((nx, ny))
    return False

def print_map(map):
    for row in map:
        print(" ".join(row))

def move_player(map, position, direction):
    x, y = position
    moves = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
    dx, dy = moves.get(direction, (0, 0))
    nx, ny = x + dx, y + dy
    if 0 <= nx < len(map) and 0 <= ny < len(map[0]) and map[nx][ny] != "#":
        return (nx, ny)
    return position

def move_enemies(map, enemies):
    new_enemies = []
    for ex, ey in enemies:
        map[ex][ey] = " "
        directions = [(ex + dx, ey + dy) for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]]
        random.shuffle(directions)
        for nx, ny in directions:
            if 0 <= nx < len(map) and 0 <= ny < len(map[0]) and map[nx][ny] == " ":
                new_enemies.append((nx, ny))
                break
        else:
            new_enemies.append((ex, ey))
    for ex, ey in new_enemies:
        map[ex][ey] = "X"
    return new_enemies

def place_items(map, item, count_range):
    size = len(map)
    items = []
    count = random.randint(*count_range)
    while len(items) < count:
        x, y = random.randint(0, size - 1), random.randint(0, size - 1)
        if map[x][y] == " ":
            map[x][y] = item
            items.append((x, y))
    return items

def main_menu():
    while True:
        print("--- Labirynt z przeszkodami ---")
        print("1. Graj")
        print("2. Ustawienia")
        print("3. Instrukcje")
        print("4. Wyjdź")
        choice = input("Wybierz opcję: ")
        if choice in ["1", "2", "3", "4"]:
            return choice
        else:
            print("Niepoprawny wybór. Spróbuj ponownie.")

def settings(enemies_count, levels, time_limit):
    while True:
        print("--- Ustawienia Gry---")
        print(f"Przeciwnicy: {enemies_count}")
        print(f"Poziomy: {levels}")
        print(f"Czas na poziom: {time_limit} sekund")
        choice = input("Chcesz zmienić ustawienia? (tak/nie/quit): ").lower()
        if choice == "t":
            enemies_count = int(input("Podaj liczbę przeciwników: "))
            levels = int(input("Podaj liczbę poziomów: "))
            time_limit = int(input("Podaj czas na poziom (w sekundach): "))
            return enemies_count, levels, time_limit
        elif choice == "tak":
            enemies_count = int(input("Podaj liczbę przeciwników: "))
            levels = int(input("Podaj liczbę poziomów: "))
            time_limit = int(input("Podaj czas na poziom (w sekundach): "))
            return enemies_count, levels, time_limit
        elif choice == "n":
            return enemies_count, levels, time_limit
        elif choice == "nie":
            return enemies_count, levels, time_limit        
        elif choice == "q":
            return enemies_count, levels, time_limit
        elif choice == "quit":
            return enemies_count, levels, time_limit
        else:
            print("Niepoprawny wybór. Spróbuj ponownie.")

def instructions():
    print("--- Instrukcje ---")
    print("Celem gry jest dotarcie do wyjścia (E).")
    print("Poruszaj się klawiszami WASD. Unikaj przeciwników (X) i dziur (O).")
    print("Otwieraj skarby (S) i zbieraj przedmioty które pomogą ci w przejściu gry!")
    input("Naciśnij Enter, aby wrócić do menu.")

def play_game(enemies_count, levels, time_limit):
    inventory = []
    for level in range(1, levels + 1):
        clear_screen()
        print(f"Poziom {level}")

        map, player, exit = generate_map(10)
        enemies = place_items(map, "X", (enemies_count, enemies_count))
        black_holes = place_items(map, "O", (1, 2))
        treasures = place_items(map, "S", (1, 3))

        start_time = time.time()
        lives = 1

        while True:
            clear_screen()
            print_map(map)
            print(f"Życia: {lives}, Ekwipunek: {inventory}")
            remaining_time = time_limit - int(time.time() - start_time)
            print(f"Czas: {remaining_time}s")

            if remaining_time <= 0:
                print("Czas się skończył! Przegrałeś.")
                return

            move = input("Ruch (WASD, B aby użyć bomby): ").lower()
            if move not in ["w", "a", "s", "d", "b"]:
                print("Niepoprawny ruch!")
                time.sleep(1)
                continue

            if move == "b":
                if "Bomba" in inventory:
                    print("Użyto bomby! Niszczenie obiektów w promieniu 2x2.")
                    x, y = player
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < len(map) and 0 <= ny < len(map[0]):
                                if map[nx][ny] == "#":
                                    map[nx][ny] = " "
                                elif (nx, ny) in enemies:
                                    enemies.remove((nx, ny))
                                    map[nx][ny] = " "
                    inventory.remove("Bomba")
                    time.sleep(1)
                else:
                    print("Nie masz bomby!")
                    time.sleep(1)

            new_player = move_player(map, player, move)
            if new_player in enemies:
                if "Miecz" in inventory:
                    print("Pokonałeś przeciwnika!")
                    inventory.remove("Miecz")
                    enemies.remove(new_player)
                    map[new_player[0]][new_player[1]] = " "
                else:
                    lives -= 1
                    if lives == 0:
                        print("Zostałeś pokonany!")
                        return

            elif new_player in black_holes:
                if random.random() < 0.1:
                    print("Wpadłeś w czarną dziurę i zginąłeś!")
                    return
                else:
                    dx, dy = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}[move]
                    nx, ny = new_player[0] + dx, new_player[1] + dy
                    if 0 <= nx < len(map) and 0 <= ny < len(map[0]):
                        if (nx, ny) in enemies:
                            lives -= 1
                            if lives == 0:
                                print("Przeskoczyłeś czarną dziurę, ale przeciwnik cię pokonał!")
                                return
                            else:
                                print("Przeskoczyłeś czarną dziurę, ale straciłeś życie z powodu przeciwnika!")
                                time.sleep(1)
                        elif map[nx][ny] == " ":
                            new_player = (nx, ny)
                        else:
                            print("Nie możesz przeskoczyć! Blokada.")
                            time.sleep(1)
                            continue

            elif new_player in treasures:
                if lives == 2:
                    treasure = random.choice(["Bomba", "Miecz"])
                else:
                    treasure = random.choice(["Bomba", "Miecz", "Serce"])
                if treasure == "Serce" and lives < 2:
                    lives += 1
                elif treasure != "Serce":
                    inventory.append(treasure)
                print(f"Znalazłeś: {treasure}!")
                treasures.remove(new_player)

            if new_player == exit:
                print(f"Brawo! Poziom {level} ukończony.")
                input("Enter aby kontynuować.")
                break

            map[player[0]][player[1]] = " "
            map[new_player[0]][new_player[1]] = "P"
            player = new_player

            enemies = move_enemies(map, enemies)

    print("Przeszedłeś wszystkie poziomy! Gratulacje!")

if __name__ == "__main__":
    enemies_count, levels, time_limit = 3, 3, 120

    while True:
        choice = main_menu()
        if choice == "1":
            play_game(enemies_count, levels, time_limit)
        elif choice == "2":
            enemies_count, levels, time_limit = settings(enemies_count, levels, time_limit)
        elif choice == "3":
            instructions()
        elif choice == "4":
            print("Dziękujemy za grę!")
            break
