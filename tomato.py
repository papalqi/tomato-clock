#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import msvcrt
# Pomodoro 番茄工作法 https://en.wikipedia.org/wiki/Pomodoro_Technique
# ====== 🍅 Tomato Clock =======
# ./tomato.py         # start a 25 minutes tomato clock + 5 minutes break
# ./tomato.py -t      # start a 25 minutes tomato clock
# ./tomato.py -t <n>  # start a <n> minutes tomato clock
# ./tomato.py -b      # take a 5 minutes break
# ./tomato.py -b <n>  # take a <n> minutes break
# ./tomato.py -h      # help


import sys
import time
import subprocess

import keyboard as keyboard
from plyer import notification
WORK_MINUTES = 25
BREAK_MINUTES = 5


def main():
    try:
        while True:
            if len(sys.argv) <= 1:
                print(f'🍅 tomato {WORK_MINUTES} minutes. Ctrl+C to exit')
                tomato(WORK_MINUTES, 'It is time to take a break')
                print(f'🛀 break {BREAK_MINUTES} minutes. Ctrl+C to exit')
                tomato(BREAK_MINUTES, 'It is time to work')

            elif sys.argv[1] == '-t':
                minutes = int(sys.argv[2]) if len(sys.argv) > 2 else WORK_MINUTES
                print(f'🍅 tomato {minutes} minutes. Ctrl+C to exit')
                tomato(minutes, 'It is time to take a break')

            elif sys.argv[1] == '-b':
                minutes = int(sys.argv[2]) if len(sys.argv) > 2 else BREAK_MINUTES
                print(f'🛀 break {minutes} minutes. Ctrl+C to exit')
                tomato(minutes, 'It is time to work')
            elif sys.argv[1] == '-h':
                help()
            else:
                help()
            if input('👍 continue? (y/n)') == 'n':
                break

    except KeyboardInterrupt:
        print('\n👋 goodbye')
    except Exception as ex:
        print(ex)
        exit(1)

def tomato(minutes, notify_msg):
    start_time = time.perf_counter()
    paused = False
    pause_time = 0
    total_pause_time = 0
    while True:
        key_pressed = None
        if sys.platform.startswith('win'):
            if msvcrt.kbhit():
                key_pressed = msvcrt.getch().decode('utf-8')
        else:
            ready_to_read, _, _ = select.select([sys.stdin], [], [], 0)
            if ready_to_read:
                key_pressed = sys.stdin.read(1)

        if key_pressed == 'p':
            paused = True
            pause_time = time.perf_counter()
            print("\n暂停中... 按 'r' 继续")
        elif key_pressed == 'r':
            paused = False
            print("继续中... 按 'p' 暂停")
            total_pause_time += time.perf_counter() - pause_time
        elif key_pressed == 'q':
            break

        if not paused:
            diff_seconds = int(round(time.perf_counter() - start_time - total_pause_time))
            left_seconds = minutes * 60 - diff_seconds
            if left_seconds <= 0:
                print('')
                break
            countdown = '{}:{} ⏰'.format(int(left_seconds / 60), int(left_seconds % 60))
            duration = min(minutes, 25)
            progressbar(diff_seconds, minutes * 60, duration, countdown)
            time.sleep(1)
        else:
            time.sleep(0.1)
    notify_me(notify_msg)
# def tomato(minutes, notify_msg):
#     start_time = time.perf_counter()
#     # 清空输入缓存，光标新起一行
#     sys.stdin.flush()
#     sys.stdout.write('\r')
#     sys.stdout.flush()
#     while True:
#         diff_seconds = int(round(time.perf_counter() - start_time))
#         left_seconds = minutes * 60 - diff_seconds
#         if left_seconds <= 0:
#             print('')
#             break
#         countdown = '{}:{} ⏰'.format(int(left_seconds / 60), int(left_seconds % 60))
#         duration = min(minutes, 25)
#         progressbar(diff_seconds, minutes * 60, duration, countdown)
#         time.sleep(1)
#         check_input()
#     notify_me(notify_msg)


def progressbar(curr, total, duration=10, extra=''):
    frac = curr / total
    filled = round(frac * duration)
    print('\r', '🍅' * filled + '--' * (duration - filled), '[{:.0%}]'.format(frac), extra, end='')


def notify_me(msg):
    '''
    # macos desktop notification
    terminal-notifier -> https://github.com/julienXX/terminal-notifier#download
    terminal-notifier -message <msg>

    # ubuntu desktop notification
    notify-send

    # voice notification
    say -v <lang> <msg>
    lang options:
    - Daniel:       British English
    - Ting-Ting:    Mandarin
    - Sin-ji:       Cantonese
    '''

    print(msg)
    try:
        if sys.platform == 'darwin':
            # macos desktop notification
            subprocess.run(['terminal-notifier', '-title', '🍅', '-message', msg])
            subprocess.run(['say', '-v', 'Daniel', msg])
        elif sys.platform.startswith('linux'):
            # ubuntu desktop notification
            subprocess.Popen(["notify-send", '🍅', msg])
        else:
            # windows?
            notification.notify(
                title='🍅',
                message=msg,
                app_name='My Application',
                timeout=10
            )
            pass

    except:
        # skip the notification error
        pass


def help():
    appname = sys.argv[0]
    appname = appname if appname.endswith('.py') else 'tomato'  # tomato is pypi package
    print('====== 🍅 Tomato Clock =======')
    print(f'{appname}         # start a {WORK_MINUTES} minutes tomato clock + {BREAK_MINUTES} minutes break')
    print(f'{appname} -t      # start a {WORK_MINUTES} minutes tomato clock')
    print(f'{appname} -t <n>  # start a <n> minutes tomato clock')
    print(f'{appname} -b      # take a {BREAK_MINUTES} minutes break')
    print(f'{appname} -b <n>  # take a <n> minutes break')
    print(f'{appname} -h      # help')


if __name__ == "__main__":
    main()
