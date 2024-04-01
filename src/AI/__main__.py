from zeroPointOneGame import ZeroPointOneGame

def main_menu():
        while True:
            print("Welcome to Zero Point One! :)")
            print("1. Human vs. Human")
            print("2. Human vs. AI")
            print("3. AI vs. AI")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == '1':
                game = ZeroPointOneGame('HvH')
                game.game_loop()
            elif choice == '2':
                print("Choose your difficulty")
                print("1. Easy")
                print("2. Hard")
                print("3. Go back")
                c2 = input("Enter your choice: ")
                if c2 == '1':
                    game = ZeroPointOneGame('HvAI', 0, 2)
                    game.game_loop()
                elif c2 == '2':
                    game = ZeroPointOneGame('HvAI', 0, 3)
                    game.game_loop()
                elif c2 == '3':
                    print()
                    print()
                    print()
                    main_menu()
                else:
                    print("Invalid choice, please try again.")
            elif choice == '3':
                print("Choose the difficulty for Red")
                print("1. Easy")
                print("2. Hard")
                print("3. Go back")
                c1 = input("Enter your choice: ")
                if c1 == '1':
                    print("Choose the difficulty for Blue")
                    print("1. Easy")
                    print("2. Hard")
                    print("3. Go back")
                    c2 = input("Enter you choice: ")
                    if c2 == '1':
                        game = ZeroPointOneGame('AIvAI', 2, 2)
                        game.game_loop()
                    elif c2 == '2':
                        game = ZeroPointOneGame('AIvAI', 2, 3)
                    elif c2 == '3':
                        print()
                        print()
                        print()
                        main_menu()
                    else:
                        print("Invalid choice, please try again.")
                elif c1 == '2':
                    print("Choose the difficulty for Blue")
                    print("1. Easy")
                    print("2. Hard")
                    print("3. Go back")
                    c2 = input("Enter you choice: ")
                    if c2 == '1':
                        game = ZeroPointOneGame('AIvAI', 3, 2)
                        game.game_loop()
                    elif c2 == '2':
                        game = ZeroPointOneGame('AIvAI', 3, 3)
                    elif c2 == '3':
                        print()
                        print()
                        print()
                        main_menu()
                    else:
                        print("Invalid choice, please try again.")
                elif c1 == '3':
                    print()
                    print()
                    print()
                    main_menu()
                else:
                    print("Invalid choice, please try again.")
            elif choice == '4':
                print("Exiting the game.")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
