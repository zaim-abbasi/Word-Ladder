import os
import platform
from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.style import Style
from rich.align import Align
from rich.box import DOUBLE, ROUNDED, HEAVY, ASCII_DOUBLE_HEAD
from rich.columns import Columns
from game import WordLadderGame

console = Console()

def clear_screen():
    # clear screen ke liye
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('clear')

def create_neon_text(text: str, color: str = "bright_yellow") -> str:
    # fancy text 
    return f"[{color}]≪ {text} ≫[/]"

def create_title(text: str) -> Panel:
    # game ka title box 
    return Panel(
        Align.center(Text(text, style="bold black on bright_yellow")),
        box=ASCII_DOUBLE_HEAD,
        border_style="bright_yellow",
        padding=(1, 4)
    )

def create_info_panel(content: str, title: str = "") -> Panel:
    # information dikhane ke liye
    return Panel(
        Align.center(Text.from_markup(content)),
        title=title,
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        padding=(1, 2)
    )

def create_retro_box(text: str, style: str = "black on bright_yellow") -> str:
    # retro theme
    return f"[{style}]{text}[/]"

def create_separator() -> str:
    # line draw 
    return "\n[bright_yellow]" + "═" * console.width + "[/]\n"

def display_game_state(game: WordLadderGame):
    # game ki current position dikhane ke liye
    stats_table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    stats_table.add_row(
        create_retro_box(" MODE ", "black on green"),
        f"[bright_green]{game.difficulty.upper()}[/]",
        create_retro_box(" ALGO ", "black on cyan"),
        f"[bright_cyan]{game.selected_algorithm}[/]"
    )
    
    if game.difficulty == "challenge" and game.banned_words:
        banned_words = " ⚠ ".join(sorted(game.banned_words))
        banned_words = "⚠ " + banned_words
        stats_table.add_row(
            create_retro_box(" BANNED ", "black on red"),
            f"[bright_red]{banned_words}[/]", "", ""
        )
    
    console.print(Panel(
        Align.center(stats_table),
        title=create_neon_text("GAME STATS"),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD
    ))
    
    progress_table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    progress_table.add_row(
        create_retro_box(" START ", "black on green"),
        f"[bright_green]{game.moves[0]}[/]",
        create_retro_box(" TARGET ", "black on red"),
        f"[bright_red]{game.target_word}[/]"
    )
    progress_table.add_row(
        create_retro_box(" CURRENT ", "black on cyan"),
        f"[bright_cyan]{game.current_word}[/]",
        create_retro_box(" MOVES ", "black on magenta"),
        f"[bright_magenta]{len(game.moves) - 1}/{game.move_limit}[/]"
    )
    
    console.print(Panel(
        Align.center(progress_table),
        title=create_neon_text("PROGRESS"),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD
    ))
    
    if game.moves:
        moves_text = " ⟹ ".join(
            f"[bright_cyan]{word}[/]" for word in game.moves
        )
        console.print(Panel(
            Align.center(Text.from_markup(moves_text)),
            title=create_neon_text("HISTORY"),
            border_style="bright_yellow",
            box=ASCII_DOUBLE_HEAD
        ))
    
    commands_left = Table(show_header=False, box=None, padding=(0, 1))
    commands_right = Table(show_header=False, box=None, padding=(0, 1))
    
    commands_left.add_row(create_retro_box(" WORD ", "black on green"), "[bright_white]Enter a word[/]")
    commands_left.add_row(create_retro_box(" hint ", "black on yellow"), "[bright_white]Get AI hint[/]")
    commands_left.add_row(create_retro_box(" algo ", "black on cyan"), "[bright_white]Change algorithm[/]")
    commands_left.add_row(create_retro_box(" new ", "black on magenta"), "[bright_white]New game[/]")
    
    commands_right.add_row(create_retro_box(" compare ", "black on blue"), "[bright_white]Compare algorithms[/]")
    commands_right.add_row(create_retro_box(" solution ", "black on green"), "[bright_white]See solution[/]")
    commands_right.add_row(create_retro_box(" mode ", "black on yellow"), "[bright_white]Change difficulty[/]")
    commands_right.add_row(create_retro_box(" quit ", "black on red"), "[bright_white]Exit game[/]")
    
    commands_panel = Columns([commands_left, commands_right], equal=True, expand=True)
    
    console.print(Panel(
        Align.center(commands_panel),
        title=create_neon_text("COMMANDS"),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD
    ))

