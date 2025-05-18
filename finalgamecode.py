introduction = 1
print('''
  ______         __       __                                __                            __       __                      __        __ 
 /      \       /  \     /  |                              /  |                          /  |  _  /  |                    /  |      /  |
/$$$$$$  |      $$  \   /$$ |  ______   ________   ______  $$/  _______    ______        $$ | / \ $$ |  ______    ______  $$ |  ____$$ |
$$ |__$$ |      $$$  \ /$$$ | /      \ /        | /      \ /  |/       \  /      \       $$ |/$  \$$ | /      \  /      \ $$ | /    $$ |
$$    $$ |      $$$$  /$$$$ | $$$$$$  |$$$$$$$$/ /$$$$$$  |$$ |$$$$$$$  |/$$$$$$  |      $$ /$$$  $$ |/$$$$$$  |/$$$$$$  |$$ |/$$$$$$$ |
$$$$$$$$ |      $$ $$ $$/$$ | /    $$ |  /  $$/  $$    $$ |$$ |$$ |  $$ |$$ |  $$ |      $$ $$/$$ $$ |$$ |  $$ |$$ |  $$/ $$ |$$ |  $$ |
$$ |  $$ |      $$ |$$$/ $$ |/$$$$$$$ | /$$$$/__ $$$$$$$$/ $$ |$$ |  $$ |$$ \__$$ |      $$$$/  $$$$ |$$ \__$$ |$$ |      $$ |$$ \__$$ |
$$ |  $$ |      $$ | $/  $$ |$$    $$ |/$$      |$$       |$$ |$$ |  $$ |$$    $$ |      $$$/    $$$ |$$    $$/ $$ |      $$ |$$    $$ |
$$/   $$/       $$/      $$/  $$$$$$$/ $$$$$$$$/  $$$$$$$/ $$/ $$/   $$/  $$$$$$$ |      $$/      $$/  $$$$$$/  $$/       $$/  $$$$$$$/ 
                                                                         /  \__$$ |                                                     
                                                                         $$    $$/                                                      
                                                                          $$$$$$/                                                       
                     
                                            ** Press [s] to start the game **
''')
startgame = input()
if startgame == 's':
    introduction += 1

if introduction == 2:
    import curses
    import random
    import time

# Initialize menu items and scoreboard
    menu = ['Home', 'Play', 'Scoreboard', 'Exit']
    scoreboard = 0
    apple_count = 0


# generate 5x5 board
    def generate_board():
        size = 0

        if 0 <= scoreboard % 25 < 6:
            size = 3
        elif 6 <= scoreboard % 25 < 12:
            size = 4
        elif 12 <= scoreboard % 25 < 18:
            size = 5
        elif 18 <= scoreboard % 25:
            size = 6

        while True:
            board = [['·' for _ in range(size)] for _ in range(size)]
            path = [(0, 0)]
            visited = set(path)
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            while len(path) < size * (size - 1):
                r, c = path[-1]
                random.shuffle(directions)
                for dr, dc in directions:
                    new_r, new_c = r + dr, c + dc
                    if 0 <= new_r < size and 0 <= new_c < size and (new_r, new_c) not in visited:
                        path.append((new_r, new_c))
                        visited.add((new_r, new_c))
                        break
                else:
                    break

            for _ in range(size):
                while True:
                    b = random.randint(0, size * size - 1)
                    row, col = divmod(b, size)
                    if board[row][col] == '·' and (row, col) not in path:
                        board[row][col] = 'X'
                        break

            if is_solvable(board, (0, 0)):
                return board, path


# Using DFS to Find Paths
    def is_solvable(board, start):
        size = len(board)
        empty_cells = sum(row.count('·') for row in board)
        visited = set()

        def dfs(row, col, steps):
            if steps == empty_cells:
                return True

            visited.add((row, col))
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

            for dr, dc in directions:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < size and 0 <= new_col < size:
                    if (new_row, new_col) not in visited and board[new_row][new_col] == '·':
                        if dfs(new_row, new_col, steps + 1):
                            return True

            visited.remove((row, col))
            return False

        return dfs(start[0], start[1], 1)


# print board
    def print_board(stdscr, board, pos):
        h, w = stdscr.getmaxyx()

        for r, row in enumerate(board):
            for c, cell in enumerate(row):
                x = c * 2 + w // 2 - len(row)
                y = r + h // 2 - len(board) // 2
                if (r, c) == pos:
                    stdscr.addstr(y, x, '🍎')
                elif cell == 'O':
                    stdscr.addstr(y, x, '🍏')
                elif cell == 'X':
                    stdscr.addstr(y, x, '🐗')
                else:
                    stdscr.addstr(y, x, cell)

        stdscr.addstr(1, w - 10, f"Score: {scoreboard}")


# movement according to key input
    def move_player(board, pos, move):
        size = len(board)
        row, col = pos

        if move == 'w':
            new_pos = (row - 1, col)
        elif move == 's':
            new_pos = (row + 1, col)
        elif move == 'a':
            new_pos = (row, col - 1)
        elif move == 'd':
            new_pos = (row, col + 1)
        else:
            return pos

        if new_pos[0] < 0 or new_pos[0] >= size or new_pos[1] < 0 or new_pos[1] >= size:
            return pos
        if board[new_pos[0]][new_pos[1]] in ['X', 'O']:
            return pos

        board[row][col] = 'O'
        return new_pos


# check all cells are visited
    def all_cells_visited(board, pos):
        return all(cell == 'O' or (r, c) == pos for r, row in enumerate(board) for c, cell in enumerate(row) if cell != 'X')


