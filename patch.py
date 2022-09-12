from sys import exit
from pathlib import Path
from subprocess import call
from shutil import copy, rmtree


workdir = Path(__file__).parent
temp_dir = workdir / Path('.tmp/')
path_bin = workdir / Path('./bin/')

ps4_prompts_dir = workdir / Path('ps4_prompts/')

quickbms_dir = path_bin / Path('./quickbms/')
quickbms_exec = quickbms_dir / Path('quickbms.exe')
quickbms_script_dtt = quickbms_dir / Path('scripts/dtt.bms')

dtt_files = (
    workdir / Path('ui_core_us.dtt'),
    workdir / Path('ui_option_us.dtt')
)


def clear_temp():
    if temp_dir.exists():
        rmtree(temp_dir)
        notice_me('Cleaned up the temp dir')


def notice_me(text: str):
    """
    Make the print noticeable
    """
    print('👉 ', text)


def main():
    # Ensure required .dtt files 're on place
    notice_me('Ensuring that everything is on place')
    missing = [file for file in dtt_files if not file.exists()]
    if len(missing) > 0:
        print("These files are missing and should be placed right in this directory:")
        for missing_file in missing:
            print('  ', missing_file.name)
        exit()

    # Extract .dtt
    for file in dtt_files:
        call([quickbms_exec, '-Y', quickbms_script_dtt, file, temp_dir / file.name[:-4]])

    notice_me('Moving the PS4 prompts to the unpacked archives')
    copy(ps4_prompts_dir / 'ui_core_us_00000080.dds', temp_dir / 'ui_core_us')
    copy(ps4_prompts_dir / 'ui_option_us_00000080.dds', temp_dir / 'ui_option_us')

    # Inject the changes into the original .dtt archives
    notice_me('Injecting the changes into the original archives')
    for file in dtt_files:
        call([quickbms_exec, '-Y', '-w', '-r', quickbms_script_dtt, file, temp_dir / file.name[:-4]])

    notice_me('Done. Clean-Up...')
    clear_temp()


if __name__ == '__main__':
    main()