def select_difficulty() -> str:
    # difficulty choose karne ke liye menu
    console.print(create_title("⚡ SELECT DIFFICULTY LEVEL ⚡"))
    
    table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    table.add_row(
        create_retro_box(" 1 ", "black on green"),
        "[bright_green]BEGINNER[/]",
        "[dim]Easy mode for new players[/]"
    )
    table.add_row(
        create_retro_box(" 2 ", "black on yellow"),
        "[bright_yellow]ADVANCED[/]",
        "[dim]Intermediate challenge[/]"
    )
    table.add_row(
        create_retro_box(" 3 ", "black on red"),
        "[bright_red]CHALLENGE[/]",
        "[dim]Expert mode with restrictions[/]"
    )
    
    console.print(Panel(
        Align.center(table),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        title=create_neon_text("SELECT MODE")
    ))
    
    while True:
        try:
            choice = Prompt.ask(
                "\n" + create_neon_text("Select your level"),
                choices=["1", "2", "3"],
                show_choices=False
            )
            if choice == "1":
                return "beginner"
            elif choice == "2":
                return "advanced"
            elif choice == "3":
                return "challenge"
        except KeyboardInterrupt:
            return "beginner"

def display_algorithm_comparison(game: WordLadderGame):
    # algorithms ka comparison
    if not game.algorithm_stats:
        console.print(create_info_panel(
            "No algorithm data available yet.",
            create_neon_text("INFO")
        ))
        return
    
    table = Table(
        title=create_neon_text("ALGORITHM COMPARISON"),
        show_header=True,
        header_style="bold bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        border_style="bright_yellow"
    )
    table.add_column("ALGORITHM", style="bright_white")
    table.add_column("MOVES", justify="center")
    table.add_column("PATH", style="bright_green")
    table.add_column("STATS", style="bright_cyan")
    
    for algo, stats in game.algorithm_stats.items():
        costs = stats['costs']
        table.add_row(
            create_retro_box(f" {algo} "),
            str(stats['length']),
            " ⟹ ".join(stats['path']),
            f"Cost {costs['f_cost']}\nPath {costs['g_cost']}\nHeur {costs['h_cost']}"
        )
    
    console.print(Panel(
        Align.center(table),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        title=create_neon_text("PERFORMANCE ANALYSIS")
    ))

def select_algorithm() -> str:
    # algorithm choose menu
    console.print(create_title("⚡ SELECT SEARCH ALGORITHM ⚡"))
    
    table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    table.add_row(
        create_retro_box(" 1 ", "black on cyan"),
        "[bright_cyan]BFS[/]",
        "[dim]Breadth-First Search[/]"
    )
    table.add_row(
        create_retro_box(" 2 ", "black on magenta"),
        "[bright_magenta]UCS[/]",
        "[dim]Uniform Cost Search[/]"
    )
    table.add_row(
        create_retro_box(" 3 ", "black on green"),
        "[bright_green]A*[/]",
        "[dim]A* Search Algorithm[/]"
    )
    
    console.print(Panel(
        Align.center(table),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        title=create_neon_text("ALGORITHM SELECT")
    ))
    
    while True:
        try:
            choice = Prompt.ask(
                "\n" + create_neon_text("Select algorithm"),
                choices=["1", "2", "3"],
                show_choices=False
            )
            if choice == "1":
                return "BFS"
            elif choice == "2":
                return "UCS"
            elif choice == "3":
                return "A*"
        except KeyboardInterrupt:
            return "A*"

def display_welcome_message():
    # welcome screen
    console.print(create_title("⚡ WORD LADDER GAME ⚡"))
    
    rules_table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    rules_table.add_row(
        create_retro_box(" 1 ", "black on green"),
        "[bright_white]Transform start word into target word[/]"
    )
    rules_table.add_row(
        create_retro_box(" 2 ", "black on yellow"),
        "[bright_white]Change only one letter at a time[/]"
    )
    rules_table.add_row(
        create_retro_box(" 3 ", "black on cyan"),
        "[bright_white]All words must be in dictionary[/]"
    )
    rules_table.add_row(
        create_retro_box(" 4 ", "black on magenta"),
        "[bright_white]Complete in minimum moves[/]"
    )
    
    console.print(Panel(
        Align.center(rules_table),
        title=create_neon_text("GAME RULES"),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD
    ))

def display_solution(game: WordLadderGame):
    # solution dikhane ke liye
    if not game.best_path:
        console.print(create_info_panel(
            "No solution available!",
            create_neon_text("SOLUTION")
        ))
        return
    
    solution_table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    solution_table.add_row(
        create_retro_box(" PATH ", "black on cyan"),
        " ⟹ ".join(f"[bright_cyan]{word}[/]" for word in game.best_path)
    )
    
    if game.selected_algorithm in game.algorithm_stats:
        costs = game.algorithm_stats[game.selected_algorithm]['costs']
        solution_table.add_row(
            create_retro_box(" STATS ", "black on magenta"),
            f"[bright_white]Total {costs['f_cost']} | Path {costs['g_cost']} | Heur {costs['h_cost']}[/]"
        )
    
    console.print(Panel(
        Align.center(solution_table),
        title=create_neon_text(f"{game.selected_algorithm} SOLUTION"),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD
    ))

