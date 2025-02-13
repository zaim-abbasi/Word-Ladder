from game import WordLadderGame
import os

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_game_state(game: WordLadderGame):
    """Display the current game state."""
    print("\n" + "="*50)
    print(f"Mode: {game.difficulty.capitalize()}")
    if game.difficulty == "challenge":
        print(f"Banned words: {', '.join(game.banned_words)}")
    print(f"Current Word: {game.current_word}")
    print(f"Target Word:  {game.target_word}")
    print(f"Moves Made:   {game.get_current_moves()}")
    if game.best_path:
        print(f"Minimum Possible Moves: {game.get_minimum_moves()}")
    print("="*50)
    print("\nYour word chain:", " -> ".join(game.moves))
    print("\nCommands:")
    print("- Enter a word to make a move")
    print("- 'hint' to get an AI-powered hint")
    print("- 'solution' to see the optimal solution")
    print("- 'mode' to change difficulty")
    print("- 'new' to start a new game")
    print("- 'quit' to exit")

def select_difficulty() -> str:
    """Let the user select game difficulty."""
    print("\nSelect difficulty level:")
    print("1. Beginner (Simple word transformations)")
    print("2. Advanced (Longer word chains)")
    print("3. Challenge (Banned words and restrictions)")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            return "beginner"
        elif choice == "2":
            return "advanced"
        elif choice == "3":
            return "challenge"
        print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    game = WordLadderGame()
    print("Welcome to Word Ladder Adventure Game!")
    print("Loading dictionary...")
    game.initialize_game('dictionary/words.txt')
    print("Dictionary loaded!")
    
    # Set initial difficulty
    difficulty = select_difficulty()
    game.set_difficulty(difficulty)

    while True:
        if not game.current_word:
            print("\nEnter two words to start a new game.")
            start_word = input("Start word: ").strip().lower()
            target_word = input("Target word: ").strip().lower()
            
            if game.start_new_game(start_word, target_word):
                clear_screen()
                print(f"\nGame started! Transform '{start_word}' into '{target_word}'")
                print("Change one letter at a time to create valid words.")
            else:
                print("\nError: Both words must exist in the dictionary and not be banned!")
                continue
        
        display_game_state(game)
        
        command = input("\nEnter your move: ").strip().lower()
        
        if command == 'quit':
            print("\nThanks for playing!")
            break
        elif command == 'new':
            game.current_word = None
            continue
        elif command == 'mode':
            difficulty = select_difficulty()
            game.set_difficulty(difficulty)
            continue
        elif command == 'hint':
            hint_word, hint_message = game.get_hint()
            if hint_word:
                print(f"\n{hint_message}")
            else:
                print("\nNo hint available!")
            continue
        elif command == 'solution':
            if game.best_path:
                print("\nOptimal solution:", " -> ".join(game.best_path))
            else:
                print("\nNo solution exists!")
            continue
        
        # Handle word moves
        if game.make_move(command):
            clear_screen()
            if game.is_solved():
                print("\n🎉 Congratulations! You've solved the puzzle! 🎉")
                print(f"You used {game.get_current_moves()} moves.")
                print(f"Minimum possible moves: {game.get_minimum_moves()}")
                print(f"Score: {game.score} points")
                input("\nPress Enter to start a new game...")
                game.current_word = None
        else:
            print("\nInvalid move! The word must:")
            print("1. Exist in the dictionary")
            print("2. Not be a banned word (in Challenge mode)")
            print("3. Differ by exactly one letter from the current word")

if __name__ == "__main__":
    main()