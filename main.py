from src import main
from colorama import Fore

if __name__ == '__main__':
    while True:
        block_requires = input(f'{Fore.GREEN}The material than you required (Enter q to quit): ')
        if block_requires in ['q', 'quit']:
            quit(0)
        main(block_requires)