def handle_input_error(error_message: str):
    # error message
    console.print(create_info_panel(
        f"[bright_red]{error_message}[/]",
        create_neon_text("ERROR")
    ))

def main():
    try:
        # game setup
        game = WordLadderGame()
        if not game.initialize_game("dictionary/words.txt"):
            console.print(create_info_panel(
                "Failed to initialize game!",
                create_neon_text("ERROR")
            ))
            return
        
        clear_screen()
        display_welcome_message()
        
        # difficulty set karo
        difficulty = select_difficulty()
        if not game.set_difficulty(difficulty):
            console.print(create_info_panel(
                "Failed to set difficulty!",
                create_neon_text("ERROR")
            ))
            return
        
        # main game loop
        while True:
            try:
                if not game.current_word:
                    if not game.start_new_game_for_difficulty():
                        handle_input_error("Failed to start new game!")
                        continue
                    clear_screen()
                    console.print(create_info_panel(
                        f"Transform [bright_green]{game.current_word}[/] into [bright_red]{game.target_word}[/]",
                        create_neon_text("NEW PUZZLE")
                    ))
                
                display_game_state(game)
                
                try:
                    command = Prompt.ask("\n" + create_neon_text("Your move")).strip().lower()
                except KeyboardInterrupt:
                    command = 'quit'
                
                if command == 'quit':
                    console.print(create_info_panel(
                        "[bright_yellow]Game Over! Thanks for playing![/]",
                        create_neon_text("GAME OVER")
                    ))
                    break
                elif command == 'new':
                    game.current_word = None
                    clear_screen()
                    continue
                elif command == 'mode':
                    difficulty = select_difficulty()
                    if not game.set_difficulty(difficulty):
                        handle_input_error("Failed to change difficulty!")
                    clear_screen()
                    continue
                elif command == 'algo':
                    algorithm = select_algorithm()
                    game.set_algorithm(algorithm)
                    clear_screen()
                    continue
                elif command == 'hint':
                    hint_word, hint_message = game.get_hint()
                    if hint_word:
                        console.print(create_info_panel(hint_message, create_neon_text("AI HINT")))
                    else:
                        handle_input_error(hint_message)
                    continue
                elif command == 'compare':
                    display_algorithm_comparison(game)
                    continue
                elif command == 'solution':
                    display_solution(game)
                    continue
                elif not command:
                    handle_input_error("Please enter a command!")
                    continue
                
                if not game.word_graph.is_valid_word(command):
                    handle_input_error("Word not found in dictionary!")
                    continue
                    
                if game.is_valid_move(command):
                    if not game.make_move(command):
                        handle_input_error("Invalid move!")
                        continue
                    
                    clear_screen()
                    if game.is_solved():
                        console.print(create_info_panel(
                            f"[bright_green]★ CONGRATULATIONS! ★[/]\n"
                            f"Puzzle solved in [bright_yellow]{len(game.moves)-1}[/] moves!\n"
                            f"Score: [bright_cyan]{game.score}[/]",
                            create_neon_text("VICTORY")
                        ))
                        game.current_word = None
                    elif game.get_remaining_moves() <= 0:
                        console.print(create_info_panel(
                            "[bright_red]★ GAME OVER! ★[/] Out of moves.\n"
                            f"Solution was: [bright_cyan]{' ⟹ '.join(game.best_path)}[/]",
                            create_neon_text("GAME OVER")
                        ))
                        game.current_word = None
                else:
                    handle_input_error(
                        "Invalid move!\n\n"
                        "Word Rules:\n"
                        f"{create_retro_box(' 1 ', 'black on green')} Must be in dictionary\n"
                        f"{create_retro_box(' 2 ', 'black on yellow')} Only one letter change\n"
                        f"{create_retro_box(' 3 ', 'black on cyan')} Not in banned list\n"
                        f"{create_retro_box(' 4 ', 'black on magenta')} Within move limit"
                    )
                    
            except Exception as e:
                handle_input_error(f"An error occurred: {str(e)}")
                continue
                
    except KeyboardInterrupt:
        console.print(create_info_panel(
            "[bright_yellow]Game terminated. Goodbye![/]",
            create_neon_text("GOODBYE")
        ))
    except Exception as e:
        console.print(create_info_panel(
            f"[bright_red]Critical error: {str(e)}[/]",
            create_neon_text("ERROR")
        ))

if __name__ == "__main__":
    main()