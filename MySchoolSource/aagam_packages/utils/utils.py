import subprocess

from aagam_packages.terminal_yoda.terminal_yoda import *


def count_lines(extension, folder=""):
    command = f'(for /r {folder} %f in ' \
              f'({str(extension)}) do @type "%f") | find /c /v ""'
    yoda_saberize_print(command, YodaSaberColor.WHITE, YodaSaberColor.RED)
    try:
        lines = subprocess.check_output(command, shell=True).decode()
        return lines
    except subprocess.CalledProcessError as err:
        yoda_saberize_print(err, YodaSaberColor.WHITE, YodaSaberColor.RED)
    except BaseException as err:
        yoda_saberize_print(err, YodaSaberColor.WHITE, YodaSaberColor.RED)
