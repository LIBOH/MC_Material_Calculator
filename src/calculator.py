from copy import deepcopy
from decimal import Decimal, ROUND_UP, getcontext
from typing import Iterable, Generator
from collections import defaultdict, namedtuple

from colorama import Fore, Style

try:
    from .block import Block, IGNOR_BLOCKS, get_block, get_tag_by_description
except ImportError:
    from block import Block, IGNOR_BLOCKS, get_block, get_tag_by_description

getcontext().rounding = ROUND_UP

INITIAL_COLOR = Fore.BLUE
INNER_COLOR = Fore.YELLOW
SPACE_COUNT = 35

iterate_count_map = defaultdict(int)
same_material = set()


def _convert_str_quantity_to_int(quantity: str) -> int:
    if quantity.isdigit():
        return int(quantity)


def _is_ignore_by_description(block_desc: str) -> bool:
    return block_desc in IGNOR_BLOCKS


def _title_info_output_unit(needed_quantity: int, desc: str, _inner_flag: bool):
    if not _inner_flag:
        colored_needed_quantity = f'{Style.BRIGHT}{Fore.RED}{needed_quantity}{INITIAL_COLOR}{Style.NORMAL}'
        colored_block_description = f'{Style.BRIGHT}{Fore.RED}{desc}{INITIAL_COLOR}{Style.NORMAL}'
        print(f'\n{INITIAL_COLOR}制作「{colored_needed_quantity}」个「{colored_block_description}」需要:')
        return
    colored_needed_quantity = f'{Style.BRIGHT}{Fore.RED}{needed_quantity}{INNER_COLOR}{Style.NORMAL}'
    colored_block_description = f'{Style.BRIGHT}{Fore.RED}{desc}{INNER_COLOR}{Style.NORMAL}'
    print(f'{INNER_COLOR}制作「{colored_needed_quantity}」个「{colored_block_description}」需要:')


def _single_output(formula: dict, needed_quantity: int) -> tuple[dict, int]:
    material_name = (material for material in list(formula.keys())[1:])
    material_quantity = (Decimal(str(material * needed_quantity)) for material in list(formula.values())[1:])
    material_data = dict(zip(material_name, material_quantity))
    return material_data, formula['outputQty']


def _multi_output(formula: dict, needed_quantity: int) -> tuple[dict, int]:
    copies_str = str(needed_quantity / formula['outputQty'])
    copies = Decimal(copies_str).quantize(Decimal('0'))
    material_name = (material for material in list(formula.keys())[1:])
    material_quantity = (material * copies for material in list(formula.values())[1:])
    material_data = dict(zip(material_name, material_quantity))
    return material_data, formula['outputQty']


def _output_by_stack_calculator(material_data: dict, outputQty: int, needed_qty: int, _inner_flag: bool) -> Generator[
    dict, None, None]:
    for material_name, material_quantity in material_data.items():
        stack_count = material_quantity // 64
        majority = stack_count * 64
        subportion = material_quantity - majority

        remainder = 0
        if outputQty != 1:
            remainder = outputQty * material_quantity - needed_qty
        _master_information_output_unit(material_name, material_quantity, stack_count, 64, subportion, remainder,
                                        _inner_flag)
        yield {material_name: material_quantity}

    if _inner_flag:
        print(f'{INNER_COLOR}-' * SPACE_COUNT)
    else:
        print(f'{INITIAL_COLOR}-' * SPACE_COUNT)


def _master_information_output_unit(material_name: str, material_quantity: int, stack_count: int,
                                    stacks: int, subportion: int, remainder: int, _inner_flag: bool):
    if not _inner_flag:
        print(
                f'  {INITIAL_COLOR}{material_name}: {material_quantity} = {stack_count} x {stacks} + {subportion} ... {remainder}'
        )
    else:
        print(
                f'  {INNER_COLOR}{material_name}: {material_quantity} = {stack_count} x {stacks} + {subportion} ... {remainder}'
        )


_inner_data = []


def _get_inner_materials(material_data: Iterable[dict]) -> list[dict]:
    for block_info in material_data:
        _inner_data.append(block_info)
    _inner_data_copy = deepcopy(_inner_data)
    _inner_data.clear()
    return _inner_data_copy


def _inner_materials_calculator(_inner_data: list[dict]):
    for data in _inner_data:
        for desc, qty in data.items():
            _block: Block = next(get_block(desc, get_tag_by_description(desc)))
            if isinstance(_block, Block) and _allow_request(desc):
                _calculate_material_needed(_block, qty, 0, True)


max_requests = 1
requested_count = 0
checked = set()


def _allow_request(block_desc: str) -> bool:
    global max_requests, requested_count, checked

    requested_less_than_max = (requested_count < max_requests)
    is_checked = (block_desc in checked)
    if not (requested_less_than_max and not is_checked):
        checked.clear()
        requested_count = 0
        return False

    if _is_ignore_by_description(block_desc):
        max_requests = 1
    else:
        max_requests = 2
    checked.add(block_desc)
    requested_count += 1
    return True


def _calculate_material_needed(block: Block, required_quantity: int, already_held: int, inner_flag: bool = False) -> None:
    calc_count = required_quantity - already_held
    _title_info_output_unit(calc_count, block.description, inner_flag)

    for formula in block.formulas:
        if formula['outputQty'] == 1:
            _inner_materials_calculator(
                    _get_inner_materials(
                            _output_by_stack_calculator(*_single_output(formula, calc_count), needed_qty=calc_count,
                                                        _inner_flag=inner_flag)))
        else:
            _inner_materials_calculator(
                    _get_inner_materials(
                            _output_by_stack_calculator(*_multi_output(formula, calc_count), needed_qty=calc_count,
                                                        _inner_flag=inner_flag)))


def main(block_requires: str) -> None:
    RequireData = namedtuple('RequireData', ('block_required', 'block_required_quantity', 'already_held_quantity'))
    # 红石中继器 60 10, 红石比较器 60 10, 红石粉 66 1
    remove_empty_str = lambda text_list: [t for t in text_list if t]

    def block_require_datas():
        for _require_data in block_requires.split(','):
            yield RequireData(*remove_empty_str(_require_data.strip().split(' ')))

    for data in block_require_datas():
        # data.block_required:          The material that you required
        # data.block_required_quantity: The quantity that you required
        # data.already_held_quantity:   The quantity that already held

        block_needed_tag = get_tag_by_description(data.block_required)
        try:
            block: Block = next(get_block(data.block_required, block_needed_tag))
            _calculate_material_needed(block, _convert_str_quantity_to_int(data.block_required_quantity),
                                       _convert_str_quantity_to_int(data.already_held_quantity))
        except AttributeError as e:
            print(
                    f'未获取到「{block_needed_tag}」中的「{type(data.block_required)}={data.block_required}」,请先检查配方书.')
            print(e)


if __name__ == '__main__':
    main('红石中继器 60 10')
