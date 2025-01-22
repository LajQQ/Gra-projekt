import random
import time
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def generate_map(size):
    while True:
        map = []
        for i in range(size):
            row = []
            for j in range(size):
                if random.random() < 0.3:
                    row.append("#")
                else:
                    row.append(" ")
            map.append(row)
        start_x = random.randint(0, size - 1)
        start_y = random.randint(0, size - 1)
        start = (start_x, start_y)

        exit_x = random.randint(0, size - 1)
        exit_y = random.randint(0, size - 1)
        exit = (exit_x, exit_y)

        if start != exit:
            map[start_x][start_y] = "P"
            map[exit_x][exit_y] = "E"

            if path_exists(map, start, exit):
                return map, start, exit

def path_exists(map, start, exit):
    size = len(map)
    checked = []
    stack = [start]

    while len(stack) > 0:
        current_position = stack.pop()
        x, y = current_position

        if current_position == exit:
            return True

        if current_position not in checked:
            checked.append(current_position)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            for dx, dy in directions:
                nx = x + dx
                ny = y + dy
                if 0 <= nx < size and 0 <= ny < size and map[nx][ny] != "#":
                    stack.append((nx, ny))
    return False

def print_map(map):
    for row in map:
        print(" ".join(row))

def move_player(map, position, direction):
    x, y = position

    if direction == "w":
        dx, dy = -1, 0
    elif direction == "s":
        dx, dy = 1, 0
    elif direction == "a":
        dx, dy = 0, -1
    elif direction == "d":
        dx, dy = 0, 1
    else:
        dx, dy = 0, 0

    nx = x + dx
    ny = y + dy

    if 0 <= nx < len(map) and 0 <= ny < len(map[0]) and map[nx][ny] != "#":
        return (nx, ny)
    return position

def move_enemies(map, enemies):
    nextenemiesmove = []
    for ex, ey in enemies:
        map[ex][ey] = " "
        possible_directions = [
            (ex - 1, ey),
            (ex + 1, ey),
            (ex, ey - 1),
            (ex, ey + 1)
        ]
        random.shuffle(possible_directions)
        moved = False
        for nx, ny in possible_directions:
            if 0 <= nx < len(map) and 0 <= ny < len(map[0]) and map[nx][ny] == " ":
                nextenemiesmove.append((nx, ny))
                moved = True
                break

        if not moved:
            nextenemiesmove.append((ex, ey))

    for ex, ey in nextenemiesmove:
        map[ex][ey] = "X"
    return nextenemiesmove

def place_items(map, item, count):
    size = len(map)
    items = []
    while len(items) < count:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
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
        choice = input("Wybierz opcję: ").lower()
        if choice in ["1", "2", "3", "4","q","quit"]:
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
    lives = 1

    for level in range(1, levels + 1):
        clear_screen()
        print(f"Poziom {level}")

        map, player, exit = generate_map(10)
        enemies = place_items(map, "X", enemies_count)
        treasures = place_items(map, "S", random.randint(1, 3))
        holes = place_items(map, "O", random.randint(1, 2))
        start_time = time.time()

        while True:
            clear_screen()
            print_map(map)
            print(f"Życia: {lives}, Ekwipunek: {inventory}")
            remaining_time = time_limit - int(time.time() - start_time)
            print(f"Czas: {remaining_time}s")

            if remaining_time <= 0:
                print("Czas się skończył! Przegrałeś.")
                return

            move = input("Ruch WASD, B aby użyć bomby: ").lower()

            if move in ["q", "quit"]:
                print("Powrót do menu...")
                time.sleep(1)
                return

            if move not in ["w", "a", "s", "d", "b"]:
                print("Niepoprawny ruch! Użyj WASD lub B.")
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
                continue

            nextplayermove = move_player(map, player, move)

            if nextplayermove in enemies:
                if "Miecz" in inventory:
                    print("Pokonałeś przeciwnika!")
                    time.sleep(1)
                    inventory.remove("Miecz")
                    enemies.remove(nextplayermove)
                    map[nextplayermove[0]][nextplayermove[1]] = " "
                else:
                    lives -= 1
                    if lives == 0:
                        print("Zostałeś pokonany! Gra skończona.")
                        return

            elif nextplayermove in holes:
                if random.random() < 0.1:
                    lives -= 1
                    if lives == 0:
                        print("Wpadłeś do dziury i straciłeś ostatnie życie! Gra skończona.")
                        time.sleep(1)
                        return
                    else:
                        print("Wpadłeś do dziury i straciłeś życie!")
                        time.sleep(1)
                        continue
                
                dx, dy = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}[move]
                nx, ny = nextplayermove[0] + dx, nextplayermove[1] + dy
                if 0 <= nx < len(map) and 0 <= ny < len(map[0]):
                    if map[nx][ny] == "#":
                        print("Za dziurą jest ściana. Nie możesz przeskoczyć!")
                        time.sleep(1)
                        continue
                    elif (nx, ny) in enemies:
                        lives -= 1
                        if lives == 0:
                            print("Za dziurą był przeciwnik. Straciłeś życie i zginąłeś!")
                            time.sleep(1)
                            return
                        else:
                            print("Za dziurą był przeciwnik. Straciłeś życie!")
                            time.sleep(1)
                            continue
                    elif map[nx][ny] == " ":
                        nextplayermove = (nx, ny)
                else:
                    print("Za dziurą jest koniec mapy. Nie możesz przeskoczyć!")
                    time.sleep(1)
                    continue

            elif nextplayermove in treasures:
                if lives == 2:
                    treasure = random.choice(["Bomba", "Miecz"])
                else:
                    treasure = random.choice(["Bomba", "Miecz", "Serce"])

                if treasure == "Serce" and lives < 2:
                    lives += 1
                elif treasure != "Serce":
                    inventory.append(treasure)
                print(f"Znalazłeś: {treasure}!")
                time.sleep(1)
                treasures.remove(nextplayermove)

            if nextplayermove == exit:
                print(f"Brawo! Ukończyłeś poziom {level}.")
                input("Naciśnij Enter, aby przejść dalej.")
                break

            map[player[0]][player[1]] = " "
            map[nextplayermove[0]][nextplayermove[1]] = "P"
            player = nextplayermove

            enemies = move_enemies(map, enemies)

    print("Gratulacje! Ukończyłeś wszystkie poziomy!")

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
        print("Wychodzenie...")
        break
    elif choice == "q":
        print("Wychodzenie...")
        break
    elif choice == "quit":
        print("Wychodzenie...")
        break