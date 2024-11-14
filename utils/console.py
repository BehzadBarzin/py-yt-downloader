import os
from simple_chalk import chalk

terminal_width = os.get_terminal_size().columns
# ------------------------------------------------------------------------------
def clear_console():
    os.system("cls" if os.name == "nt" else "clear")
    
# ------------------------------------------------------------------------------
def print_separator():
    print('-' * terminal_width)

# ------------------------------------------------------------------------------
# Print with chalk
def print_success(message):
    print(chalk.green.bold(message))

def print_error(message):
    print(chalk.red.bold(message))

def print_info(message):
    print(chalk.blue.bold(message))