from src import main as main_calculator
from utils import main as main_add_block

from colorama import Fore

OUT_TITLE = Fore.LIGHTBLUE_EX + '[Out]: ' + Fore.LIGHTMAGENTA_EX
IN_TITLE = Fore.LIGHTGREEN_EX + '[In]:  ' + Fore.LIGHTGREEN_EX
ERROR_TITLE = Fore.RED + '[ERROR]: '

requires_tips = lambda: print(f'\n{OUT_TITLE}Enter "q" / "quit" to quit.'
                              f'\n{OUT_TITLE}Enter "-add" to switch to Add mode.'
                              f'\n{OUT_TITLE}Example: 红石粉 64 4'
                              '<Use "|" to split different block>')
add_block_tips = lambda: print(f'\n{OUT_TITLE}Enter "q" / "quit" to quit.'
                               f'\n{OUT_TITLE}Example: oak_wood-({{"outputQty": 3, "橡木原木": 4}},)-橡木-建筑方块. '
                               '<Use "|" to split different block>')


def main():
    while True:
        requires_tips()
        block_requires = input(
                f'{IN_TITLE}The material that you required: ')
        match block_requires:
            case 'q' | 'quit':
                quit(0)
            case '-add':
                while True:
                    add_block_tips()
                    block_info = input(f'{IN_TITLE}The information of block: ')
                    if block_info in ['q', 'quit']:
                        quit(0)
                    try:
                        main_add_block(block_info)
                    except TypeError:
                        print(f'{ERROR_TITLE}Missing relevant parameters.')
            case _:
                try:
                    main_calculator(block_requires)
                except TypeError:
                    print(f'{ERROR_TITLE}Missing relevant parameters.')


if __name__ == '__main__':
    main()
