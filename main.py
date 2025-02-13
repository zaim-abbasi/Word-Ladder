"""
Word Ladder Game Main Module

This module contains the main game loop and user interface for the Word Ladder game.
"""

import os
import platform
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.style import Style
from game import WordLadderGame

# Initialize Rich console
console = Console()

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('clear')

def create_title(text: str) -> Panel:
    """Create a styled title panel."""
    return Panel(
        Text(text, style="bold white on magenta", justify="center"),
        border_style="magenta"
    )

def create_info_panel(content: str, title: str = "") -> Panel:
    """Create an information panel with optional title."""
    return Panel(
        Text.from_markup(content, justify="left"),  # Use from_markup to properly render colors
        title=title,
        border_style="cyan"
    )

def select_difficulty() -> str:
    """
    Let the user select the game difficulty.
    
    Returns:
        str: Selected difficulty level
    """
    console.print(create_title("Select Difficulty Level"))
    
    table = Table(show_header=False, box=None)
    table.add_row("[white on blue]1[/]", "Beginner - Simple word transformations")
    table.add_row("[white on yellow]2[/]", "Advanced - Complex transformations")
    table.add_row("[white on red]3[/]", "Challenge - With banned words")
    
    console.print(Panel(table, border_style="blue"))
    
    while True:
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"])
        if choice == "1":
            return "beginner"
        elif choice == "2":
            return "advanced"
        elif choice == "3":
            return "challenge"

def display_algorithm_comparison(game: WordLadderGame):
    """Display comparison of different algorithm results."""
    if not game.algorithm_stats:
        console.print(create_info_panel("No algorithm statistics available yet."))
        return
    
    table = Table(title="Algorithm Comparison", show_header=True, header_style="bold cyan")
    table.add_column("Algorithm", style="white on blue")
    table.add_column("Path Length")
    table.add_column("Path")
    table.add_column("Costs")
    
    for algo, stats in game.algorithm_stats.items():
        costs = stats['costs']
        table.add_row(
            algo,
            str(stats['length']),
            " → ".join(stats['path']),
            f"g(n): {costs['g_cost']}\nh(n): {costs['h_cost']}\nf(n): {costs['f_cost']}"
        )
    
    console.print(Panel(table, border_style="blue"))

def select_algorithm() -> str:
    """
    Let the user select the search algorithm.
    
    Returns:
        str: Selected algorithm name
    """
    console.print(create_title("Select Search Algorithm"))
    
    table = Table(show_header=False, box=None)
    table.add_row("[white on blue]1[/]", "BFS - Breadth-First Search")
    table.add_row("[white on green]2[/]", "UCS - Uniform Cost Search")
    table.add_row("[white on yellow]3[/]", "A* - A-Star Search")
    
    console.print(Panel(table, border_style="blue"))
    
    while True:
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3"])
        if choice == "1":
            return "BFS"
        elif choice == "2":
            return "UCS"
        elif choice == "3":
            return "A*"

def display_game_state(game: WordLadderGame):
    """Display the current game state."""
    # Game info panel
    info_content = [
        f"[white on blue] Mode [/] {game.difficulty.capitalize()}",
        f"[white on cyan] Algorithm [/] {game.selected_algorithm}",
    ]
    
    if game.difficulty == "challenge":
        info_content.append(f"[white on red] Banned Words [/] {', '.join(game.banned_words)}")
    
    # Game progress panel
    progress_content = [
        f"[black on green] Start [/] {game.moves[0]}",
        f"[black on red] Target [/] {game.target_word}",
        f"[black on yellow] Current [/] {game.current_word}",
        f"[white on blue] Moves Made [/] {len(game.moves) - 1}",
        f"[white on magenta] Moves Left [/] {game.get_remaining_moves()}"
    ]
    
    # Move history
    if game.moves:
        moves_text = " → ".join(f"[black on cyan]{word}[/]" for word in game.moves)
        progress_content.append(f"\n[white on blue] History [/] {moves_text}")
    
    # Commands panel
    commands = [
        "[white on green] WORD [/] Enter a word to make a move",
        "[white on yellow] hint [/] Get AI-powered hint",
        "[white on blue] algo [/] Change algorithm",
        "[white on cyan] compare [/] View algorithm comparison",
        "[white on magenta] solution [/] See optimal solution",
        "[white on red] mode [/] Change difficulty",
        "[black on white] new [/] Start a new game",
        "[white on red] quit [/] Exit game"
    ]
    
    # Display panels
    console.print(create_info_panel("\n".join(info_content), "Game Info"))
    console.print(create_info_panel("\n".join(progress_content), "Game Progress"))
    console.print(create_info_panel("\n".join(commands), "Available Commands"))

