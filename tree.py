# /usr/bin/env python3
# coding: utf-8

import os
import sys
import colorama

dirs = 0
files = 0


def lookahead(iterable):
    it = iter(iterable)

    try:
        last = next(it)
    except StopIteration:
        return None, True

    for val in it:
        yield last, False
        last = val

    yield last, True


def traverse_dir(directory, index_map=None):
    global dirs, files
    try:
        items = os.scandir(directory)
    except PermissionError:
        return

    for item, is_last in lookahead(items):
        if item is None or item.is_symlink() or item.name.startswith('.'):
            continue

        out_string = ''
        for state in index_map:
            out_string += '│   ' if not state else '    '

        color = colorama.Fore.MAGENTA if (
            is_dir := item.is_dir()) else colorama.Fore.CYAN
        out_string += f'{"└──⩺" if is_last else "├──⩺"} {color}{item.name}{colorama.Style.RESET_ALL}'
        print(out_string)

        if is_dir:
            dirs += 1
            traverse_dir(item, index_map + [is_last])
        else:
            files += 1


def main(argc, argv):
    if argc < 2:
        return 1

    print(colorama.Fore.MAGENTA+argv[1]+colorama.Style.RESET_ALL)
    traverse_dir(argv[1], [])
    print(f"{dirs} directorie(s), {files} file(s)")
    return 0


if __name__ == '__main__':
    exit(main(len(sys.argv), sys.argv))
