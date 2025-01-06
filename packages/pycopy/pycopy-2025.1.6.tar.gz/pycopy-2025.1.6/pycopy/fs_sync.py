import os.path as path
import shutil
from pathlib import Path

from pycopy import terminal_formatting


def sync(src: Path, dest: Path, verbose=True, do_delete=False, check_modification_date=True, check_size=True,
         use_colors=True):
    if not src.exists():
        utils.hide_temp()
        print(f"Deleting {terminal_formatting.add_color(1, dest)}")
        delete_path(dest)
        return

    if src.is_dir():
        utils.print_temp(src)

        if dest.exists() and not dest.is_dir():
            utils.hide_temp()
            print(f"Deleting {dest}")
            delete_path(dest)

        dest.mkdir(parents=True, exist_ok=True)

        for item in dest.iterdir():
            sub_path = item.relative_to(dest)
            sync(src / sub_path, dest / sub_path, check_modification_date=check_modification_date)

        for item in src.iterdir():
            sub_path = item.relative_to(src)
            sync(src / sub_path, dest / sub_path, check_modification_date=check_modification_date)

        utils.hide_temp()
        return

    if not dest.exists():
        # dest.touch(exist_ok=True)
        dest_mod = -1
    elif dest.is_dir():
        utils.hide_temp()
        print(f"Deleting {dest}")
        delete_path(dest)
        # dest.touch(exist_ok=True)
        dest_mod = -1
    else:
        dest_mod = path.getmtime(dest)

    src_mod = path.getmtime(src)

    if src_mod <= dest_mod:
        return

    shutil.copyfile(src, dest)


def delete_path(file: Path):
    """
    Deletes this file if path is a folder or the folder and all subdirectories
    """
    if not file.exists():
        return

    if file.is_dir():
        for item in file.iterdir():
            delete_path(item)
        file.rmdir()
        return

    file.unlink(missing_ok=True)
