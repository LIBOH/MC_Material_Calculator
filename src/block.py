from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable, Generator, TypeAlias

from static import *

Formulas: TypeAlias = list[dict, ...]
BlockData: TypeAlias = tuple[str, Formulas, str]

IGNOR_BLOCKS = {'铁锭', '铁块', '红石粉', '红石块', '下界合金锭', '下界合金块'}
GROUP_MAP = {
    '建筑方块': BuildingGroup,
    '染色方块': DyeGroup,
    '自然方块': NaturalGroup,
    '功能方块': FunctionGroup,
    '红石方块': RedstoneGroup,
}

group_block_map = {}


@dataclass
class Block:
    block_name: str
    formulas: Formulas
    description: str
    tag: str


def _map_block_description_by_group(group_map: dict):
    group_set = set()
    for group_name, group_data in group_map.items():
        for info in group_data:
            group_set.add(info[2])
        group_block_map.update({group_name: deepcopy(group_set)})
        group_set.clear()


def fetch_data(data: Iterable[BlockData]) -> Generator[BlockData, None, None]:
    for item in data:
        yield item


def map_items(blocks_info: Iterable[BlockData]) -> Generator[Block, None, None]:
    for info in blocks_info:
        yield Block(*info)


def _fetched_name(block: Block, target_name: str) -> bool:
    return block.block_name == target_name


def filter_name(blocks: Iterable[Block], block_name: str) -> Block:
    for block in blocks:
        if _fetched_name(block, block_name):
            return block


def _fetched_description(block: Block, description: str) -> bool:
    return block.description == description


def filter_description(blocks: Iterable[Block], description: str) -> Block:
    for block in blocks:
        if _fetched_description(block, description):
            return block


def _fetched_tag(block: Block, tag: str | None) -> bool:
    if tag:
        return block.tag == tag


def filter_tag(blocks: Iterable[Block], tag: str | None = None) -> Generator[Block, None, None]:
    for block in blocks:
        if _fetched_tag(block, tag):
            yield block


def _get_block_handle(block_name: str):
    for group in GROUP_MAP.values():
        yield filter_description(map_items(fetch_data(group)), block_name)


def get_block(block_name: str, tag: str = None) -> Generator[Block, None, None]:
    group = GROUP_MAP.get(tag)
    if group:
        block = filter_description(map_items(fetch_data(GROUP_MAP[tag])), block_name)
        yield block
        return

    blocks = _get_block_handle(block_name)
    for block in blocks:
        yield block
        return


def get_tag_by_description(block_desc: str) -> str:
    for group_name, block_set in group_block_map.items():
        if block_desc in block_set:
            return group_name


_map_block_description_by_group(GROUP_MAP)
if __name__ == '__main__':
    _block = '红石中继器'
    print(next(get_block(_block, get_tag_by_description(_block))))
