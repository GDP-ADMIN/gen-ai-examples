"""UI components for the custom pipeline demo."""

def print_colored(text: str, color: str = "default") -> None:
    """Print colored text to the console."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "default": "\033[0m",
    }
    end_color = "\033[0m"

    color_code = colors.get(color.lower(), colors["default"])
    print(f"{color_code}{text}{end_color}")

def display_menu(options: list[str], title: str) -> None:
    """Display a menu with options."""
    print_colored(f"\n{title}", "cyan")
    print_colored("=" * len(title), "cyan")

    for i, option in enumerate(options, 1):
        print(f"  {i}. {option}")

    print_colored("\nEnter 'q' to quit", "yellow")

def get_user_choice(options: list[str], prompt: str) -> str | None:
    """Get user choice from a list of options."""
    while True:
        try:
            choice = input(f"{prompt}: ").strip().lower()

            if choice == "q":
                print_colored("\nExiting program.", "yellow")
                return None

            idx = int(choice) - 1
            if 0 <= idx < len(options):
                return options[idx]
            else:
                print_colored(
                    f"Please enter a number between 1 and {len(options)}", "red"
                )
        except ValueError:
            print_colored("Please enter a valid number or 'q' to quit", "red")
