from collections import namedtuple
from typing import Any

from colorama import Fore

try:
    from .block_group_modifier import close_revers_open
except ImportError:
    from block_group_modifier import close_revers_open

BUILDING_GROUP_SPASE = ' ' * 17
DYE_GROUP_SPASE = ' ' * 12
NATURAL_GROUP_SPASE = ' ' * 16
FUNCTION_GROUP_SPASE = ' ' * 17
REDSTONE_GROUP_SPASE = ' ' * 17
SPASE_MAP = {
    '建筑方块': BUILDING_GROUP_SPASE,
    '染色方块': DYE_GROUP_SPASE,
    '自然方块': NATURAL_GROUP_SPASE,
    '功能方块': FUNCTION_GROUP_SPASE,
    '红石方块': REDSTONE_GROUP_SPASE
}
GROUP_PATH_MAP = {
    '建筑方块': './static/vanilla/BuildingGroup.py',
    '染色方块': './static/vanilla/DyeGroup.py',
    '自然方块': './static/vanilla/NaturalGroup.py',
    '功能方块': './static/vanilla/FunctionGroup.py',
    '红石方块': './static/vanilla/RedstoneGroup.py'
}


def _notify(func_name: str, entry: Any) -> None:
    print(f'{Fore.BLUE}{func_name} -> {Fore.GREEN}{entry}')


def _set_item_name(item: list, block_name: str) -> list:
    item.append(block_name)
    _notify('\n_set_item_name', item)
    return item


def _set_item_formulas(item: list, block_formulas: str) -> list:
    item.append(eval(block_formulas))
    _notify('_set_item_formulas', item)
    return item


def _set_item_description(item: list, description: str) -> list:
    item.append(description)
    _notify('_set_item_description', item)
    return item


def _set_item_tag(item: list, tag: str) -> list:
    item.append(tag)
    _notify('_set_item_tag', item)
    return item


def _create_item(**kwargs) -> tuple:
    item = []

    block_data = _set_item_tag(
            _set_item_description(_set_item_formulas(_set_item_name(item, kwargs['name']), kwargs['formulas']),
                                  kwargs['desc']), kwargs['tag'])
    block_data = tuple(block_data)
    _notify('_create_item', block_data)
    return block_data


def _write_item(group_path, block_item: tuple, working_group: str):
    with open(group_path, 'a+', encoding='utf-8') as f:
        f.write(f'{SPASE_MAP[working_group]}{block_item},\r\n')
    _notify('_write_item', 'Successfully added the block item.')


def main(block_items: str):
    BlockItem = namedtuple('BlockItem', ('name', 'formulas', 'desc', 'working_group'))
    remove_empty_str = lambda text_list: [t for t in text_list if t]

    def block_item_datas():
        for _item in block_items.split('|'):
            yield BlockItem(*remove_empty_str(_item.strip().split('-')))

    for item in block_item_datas():
        file_path = GROUP_PATH_MAP[item.working_group]
        close_revers_open(
                file_path,
                _write_item,
                file_path,
                _create_item(name=item.name, formulas=item.formulas,
                             desc=item.desc, tag=item.working_group),
                item.working_group
        )


if __name__ == '__main__':
    # 测试用例:
    #     建筑方块-oak_wood-({'outputQty': 3, '橡木原木': 4},)-橡木
    main("oak_wood-({'outputQty': 3, '橡木原木': 4},)-橡木-建筑方块")
