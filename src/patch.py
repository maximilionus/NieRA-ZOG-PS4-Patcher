import sys
from pathlib import Path
from getpass import getpass
from subprocess import call, DEVNULL
from shutil import copy, rmtree


def show_intro():
    print('NieR: Automata - RUS ZOG')
    print('PS4 Prompts Patcher')
    print('by @maximilionus <maximilionuss@gmail.com>')
    print('\nДля правильной работы должен находиться в папке <NIER>\\data\\ui\n')


def get_internal_dir() -> Path:
    """
    Get working directory based on pyinstaller detection
    """
    if getattr(sys, 'frozen', False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).parent


def clear_temp():
    if temp_dir.exists():
        rmtree(temp_dir)
        notice_me('Временная директория удалена')


def notice_me(text: str):
    """
    Make the print noticeable
    """
    print('👉 ', text)


def call_command(args=[], output=DEVNULL):
    call(args, stdout=output, stderr=output)


executable_dir = Path(sys.executable).parent
internal_dir = get_internal_dir()
temp_dir = executable_dir / Path('.tmp/')
path_bin = internal_dir / Path('bin/')

ps4_prompts_dir = internal_dir / Path('ps4_prompts/')

quickbms_dir = path_bin / Path('./quickbms/')
quickbms_exec = quickbms_dir / Path('quickbms.exe')
quickbms_script_dtt = quickbms_dir / Path('scripts/dtt.bms')

dtt_files = (
    executable_dir / Path('ui_core_us.dtt'),
    executable_dir / Path('ui_option_us.dtt')
)


def main():
    # Ensure required .dtt files 're on place
    notice_me('Проверяю, что все нужное на месте')
    missing = [file for file in dtt_files if not file.exists()]
    if len(missing) > 0:
        print("Данные файлы не найдены в текущей дериктории:")
        for missing_file in missing:
            print('  ', missing_file.name)
        return 0

    # Extract .dtt
    notice_me('Распаковка необходимых игровых архивов')
    for file in dtt_files:
        call_command([quickbms_exec, '-Y', quickbms_script_dtt, file, temp_dir / file.name[:-4]])

    notice_me('Перемещаю PS4 иконки в распакованный архив')
    copy(ps4_prompts_dir / 'ui_core_us_00000080.dds', temp_dir / 'ui_core_us')
    copy(ps4_prompts_dir / 'ui_option_us_00000080.dds', temp_dir / 'ui_option_us')

    # Inject the changes into the original .dtt archives
    notice_me('Вшиваю измененные текстуры в оригинальные архивы')
    for file in dtt_files:
        call_command([quickbms_exec, '-Y', '-w', '-r', quickbms_script_dtt, file, temp_dir / file.name[:-4]])

    notice_me('Готово! Очистка временных файлов...')
    clear_temp()


def pause():
    if getattr(sys, 'frozen', False):
        getpass('Press "Enter" to exit')


if __name__ == '__main__':
    show_intro()
    main()
    pause()
