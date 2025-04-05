import subprocess

def show_notification(title, message):
    subprocess.run(['osascript', '-e', f'display notification "{message}" with title "{title}"'])

def show_dialog(title, message, buttons=None, default_button=""):
    script = f'''
    display dialog "{message}" with title "{title}" '''

    script += f'buttons "Got it" '
    script += 'with icon note'

    subprocess.run(['osascript', '-e', script])