def display_welcome_message():
    """Display the welcome message and game instructions."""
    title = create_title("Welcome to Word Ladder Adventure!")
    
    rules = [
        "[white on blue] 1 [/] Transform the start word into the target word",
        "[white on blue] 2 [/] Change only one letter at a time",
        "[white on blue] 3 [/] Each intermediate word must be valid",
        "[white on blue] 4 [/] Complete the transformation in as few moves as possible"
    ]
    
    features = [
        "[white on green] ★ [/] Multiple difficulty levels",
        "[white on yellow] ★ [/] AI-powered hints using different search algorithms",
        "[white on cyan] ★ [/] Algorithm comparison and analysis",
        "[white on magenta] ★ [/] Score tracking based on performance"
    ]
    
    console.print(title)
    console.print(create_info_panel("\n".join(rules), "Game Rules"))
    console.print(create_info_panel("\n".join(features), "Features"))

def display_solution(game: WordLadderGame):
    """Display the optimal solution and algorithm statistics."""
    if not game.best_path:
        console.print(create_info_panel("[white on red] No solution exists! [/]", "Solution"))
        return
    
    solution_content = [
        f"[white on green] Optimal Solution [/] {' → '.join(f'[black on cyan]{word}[/]' for word in game.best_path)}"
    ]
    
    if game.selected_algorithm in game.algorithm_stats:
        costs = game.algorithm_stats[game.selected_algorithm]['costs']
        solution_content.extend([
            f"\n[white on blue] {game.selected_algorithm} Algorithm Stats [/]",
            f"[white on cyan] Total Cost [/] {costs['f_cost']}",
            f"[white on yellow] Path Cost [/] {costs['g_cost']}",
            f"[white on magenta] Heuristic [/] {costs['h_cost']}"
        ])
    
    console.print(create_info_panel("\n".join(solution_content), "Solution"))

def main():
    """Main game loop."""
    game = WordLadderGame()
    game.initialize_game("dictionary/words.txt")
    
    clear_screen()
    display_welcome_message()
    
    while True:
        if not game.current_word:
            console.print("\n[white on blue] New Game [/] Enter two words to start")
            start_word = Prompt.ask("Start word").strip().lower()
            target_word = Prompt.ask("Target word").strip().lower()
            
            if game.start_new_game(start_word, target_word):
                clear_screen()
                console.print(f"\n[white on green] Game Started! [/] Transform '{start_word}' into '{target_word}'")
                console.print(f"[white on blue] Moves Available [/] {game.get_remaining_moves()}")
            else:
                console.print("\n[white on red] Error [/] Both words must exist in the dictionary and not be banned!")
                continue
        
        display_game_state(game)
        
        command = Prompt.ask("\nEnter your move").strip().lower()
        
        if command == 'quit':
            console.print("\n[white on green] Thanks for playing! [/]")
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
                console.print(create_info_panel(hint_message, "Hint"))
            else:
                console.print("\n[white on red] No hint available! [/]")
            continue
        elif command == 'compare':
            display_algorithm_comparison(game)
            continue
        elif command == 'solution':
            display_solution(game)
            continue
        
        if game.is_valid_move(command):
            game.make_move(command)
            if game.is_solved():
                console.print(f"\n[white on green] Congratulations! [/] You solved the puzzle in {len(game.moves)-1} moves!")
                console.print(f"[white on cyan] Score [/] {game.score}")
                game.current_word = None
            elif game.get_remaining_moves() <= 0:
                console.print("\n[white on red] Game Over! [/] You've run out of moves.")
                if game.best_path:
                    console.print(f"[white on blue] Optimal Solution [/] {' → '.join(game.best_path)}")
                game.current_word = None
        else:
            console.print(create_info_panel(
                "[white on red] Invalid Move [/] The word must:\n"
                "[white on blue] 1 [/] Exist in the dictionary\n"
                "[white on blue] 2 [/] Differ by exactly one letter\n"
                "[white on blue] 3 [/] Not be a banned word\n"
                "[white on blue] 4 [/] Be within the move limit",
                "Invalid Move"
            ))

if __name__ == "__main__":
    main()