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
    if platform.system().lower() == "windows":
        os.system('cls')
    else:
        os.system('clear')

def create_neon_text(text: str, color: str = "bright_yellow") -> str:
    return f"[{color}]≪ {text} ≫[/]"

def create_title(text: str) -> Panel:
    return Panel(
        Text(text, style="bold black on bright_yellow", justify="center"),
        box=ASCII_DOUBLE_HEAD,
        border_style="bright_yellow",
        padding=(1, 4)
    )

def create_info_panel(content: str, title: str = "") -> Panel:
    return Panel(
        Align.center(Text.from_markup(content)),
        title=title,
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        padding=(1, 2)
    )

def create_retro_box(text: str, style: str = "black on bright_yellow") -> str:
    return f"[{style}]{text}[/]"

def create_separator() -> str:
    return "\n[bright_yellow]" + "═" * console.width + "[/]\n"

def select_difficulty() -> str:
    console.print(create_title("⚡ SELECT YOUR CHALLENGE ⚡"))
    
    table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    table.add_row(
        create_retro_box(" 1 ", "black on green"),
        "[bright_green]BEGINNER[/]",
        "[dim]Simple word transformations for newcomers[/]"
    )
    table.add_row(
        create_retro_box(" 2 ", "black on yellow"),
        "[bright_yellow]ADVANCED[/]",
        "[dim]Complex transformations for word masters[/]"
    )
    table.add_row(
        create_retro_box(" 3 ", "black on red"),
        "[bright_red]CHALLENGE[/]",
        "[dim]Expert mode with forbidden words[/]"
    )
    
    console.print(Panel(
        table,
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        title=create_neon_text("DIFFICULTY SELECT")
    ))
    
    while True:
        choice = Prompt.ask(
            "\n" + create_neon_text("SELECT YOUR DESTINY"),
            choices=["1", "2", "3"],
            show_choices=False
        )
        if choice == "1":
            return "beginner"
        elif choice == "2":
            return "advanced"
        elif choice == "3":
            return "challenge"

def display_algorithm_comparison(game: WordLadderGame):
    if not game.algorithm_stats:
        console.print(create_info_panel("No algorithm data available yet."))
        return
    
    table = Table(
        title=create_neon_text("ALGORITHM BATTLE"),
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
        table,
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        title=create_neon_text("PERFORMANCE ANALYSIS")
    ))

def select_algorithm() -> str:
    console.print(create_title("⚡ SELECT YOUR ALGORITHM ⚡"))
    
    table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    table.add_row(
        create_retro_box(" 1 ", "black on cyan"),
        "[bright_cyan]BFS[/]",
        "[dim]Breadth-First Search - Explores level by level[/]"
    )
    table.add_row(
        create_retro_box(" 2 ", "black on magenta"),
        "[bright_magenta]UCS[/]",
        "[dim]Uniform Cost Search - Finds shortest paths[/]"
    )
    table.add_row(
        create_retro_box(" 3 ", "black on green"),
        "[bright_green]A*[/]",
        "[dim]A-Star Search - Smart pathfinding[/]"
    )
    
    console.print(Panel(
        table,
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD,
        title=create_neon_text("ALGORITHM SELECT")
    ))
    
    while True:
        choice = Prompt.ask(
            "\n" + create_neon_text("CHOOSE YOUR WEAPON"),
            choices=["1", "2", "3"],
            show_choices=False
        )
        if choice == "1":
            return "BFS"
        elif choice == "2":
            return "UCS"
        elif choice == "3":
            return "A*"

def display_game_state(game: WordLadderGame):
    stats_table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    stats_table.add_row(
        create_retro_box(" MODE ", "black on green"),
        f"[bright_green]{game.difficulty.upper()}[/]",
        create_retro_box(" ALGO ", "black on cyan"),
        f"[bright_cyan]{game.selected_algorithm}[/]"
    )
    
    if game.difficulty == "challenge":
        banned_words = " ⚠ ".join(game.banned_words)
        stats_table.add_row(
            create_retro_box(" BANNED ", "black on red"),
            f"[bright_red]{banned_words}[/]", "", ""
        )
    
    console.print(Panel(
        stats_table,
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
        progress_table,
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
        commands_panel,
        title=create_neon_text("COMMANDS"),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD
    ))

