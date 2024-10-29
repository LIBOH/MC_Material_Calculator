from src import main as main_calculator
from utils import main as main_add_block

from colorama import Fore

OUT_TITLE = Fore.LIGHTBLUE_EX + '[Out]: ' + Fore.LIGHTMAGENTA_EX
IN_TITLE = Fore.LIGHTGREEN_EX + '[In]:  ' + Fore.LIGHTGREEN_EX
ERROR_TITLE = Fore.RED + '[ERROR]: '


def _requires_tips():
    print(f'\n{OUT_TITLE}Enter "q" / "quit" to quit.'
          f'\n{OUT_TITLE}Enter "-a" will switch to Add mode.'
          f'\n{OUT_TITLE}Example: 红石粉 64 4 | ... '
          '<Use "|" to split different block>')


def _add_block_tips():
    print(f'\n{OUT_TITLE}Enter "q" / "quit" to quit.'
          f'\n{OUT_TITLE}Enter "-c" will switch to Check mode.'
          f'\n{OUT_TITLE}Example: oak_wood-({{"outputQty": 3, "橡木原木": 4}},)-橡木-建筑方块 | ... '
          '<Use "|" to split different block>')


def main():
    while True:
        _requires_tips()
        block_requires = input(
                f'{IN_TITLE}The material that you required: ')
        match block_requires:
            case 'q' | 'quit':
                quit(0)
            case '-a':
                while True:
                    _add_block_tips()
                    block_info = input(f'{IN_TITLE}The information of block: ')
                    if block_info in ['q', 'quit']:
                        quit(0)
                    elif block_info == '-c':
                        break
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
