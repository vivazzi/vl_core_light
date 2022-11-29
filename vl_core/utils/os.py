import re
from os import walk, statvfs, listdir, remove
from os.path import join, islink, getsize, isfile, isdir, exists

import ctypes
import platform
import tempfile


def get_size(start_path='.'):
    if isfile(start_path):
        return getsize(start_path)

    total_size = 0
    for dir_path, dir_names, file_names in walk(start_path):
        for f in file_names:
            fp = join(dir_path, f)
            if not islink(fp):
                total_size += getsize(fp)

    return total_size


def get_free_space():
    def get_free_drive_space(drive):
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(drive), None, None, ctypes.pointer(free_bytes))
            return free_bytes.value
        else:
            return statvfs('/').f_bavail * statvfs('/').f_bsize

    my_temp = tempfile.gettempdir()
    my_drive = my_temp[0:2]
    return get_free_drive_space(my_drive)


def apply_func_to_file_in_folder(path, is_recursion, ignore_patterns, verbose, func, *args):
    files = listdir(path)
    for f in files:
        p = join(path, f)
        if not (ignore_patterns and any([re.search(pattern, f) for pattern in ignore_patterns])):
            if isdir(p):
                if is_recursion:
                    apply_func_to_file_in_folder(p, is_recursion, ignore_patterns, verbose, func, *args)
            else:
                if verbose:
                    print('{}: applying the function "{}" ({})'.format(join(path, f), func.__name__, func.__doc__))
                func(join(path, f), *args)


def is_file_changed(old_file, new_file):
    return old_file.name and new_file != old_file
