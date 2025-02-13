import os
import platform
from game import WordLadderGame

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('clear')

def select_difficulty() -> str:
    """Let the user select the game difficulty."""
    print("\nSelect difficulty level:")
    print("1. Beginner (Simple word transformations)")
    print("2. Advanced (Complex transformations)")
    print("3. Challenge (With banned words)")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            return "beginner"
        elif choice == "2":
            return "advanced"
        elif choice == "3":
            return "challenge"
        print("Invalid choice. Please enter 1, 2, or 3.")

def display_algorithm_comparison(game: WordLadderGame):
    """Display comparison of different algorithm results."""
    if not game.algorithm_stats:
        return
    
    print("\nAlgorithm Comparison:")
    print("-" * 60)
    for algo, stats in game.algorithm_stats.items():
        print(f"{algo}:")
        print(f"  Path length: {stats['length']}")
        print(f"  Path: {' -> '.join(stats['path'])}")
        print("  Costs:")
        print(f"    g(n) (path cost): {stats['costs']['g_cost']}")
        print(f"    h(n) (heuristic): {stats['costs']['h_cost']}")
        print(f"    f(n) (total): {stats['costs']['f_cost']}")
    print("-" * 60)

def select_algorithm() -> str:
    """Let the user select the search algorithm."""
    print("\nSelect search algorithm:")
    print("1. BFS (Breadth-First Search)")
    print("2. UCS (Uniform Cost Search)")
    print("3. A* (A-Star Search)")
    
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice == "1":
            return "BFS"
        elif choice == "2":
            return "UCS"
        elif choice == "3":
            return "A*"
        print("Invalid choice. Please enter 1, 2, or 3.")

def display_game_state(game: WordLadderGame):
    """Display the current game state."""
    print("\n" + "="*50)
    print(f"Mode: {game.difficulty.capitalize()}")
    print(f"Current Algorithm: {game.selected_algorithm}")
    if game.difficulty == "challenge":
        print(f"Banned words: {', '.join(game.banned_words)}")
    
    print(f"\nStart word: {game.moves[0]}")
    print(f"Target word: {game.target_word}")
    print(f"Current word: {game.current_word}")
    print(f"Moves made: {len(game.moves) - 1}")
    print(f"Moves remaining: {game.get_remaining_moves()}")
    
    if game.moves:
        print("\nMove history:", " -> ".join(game.moves))
    
    print("\nCommands:")
    print("- Enter a word to make a move")
    print("- 'hint' to get an AI-powered hint")
    print("- 'algo' to change search algorithm")
    print("- 'compare' to see algorithm comparisons")
    print("- 'solution' to see the optimal solution")
    print("- 'mode' to change difficulty")
    print("- 'new' to start a new game")
    print("- 'quit' to exit")

def display_welcome_message():
    """Display the welcome message and game instructions."""
    print("\n" + "="*50)
    print("Welcome to Word Ladder Adventure!")
    print("="*50)
    print("\nGame Rules:")
    print("1. Transform the start word into the target word")
    print("2. Change only one letter at a time")
    print("3. Each intermediate word must be valid")
    print("4. Complete the transformation in as few moves as possible")
    print("\nFeatures:")
    print("- Multiple difficulty levels")
    print("- AI-powered hints using different search algorithms")
    print("- Algorithm comparison and analysis")
    print("- Score tracking based on performance")
    print("\nLet's begin!")

def main():
    """Main game loop."""
    # Initialize game
    game = WordLadderGame()
    game.initialize_game("dictionary/words.txt")
    
    # Display welcome message
    clear_screen()
    display_welcome_message()
    
    # Main game loop
    while True:
        if not game.current_word:
            print("\nEnter two words to start a new game.")
            start_word = input("Start word: ").strip().lower()
            target_word = input("Target word: ").strip().lower()
            
            if game.start_new_game(start_word, target_word):
                clear_screen()
                print(f"\nGame started! Transform '{start_word}' into '{target_word}'")
                print("Change one letter at a time to create valid words.")
                print(f"You have {game.get_remaining_moves()} moves available.")
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
        elif command == 'algo':
            algorithm = select_algorithm()
            game.set_algorithm(algorithm)
            continue
        elif command == 'hint':
            hint_word, hint_message = game.get_hint()
            if hint_word:
                print(f"\n{hint_message}")
            else:
                print("\nNo hint available!")
            continue
        elif command == 'compare':
            display_algorithm_comparison(game)
            continue
        elif command == 'solution':
            if game.best_path:
                print("\nOptimal solution:", " -> ".join(game.best_path))
                print(f"\nUsing {game.selected_algorithm} algorithm:")
                costs = game.algorithm_stats[game.selected_algorithm]['costs']
                print(f"Total cost (f(n)): {costs['f_cost']}")
                print(f"Path cost (g(n)): {costs['g_cost']}")
                print(f"Heuristic estimate (h(n)): {costs['h_cost']}")
            else:
                print("\nNo solution exists!")
            continue
        
        # Handle word moves
        if game.is_valid_move(command):
            game.make_move(command)
            if game.is_solved():
                print(f"\nCongratulations! You solved the puzzle in {len(game.moves)-1} moves!")
                print(f"Your score: {game.score}")
                game.current_word = None
            elif game.get_remaining_moves() <= 0:
                print("\nGame Over! You've run out of moves.")
                print(f"The optimal solution was: {' -> '.join(game.best_path)}")
                game.current_word = None
        else:
            print("\nInvalid move! The word must:")
            print("1. Exist in the dictionary")
            print("2. Differ by exactly one letter")
            print("3. Not be a banned word")
            print("4. Be within the move limit")

if __name__ == "__main__":
    main()