def display_welcome_message():
    console.print(create_title("⚡ WELCOME TO THE WORD LADDER ARCADE ⚡"))
    
    rules_table = Table(show_header=False, box=ASCII_DOUBLE_HEAD, border_style="bright_yellow")
    rules_table.add_row(
        create_retro_box(" 1 ", "black on green"),
        "[bright_white]Transform START word into TARGET word[/]"
    )
    rules_table.add_row(
        create_retro_box(" 2 ", "black on yellow"),
        "[bright_white]Change only ONE letter at a time[/]"
    )
    rules_table.add_row(
        create_retro_box(" 3 ", "black on cyan"),
        "[bright_white]Each word must be valid[/]"
    )
    rules_table.add_row(
        create_retro_box(" 4 ", "black on magenta"),
        "[bright_white]Complete in minimum moves[/]"
    )
    
    console.print(Panel(
        rules_table,
        title=create_neon_text("GAME RULES"),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD
    ))

def display_solution(game: WordLadderGame):
    if not game.best_path:
        console.print(create_info_panel(
            "[bright_red]No solution exists![/]",
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
        solution_table,
        title=create_neon_text(f"{game.selected_algorithm} SOLUTION"),
        border_style="bright_yellow",
        box=ASCII_DOUBLE_HEAD
    ))

def main():
    game = WordLadderGame()
    game.initialize_game("dictionary/words.txt")
    
    clear_screen()
    display_welcome_message()
    
    difficulty = select_difficulty()
    game.set_difficulty(difficulty)
    
    while True:
        if not game.current_word:
            game.start_new_game_for_difficulty()
            clear_screen()
            console.print(create_info_panel(
                f"Transform [bright_green]{game.current_word}[/] into [bright_red]{game.target_word}[/]",
                create_neon_text("NEW PUZZLE")
            ))
        
        display_game_state(game)
        
        command = Prompt.ask("\n" + create_neon_text("YOUR MOVE")).strip().lower()
        
        if command == 'quit':
            console.print(create_info_panel(
                "[bright_yellow]Thanks for playing! See you next time![/]",
                create_neon_text("GAME OVER")
            ))
            break
        elif command == 'new':
            game.current_word = None
            clear_screen()
            continue
        elif command == 'mode':
            difficulty = select_difficulty()
            game.set_difficulty(difficulty)
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
                console.print(create_info_panel(
                    "[bright_red]No hint available![/]",
                    create_neon_text("ERROR")
                ))
            continue
        elif command == 'compare':
            display_algorithm_comparison(game)
            continue
        elif command == 'solution':
            display_solution(game)
            continue
        
        if not game.word_graph.word_exists(command):
            console.print(create_info_panel(
                "[bright_red]Word not found in dictionary![/]",
                create_neon_text("ERROR")
            ))
            continue
            
        if game.is_valid_move(command):
            game.make_move(command)
            clear_screen()
            if game.is_solved():
                console.print(create_info_panel(
                    f"[bright_green]★ CONGRATULATIONS! ★[/]\n"
                    f"Puzzle solved in [bright_yellow]{len(game.moves)-1}[/] moves!\n"
                    f"Score [bright_cyan]{game.score}[/]",
                    create_neon_text("VICTORY")
                ))
                game.current_word = None
            elif game.get_remaining_moves() <= 0:
                console.print(create_info_panel(
                    "[bright_red]★ GAME OVER! ★[/] You've run out of moves.\n"
                    f"Solution [bright_cyan]{' ⟹ '.join(game.best_path)}[/]",
                    create_neon_text("GAME OVER")
                ))
                game.current_word = None
        else:
            console.print(create_info_panel(
                "[bright_red]Invalid move![/]\n\n"
                "The word must\n"
                f"{create_retro_box(' 1 ', 'black on green')} Exist in dictionary\n"
                f"{create_retro_box(' 2 ', 'black on yellow')} Differ by one letter\n"
                f"{create_retro_box(' 3 ', 'black on cyan')} Not be banned\n"
                f"{create_retro_box(' 4 ', 'black on magenta')} Be within move limit",
                create_neon_text("ERROR")
            ))

if __name__ == "__main__":
    main()