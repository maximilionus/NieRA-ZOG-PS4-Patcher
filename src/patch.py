import sys
from pathlib import Path
from getpass import getpass
from subprocess import call, DEVNULL
from shutil import copy, rmtree, get_terminal_size


__version__ = '2.0 Beta 2'


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
        notice_me("Ошибка. Не найдены необходимые файлы:", '!')
        for missing_file in missing:
            print('   - ', missing_file.name)
        print(
            'Убедитесь, что у вас установлена последняя версия руссификатора от ZOG.'
            ' Патчер расчитан на работу только с ZOG руссификатором.'
        )
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
    centered_lines = (
        'NieR: Automata - RUS ZOG',
        'PS4 Prompts Patcher',
        f'version: {__version__}\n',
        'by @maximilionus <maximilionuss@gmail.com>',
        'Полностью совместимая версия локализатора: "Версия 1.31 от 16.07.21"'
    )
    for line in centered_lines:
        print(
            center_string_terminal(line)
        )

    print(
        '\nЭтот патч внесет изменения в некоторые игровые архивы руссификатора ZOG. '
        'Что бы вернуть все в оригинальное состояние просто переустановите '
        'руссификатор или же удалите его полностью.'
    )
    print('\nДля правильной работы должен находиться в корневой папке игры или же в папке "<NIER>\\data\\ui"\n')


def request_user_confirmation() -> bool:
    result = False
    while True:
        user_input = input('? Продолжаем? [(y)es / (n)o)]: ')
        if len(user_input) > 0: break

    if user_input[0].lower() == 'y':
        result = True

    return result


def notice_me(text: str, notice_symbol='>'):
    """
    Make the print noticeable
    """
    print(notice_symbol, text)


def center_string_terminal(string: str) -> str:
    """
    Center the string to the terminal window size
    """
    return string.center(
        get_terminal_size()[0]
    )


def call_command(args=[], output=DEVNULL):
    call(args, stdout=output, stderr=output)


def pause():
    if getattr(sys, 'frozen', False):
        getpass('Press "Enter" to exit')


if __name__ == '__main__':
    show_intro()
    if request_user_confirmation():
        main()
        pause()
    else:
        notice_me('Подтверждение не получено, выход', '!')
