import os;

# os.system("xdotool windowkill $(xdotool getmouselocation | grep -o '[0-9]\+$')")
# User configuration file typically located at `~/.config/nerd-dictation/nerd-dictation.py`

# This examples shows how explicit start/end commands can be implemented.
#
# This assumes dictation is always running in the background,
# special commands are spoken to start/end dictation which are excluded

# Global, track when dictation is active.
is_active = False
is_active_dictation = False

is_active_mouse = False

# -----------------------------------------------------------------------------
# Constants

# Commands to use.
START_COMMAND = ("start", "dictation")
FINISH_COMMAND = ("finish", "dictation")

START_Mouse = ("mickey", "mouse")
Mouse_kill = ("kill")
Mouse_up = ("up")
Mouse_down = ("down")
Mouse_left = ("left")
Mouse_right = ("right")
Mouse_click = ("click")
Mouse_double_click = ("double", "click")
Mouse_scroll = ("scroll")
Mouse_drag_start = ("drag")
Mouse_drag_end = ("drop")

Open_firefox = ("firefox")
Open_chrome = ("chrome")
Open_terminal = ("terminal")
Open_youtube = ("youtube")
Open_github = ("github")
Open_vscode = ("vscode")
Open_gmail = ("gmail")
Open_discord = ("discord")

FINISH_Mouse = ("finish", "mouse")
# -----------------------------------------------------------------------------

copy = "copy"
paste = "paste"
cut = "cut"
selectAll = "select all"
minimize = "minimize"
maximize = "maximize"
undo = "undo"
redo = "redo"


# -----------------------------------------------------------------------------
# Utility Functions

def match_words_at_index(haystack_words, haystack_index, needle_words):
    """
    Check needle_words is in haystack_words at haystack_index.
    """
    return (
        (needle_words[0] == haystack_words[haystack_index]) and
        (haystack_index + len(needle_words) <= len(haystack_words)) and
        (needle_words[1:] == haystack_words[haystack_index + 1 : haystack_index + len(needle_words)])
    )


# -----------------------------------------------------------------------------
# Main Processing Function

def nerd_dictation_process(text):
    global is_active, is_active_dictation, is_active_mouse

    words_input = tuple(text.split(" "))
    words = []
    i = 0

    # First check if there is text prior to having begun/ended dictation.
    # The part should always be ignored.
    if is_active:
        while i < len(words_input):
            if match_words_at_index(words_input, i, START_COMMAND):
                i += len(START_COMMAND)
                break
            i += 1
        if i == len(words_input):
            i = 0
        # Else keep the advance of 'i', since it skips text before dictation started.

    while i < len(words_input):
        word = words_input[i]
        if word == "kill":
            os.system("play Nuke.wav -q")
            os.system("xdotool windowkill $(xdotool getmouselocation | grep -o '[0-9]\+$')")
            i += 1
            continue
        if is_active:
            if match_words_at_index(words_input, i, FINISH_COMMAND):
                is_active = False
                i += len(FINISH_COMMAND)
                if i == len(words_input) and is_active_dictation == False:
                    is_active_dictation = True
                    os.system("play MicDrop.wav -q")
                
                continue
        else:
            if match_words_at_index(words_input, i, START_COMMAND) and is_active_dictation == False:
                is_active = True
                i += len(START_COMMAND)
                if i == len(words_input) and is_active_dictation == True:
                    is_active_dictation = False
                    os.system("play Dictation.wav -q")
                continue
            if match_words_at_index(words_input, i, START_Mouse) and is_active_mouse == False:
                if i == len(words_input) and is_active_mouse == False:
                    is_active_mouse = True
                    os.system("play mouse.wav -q")
                i += len(START_Mouse)
                continue
            if match_words_at_index(words_input, i, FINISH_Mouse) and is_active_mouse == True:
                if i == len(words_input):
                    is_active_mouse = False
                    os.system("play Squish.wav -q")
                i += len(FINISH_Mouse)
                continue
        if is_active_mouse and i == len(words_input):
            print("Processing: ", text)
            if match_words_at_index(words_input, i, Open_firefox):
                os.system("firefox &")
                i += len(Open_firefox)
                continue
            if match_words_at_index(words_input, i, Open_chrome):
                os.system("google-chrome &")
                i += len(Open_chrome)
                continue
            if match_words_at_index(words_input, i, Open_terminal):
                os.system("gnome-terminal &")
                i += len(Open_terminal)
                continue
            if match_words_at_index(words_input, i, Open_youtube):
                os.system("firefox https://www.youtube.com &")
                i += len(Open_youtube)
                continue
            if match_words_at_index(words_input, i, Open_github):
                os.system("firefox https://github.com &")
                i += len(Open_github)
                continue
            if match_words_at_index(words_input, i, Open_vscode):
                os.system("code &")
                i += len(Open_vscode)
                continue
            if match_words_at_index(words_input, i, Open_discord):
                os.system("discord &")
                i += len(Open_discord)
                continue
            if match_words_at_index(words_input, i, Open_gmail):
                os.system("firefox https://mail.google.com &")
                i += len(Open_gmail)
                continue
            if match_words_at_index(words_input, i, Mouse_up):
                os.system("xdotool mousemove_relative 0 -10")
                i += len(Mouse_up)
                continue
            if match_words_at_index(words_input, i, Mouse_down):
                os.system("xdotool mousemove_relative 0 10")
                i += len(Mouse_down)
                continue
            if match_words_at_index(words_input, i, Mouse_left):
                os.system("xdotool mousemove_relative -10 0")
                i += len(Mouse_left)
                continue
            if match_words_at_index(words_input, i, Mouse_right):
                os.system("xdotool mousemove_relative 10 0")
                i += len(Mouse_right)
                continue
            if match_words_at_index(words_input, i, Mouse_click):
                os.system("xdotool click 1")
                i += len(Mouse_click)
                continue
            if match_words_at_index(words_input, i, Mouse_double_click):
                os.system("xdotool click 1")
                os.system("xdotool click 1")
                i += len(Mouse_double_click)
                continue
            if match_words_at_index(words_input, i, Mouse_scroll):
                os.system("xdotool click 4")
                i += len(Mouse_scroll)
                continue
            if match_words_at_index(words_input, i, Mouse_drag_start):
                os.system("xdotool mousedown 1")
                i += len(Mouse_drag_start)
                continue
            if match_words_at_index(words_input, i, Mouse_drag_end):
                os.system("xdotool mouseup 1")
                i += len(Mouse_drag_end)
                continue

        if is_active:
            words.append(word)
        i += 1

    return " ".join(words)

