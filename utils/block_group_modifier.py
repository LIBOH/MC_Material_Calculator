import os
from typing import Any


def _notify(func_name: str, entry: Any) -> None:
    print(f'{func_name} -> {entry}')


def _modify_last_line(file_path: str, modify_str: str):
    with open(file_path, 'rb') as f:
        offset = -50
        while True:
            f.seek(offset, 2)
            lines = f.readlines()
            if len(lines) >= 2:
                last_line = list(lines[-1].decode())
                break
            offset *= 2

    last_line[-3] = modify_str
    _notify('_modify_last_line', repr(f'{last_line[-3]} >> {modify_str}'))
    new_str = ''.join(last_line)
    return new_str


def _delete_last_line(file_path: str):
    m = 150
    with open(file_path, 'rb+') as f:
        f.seek(-m, os.SEEK_END)
        lines = f.readlines()
        f.seek(-len(lines[-1]), os.SEEK_END)
        f.truncate()
        _notify('_delete_last_line', 'The last line was successfully deleted.')


def _rewrite_last_line(file_path: str, last_line):
    with open(file_path, 'a+', encoding='utf-8') as f:
        f.write(last_line)
    _notify('_rewrite_last_line', 'The last line was successfully overwritten.')


def _remove_trailing_empty_lines(file_path: str):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        while lines and lines[-1].strip() == '':
            lines.pop()

        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)


def _close_to_open(file_path: str):
    _notify('_close_to_open', 'Opening last line ")"')
    new_last_line = _modify_last_line(file_path, '\n')
    _delete_last_line(file_path, )
    _rewrite_last_line(file_path, new_last_line)
    _remove_trailing_empty_lines(file_path)


def _open_to_close(file_path: str):
    _notify('_open_to_close', 'Closing last line ")"')
    new_last_line = _modify_last_line(file_path, ')')
    _delete_last_line(file_path, )
    _rewrite_last_line(file_path, new_last_line)
    _remove_trailing_empty_lines(file_path)


def close_revers_open(file_path: str, mid_func, *args, **kwargs):
    _close_to_open(file_path)
    mid_func(*args, **kwargs)
    _open_to_close(file_path)


if __name__ == '__main__':
    path = '../static/TestGroup.py'
    # close_to_open(path)
    # open_to_close(path)
