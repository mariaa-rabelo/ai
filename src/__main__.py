from zeroPointOneGame import ZeroPointOneGame
from ai import AI

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
                game = ZeroPointOneGame('HvAI')
                game.game_loop()
            elif choice == '3':
                game = ZeroPointOneGame('AIvAI')
                game.game_loop()
            elif choice == '4':
                print("Exiting the game.")
                break
            else:
                print("Invalid choice, please try again.")

if __name__ == "__main__":
    main_menu()
