import PyInstaller.__main__

app_name = 'PS4 Prompts ZOG Patcher'
app_icon_win = './img/icon.ico'

PyInstaller.__main__.run([
    './patch.py',
    '--onefile',
    '--name', app_name,
    '--add-data', '../bin;./bin',  # Add all binary tools
    '--add-data', '../ps4_prompts;./ps4_prompts',  # Add ps4 dualshock textures
    '--icon', app_icon_win
])
