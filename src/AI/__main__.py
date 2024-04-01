from zeroPointOneGame import ZeroPointOneGame

def main_menu():
        """
        Display the main menu and handle the user's choice.

        This function continuously displays the main menu options until the user
        decides to exit the game. It handles four options: playing Human vs. Human,
        Human vs. AI, AI vs. AI, or exiting the game.
        """
        while True:
            # Print the main menu options
            print("Welcome to Zero Point One! :)")
            print("1. Human vs. Human")
            print("2. Human vs. AI")
            print("3. AI vs. AI")
            print("4. Exit")

            # Get the user's choice
            choice = input("Enter your choice: ")

            # Handle the user's choice
            if choice == '1':
                # Start a new game with two human players
                game = ZeroPointOneGame('HvH')
                game.game_loop()
            elif choice == '2':
                # Start a new game with a human player against the AI
                game = ZeroPointOneGame('HvAI')
                game.game_loop()
            elif choice == '3':
                # Start a new game with two AI players
                game = ZeroPointOneGame('AIvAI')
                game.game_loop()
            elif choice == '4':
                # Exit the game loop
                print("Exiting the game.")
                break
            else:
                # Handle invalid input
                print("Invalid choice, please try again.")

# Check if the script is run directly (and not imported)
if __name__ == "__main__":
    # If this script is run as the main program, call the main_menu function
    main_menu()
