import sys
from pathlib import Path
from getpass import getpass
from subprocess import call, DEVNULL
from shutil import copy, rmtree


__version__ = '2.0 Beta 1'


def get_internal_dir() -> Path:
    """
    Get working directory based on pyinstaller detection
    """
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent


def clear_temp():
    if TEMP_DIR.exists():
        rmtree(TEMP_DIR)
        notice_me('Временная директория удалена')


EXECUTABLE_DIR = Path(sys.executable).parent
GAME_DATA_UI_DIR = Path('data/ui/')

if GAME_DATA_UI_DIR.exists():
    # Detect if executable located in root of the game dir
    # And switch to game directory with required files
    EXECUTABLE_DIR = EXECUTABLE_DIR / GAME_DATA_UI_DIR

INTERNAL_DIR = get_internal_dir()
TEMP_DIR = EXECUTABLE_DIR / Path('.tmp/')
PATH_BIN = INTERNAL_DIR / Path('bin/')

PS4_PROMPTS_DIR = INTERNAL_DIR / Path('ps4_prompts/')

QUICKBMS_DIR = PATH_BIN / Path('./quickbms/')
QUICKBMS_EXEC = QUICKBMS_DIR / Path('quickbms.exe')
QUICKBMS_SCRIPT_DTT = QUICKBMS_DIR / Path('scripts/dtt.bms')

DTT_FILES = (
    EXECUTABLE_DIR / Path('ui_core_us.dtt'),
    EXECUTABLE_DIR / Path('ui_option_us.dtt')
)


def main():
    # Ensure required .dtt files 're on place
    notice_me('Проверяю, что все нужное на месте')
    missing = [file for file in DTT_FILES if not file.exists()]
    if len(missing) > 0:
        print("Данные файлы не найдены в текущей дериктории:")
        for missing_file in missing:
            print('  ', missing_file.name)
        return 0

    # Extract .dtt
    notice_me('Распаковка необходимых игровых архивов')
    for file in DTT_FILES:
        call_command([QUICKBMS_EXEC, '-Y', QUICKBMS_SCRIPT_DTT, file, TEMP_DIR / file.name[:-4]])

    notice_me('Перемещаю PS4 иконки в распакованный архив')
    copy(PS4_PROMPTS_DIR / 'ui_core_us_00000080.dds', TEMP_DIR / 'ui_core_us')
    copy(PS4_PROMPTS_DIR / 'ui_option_us_00000080.dds', TEMP_DIR / 'ui_option_us')

    # Inject the changes into the original .dtt archives
    notice_me('Вшиваю измененные текстуры в оригинальные архивы')
    for file in DTT_FILES:
        call_command([QUICKBMS_EXEC, '-Y', '-w', '-r', QUICKBMS_SCRIPT_DTT, file, TEMP_DIR / file.name[:-4]])

    notice_me('Готово! Очистка временных файлов...')
    clear_temp()


def show_intro():
    print('NieR: Automata - RUS ZOG')
    print('PS4 Prompts Patcher')
    print(f'\nversion: {__version__}')
    print('by @maximilionus <maximilionuss@gmail.com>')
    print('\nДля правильной работы должен находиться в корневой папке игры или же в папке "<NIER>\\data\\ui"\n')


def notice_me(text: str):
    """
    Make the print noticeable
    """
    print('👉 ', text)


def call_command(args=[], output=DEVNULL):
    call(args, stdout=output, stderr=output)


def pause():
    if getattr(sys, 'frozen', False):
        getpass('Press "Enter" to exit')


if __name__ == '__main__':
    show_intro()
    main()
    pause()