# play game function
    def play_game(stdscr):
        global scoreboard
        curses.curs_set(0)
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_RED)

        board, blocked = generate_board()
        pos = (0, 0)
        board[0][0] = 'P'
        original_board = [row[:] for row in board]

        stdscr.nodelay(True)
        stdscr.timeout(10)

        start_time = 15
        end_time = time.time() + start_time
        running = False

        timer_str = None
        while True:
            if running:
                elapsed_time = max(0, end_time - time.time())

                if elapsed_time <= 0:
                    stdscr.nodelay(False)
                    stdscr.timeout(-1)

                    stdscr.addstr(0, 0, "Game Over! Want to try again? (y/n)", curses.A_BOLD)
                    stdscr.refresh()
                    if stdscr.getch() == ord('y'):
                        board, blocked = generate_board()
                        original_board = [row[:] for row in board]
                        pos = (0, 0)
                        board[0][0] = 'P'

                        end_time = time.time() + start_time
                        stdscr.nodelay(True)
                        stdscr.timeout(10)
                    else:
                        break

            # calculate time
                minutes = int(elapsed_time // 60)
                seconds = int(elapsed_time % 60)
                hundredths = int((elapsed_time * 100) % 100)
                timer_str = f"{minutes:02}:{seconds:02}.{hundredths:02}"

            print_board(stdscr, board, pos)
            running = True
            key = stdscr.getch()

            stdscr.clear()
            stdscr.addstr(1, 1, f"Timer: {timer_str}")
            stdscr.refresh()

            if key == ord('q'):
                break  

            elif key == ord('r'):
                board = [row[:] for row in original_board]
                pos = (0, 0)
                board[0][0] = 'P'
                continue

            elif key in [ord('w'), ord('s'), ord('a'), ord('d')]:
                move = chr(key)
                new_pos = move_player(board, pos, move)
                if new_pos != pos:
                    pos = new_pos
                    board[pos[0]][pos[1]] = 'P'

                print_board(stdscr, board, pos)

                if all_cells_visited(board, pos):
                    stdscr.nodelay(False)
                    stdscr.timeout(-1)

                    scoreboard += 1
                    stdscr.addstr(0, 0, "Congratulations! You succeeded! Want to start a new game? (y/n)", curses.A_BOLD)
                    stdscr.refresh()

                    if stdscr.getch() == ord('y'):
                        board, blocked = generate_board()
                        original_board = [row[:] for row in board]
                        pos = (0, 0)
                        board[0][0] = 'P'

                        end_time = time.time() + start_time

                        stdscr.nodelay(True)
                        stdscr.timeout(10)
                    else:
                        break

                if not any(move_player(board, pos, m) != pos for m in 'wsad'):
                    stdscr.nodelay(False)
                    stdscr.timeout(-1)

                    stdscr.addstr(0, 0, "Game Over! Want to try again? (y/n)", curses.A_BOLD)
                    stdscr.refresh()
                    if stdscr.getch() == ord('y'):
                        board, blocked = generate_board()
                        original_board = [row[:] for row in board]
                        pos = (0, 0)
                        board[0][0] = 'P'

                        end_time = time.time() + start_time
                        stdscr.nodelay(True)
                        stdscr.timeout(10)
                    else:
                        break


# drawing apple
    def draw_apple(stdscr):
        global scoreboard, apple_count
        stdscr.clear()
        h, w = stdscr.getmaxyx()

        start_row = h // 2 - 5
        start_col = w // 2 - 5

        apple_shape = [
            "██   ",
            " ███ ",
            "█████",
            "█████",
            " ███ ",
        ]

        curses.start_color()
        curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    # draw apple along with scoreboard 
        for i in range(5):
            for j in range(5):
                if i + j * 5 <= scoreboard % 25:
                    if i == 0:
                        stdscr.addstr(start_row + i, start_col + j, apple_shape[i][j], curses.color_pair(2))
                    else:
                        stdscr.addstr(start_row + i, start_col + j, apple_shape[i][j], curses.color_pair(1))
    
        if scoreboard != 0 and scoreboard % 25 == 0:
            stdscr.addstr(start_row + 9, start_col + 1, "Earn an apple!", curses.A_BOLD)
            apple_count += 1

    
        stdscr.addstr(h - 3, w // 2 - 10, f"Score: {scoreboard}")
        stdscr.addstr(h - 2, w // 2 - 10, f"Apple: {apple_count}")

        stdscr.refresh()
        stdscr.getch() 


# print menu
    def print_menu(stdscr, selected_row_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        for idx, row in enumerate(menu):
            x = w // 2 - len(row) // 2
            y = h // 2 - len(menu) // 2 + idx
            if idx == selected_row_idx:
                stdscr.attron(curses.color_pair(1))  
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)  
        stdscr.refresh()


# main function
    def main(stdscr):
        global scoreboard, apple_count
        curses.curs_set(0)

    
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  #
    

        current_row = 0
        print_menu(stdscr, current_row)

        while True:
            curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  
            print_menu(stdscr, current_row)

            key = stdscr.getch()

            if key == curses.KEY_UP and current_row > 0:
                current_row -= 1
            elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
                current_row += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                stdscr.clear()
                if current_row == 1:
                    play_game(stdscr)
                elif current_row == 2:
                    print_center(stdscr, f"Scoreboard: {scoreboard}")
                    stdscr.getch()
                elif current_row == 0:  
                    draw_apple(stdscr)
                elif current_row == len(menu) - 1:
                    break
                print_menu(stdscr, current_row)  

            print_menu(stdscr, current_row)


# print at center
    def print_center(stdscr, text):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        x = w // 2 - len(text) // 2
        y = h // 2
        stdscr.addstr(y, x, text)
        stdscr.refresh()


    curses.wrapper(main)




