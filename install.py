# This is the main installation script, meant to be run
# by the developer on any OS to install
import platform
import libmgr
import os
import shutil
import arg_parsing.arg_cache
import importlib

requirement_cpu_count = 4
requirement_ram_mb = 16384
requirement_ram_mb_free = 10000
requirement_disk_space_mb = 100000


class colorText:
    def __init__(self):
        init = True

    reset = '\033[0m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


def check_system_requirements(psutil):
    cpu_count = os.cpu_count()
    ram_mb = psutil.virtual_memory().total / 1000000
    ram_mb_free = psutil.virtual_memory().available / 1000000
    disk_free_space_mb = shutil.disk_usage(os.getcwd())[2] / 1000000

    if cpu_count < requirement_cpu_count:
        print(
            colorText.bold + 'WARNING: Found ' +
            str(cpu_count) + ' logical CPU cores, we recommend at least ' +
            str(requirement_cpu_count) + ' cores.\n'
            'Objectscale performance may suffer.' + colorText.reset)
    if ram_mb < requirement_ram_mb:
        print(
            colorText.bold + 'WARNING: Found ' +
            str(ram_mb) + 'MB of RAM, we recommend at least ' +
            str(requirement_ram_mb) + 'MB of RAM.\n'
            'Objectscale performance will suffer.' + colorText.reset)
    if ram_mb_free < requirement_ram_mb_free:
        print(
            colorText.bold + 'WARNING: Found ' +
            str(ram_mb_free) + 'MB of free RAM, we recommend at least ' +
            str(requirement_ram_mb_free) + 'MB of free RAM.\n'
            'Objectscale performance may suffer.' + colorText.reset)
    if disk_free_space_mb < requirement_disk_space_mb:
        print(
            colorText.bold + 'WARNING: Found ' +
            str(disk_free_space_mb) + 'MB of free Disk Space, we recommend at least ' +
            str(requirement_disk_space_mb) + 'MB of free space.\n'
            'Objectscale performance may suffer.' + colorText.reset)
    if disk_free_space_mb * 2 < requirement_disk_space_mb:
        print(
            colorText.bold + 'Error: Disk space much too low to support a development environment. Please allocate '
                             'more free space on your disk (>'+requirement_disk_space_mb/2+' total), and then run again.' + colorText.reset)
        exit(112)


def main():
    print('Hello, Developer.')
    print('-----Libraries & Prerequisites-----')
    args = arg_parsing.arg_cache.parse_cache()
    manager = libmgr.libmgr()
    manager.get_libs()
    psutil = importlib.import_module('psutil')
    check_system_requirements(psutil)
    print('----- END Libraries & Prerequisites -----')
    os = platform.system().casefold()
    if os.find('linux') > -1:
        tux_installer = importlib.import_module('linux.install_linux')
        tux_installer.install_tux(args.args)
    elif os.find('windows') > -1:
        windows_installer = importlib.import_module('windows.install_windows')
        windows_installer.install_win(args.args, manager.certs_found)
    elif os.find('darwin') > -1:
        mac_installer = importlib.import_module('macos.install_macos')
        mac_installer.install_mac()
    else:
        print("Error: Unsupported OS: " + os)


if __name__ == "__main__":
    main()
else:
    print('Not run in main context.')
