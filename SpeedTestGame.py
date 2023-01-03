import pygame
from pygame import mixer
import requests
import time
import os
import sys

# BUGS
# mute buttons should always be visible
# implement restart app function
# convert to OOP

pygame.init()
mixer.init()


# variables
x, y = 800, 450
begin_end = []
user_text = ""
wrong_counter = 0
font_size, text_size = 32, 23

# quote api request
phrase = requests.get('https://quotable.io/random?minLength=100?tags=famous-quotes')
phrase = phrase.json()
phrase = phrase['content']
phrase_length = len(phrase.split())


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


# colors and fonts
w, p, r = 'white', (254, 132, 132), (254, 132, 132)
color_active = pygame.Color('white')
color_passive = pygame.Color('grey')
color = color_passive
phrase_color, correct, incorrect = 'white', 'green', 'red'
font = pygame.font.Font(resource_path('LT Energy Bold.ttf'), 32)

# visual objects
icon = pygame.image.load(resource_path('icon.png'))
desk_icon = pygame.image.load(resource_path('desk_icon.ico'))
mute = pygame.image.load(resource_path('mute.png'))
unmute = pygame.image.load(resource_path('unmute.png'))

pygame.transform.scale(mute, (2, 2))
pygame.transform.scale(unmute, (2, 2))
bg_image = pygame.image.load(resource_path('bg.jpg'))

canvas = pygame.display.set_mode((x, y))
pygame.display.set_caption('Speedy Typer')
pygame.display.set_icon(icon)

mute_rect = pygame.Rect(10, 10, mute.get_width(), mute.get_height())
input_rect = pygame.Rect(100, 300, 600, 120)
start_rect = pygame.Rect(340, 150, 120, 50)
ref_rect = pygame.Rect(0, 0, 0, 0)

# booleans
_exit = False
active = False
toggle = True
start_click = False
made_mistake = True
done = False


def get_new_quote():
    try:
        new_quote = requests.get('https://quotable.io/random?minLength=100?tags=famous-quotes')
        new_quote = new_quote.json()
        new_quote = new_quote['content']
    except:
        new_quote = phrase
    return new_quote


def play_music():
    mixer.music.load(resource_path('bg_music.wav'))
    mixer.music.set_volume(0.1)
    mixer.music.play(loops=100)


def toggle_mute():
    img = pygame.image.load(resource_path('mute.png'))
    if not toggle:
        img = pygame.image.load(resource_path('unmute.png'))
    return img


def needed_for_sixty(z):
    num = 60 / z
    return int(num * z)


def calc_stats(points):
    duration = begin_end[1] - begin_end[0]
    sixty = needed_for_sixty(duration)
    accuracy = calc_accuracy()
    accuracy = accuracy - (points / accuracy * 100)
    wpm = phrase_length / duration * sixty

    wpm_stats = font.render(f"WPM: {int(wpm)}", True, 'white')
    time_stats = font.render(f"Time Taken (seconds): {round(duration, 2)}", True, 'white')
    acc_stats = font.render(f"Accuracy: {str(int(accuracy))}%", True, 'white')

    canvas.blit(wpm_stats, (200, 150))
    canvas.blit(time_stats, (200, 200))
    canvas.blit(acc_stats, (200, 250))


def calc_accuracy():
    count = 0
    for i, c in enumerate(phrase):
        try:
            if user_text[i] == c:
                count += 1
        except:
            continue
    accuracy = count / len(phrase) * 100
    return accuracy


def render_input_text(input_text, fsize, colour, screen, allowed_width):
    words = input_text.split()
    lines = []
    base_font = pygame.font.SysFont('system', fsize)

    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = base_font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        line = ' '.join(line_words)
        lines.append(line)

    y_offset = 0
    for line in lines:
        fw, fh = base_font.size(line)
        tx = 100
        ty = 300 + y_offset

        font_surface = base_font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))
        y_offset += fh

    if y_offset > 120:
        global text_size
        text_size -= 2


def render_quote(quote_text, fsize, colour, xcor, ycor, screen, allowed_width):
    words = quote_text.split()
    lines = []
    phrase_font = pygame.font.SysFont('system', fsize)

    while len(words) > 0:
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = phrase_font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break

        line = ' '.join(line_words)
        lines.append(line)

    y_offset = 0
    for line in lines:
        fw, fh = phrase_font.size(line)

        tx = xcor - fw / 2
        ty = ycor + y_offset

        font_surface = phrase_font.render(line, True, colour)
        screen.blit(font_surface, (tx, ty))
        y_offset += fh

    if y_offset >= 167:
        global font_size
        font_size -= 2


def main_menu():
    canvas.blit(bg_image, (0, 0))
    canvas.blit(current_image, (10, 10))


play_music()
current_image = pygame.image.load(resource_path('unmute.png'))
while not _exit:
    main_menu()
    cursor = pygame.mouse.get_pos()
    start_button = font.render('START', True, w, p)
    refresh_button = font.render('Refresh', True, r)

    # toggle music
    if not toggle:
        mixer.music.pause()
    else:
        mixer.music.unpause()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            _exit = True

        # hover over start button
        if start_rect.x + start_rect.w >= cursor[0] >= start_rect.x and \
                start_rect.y + start_rect.h >= cursor[1] >= start_rect.y:
            p, w = 'white', (254, 132, 132)
        else:
            w, p = 'white', (254, 132, 132)

        # hover over refresh
        if ref_rect.x + ref_rect.w >= cursor[0] >= ref_rect.x and \
                ref_rect.y + ref_rect.h >= cursor[1] >= ref_rect.y:
            r = w
        else:
            r = (254, 132, 132)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if start_rect.collidepoint(event.pos):
                start_click = True
            if ref_rect.collidepoint(event.pos):
                phrase = get_new_quote()
                now = time.time()
                user_text = ""

            if mute_rect.collidepoint(event.pos):
                current_image = toggle_mute()
                toggle = not toggle

        if event.type == pygame.KEYDOWN:
            made_mistake = True
            if active is True:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

    if active:
        color = color_active
    else:
        color = color_passive

    # text box input
    pygame.draw.rect(canvas, color, input_rect)
    render_input_text(user_text, text_size, 'black', canvas, 600)

    if not start_click:
        # draws the start button
        pygame.draw.rect(canvas, p, start_rect)
        canvas.blit(start_button, (start_rect.x + 18, start_rect.y + 8))
    else:
        # draws the refresh button
        ref_rect = pygame.Rect(670, 15, 110, 30)
        canvas.blit(refresh_button, (ref_rect.x, ref_rect.y))
        render_quote(phrase, font_size, phrase_color, 400, 150, canvas, 750)

        # starts timer
        active = True
        now = time.time()
        if len(begin_end) < 1:
            begin_end.append(now)

        # check for correct typing
        try:
            if user_text[len(user_text) - 1] == phrase[len(user_text) - 1]:
                phrase_color = correct
                if user_text.find('*') != -1:
                    phrase_color = incorrect
            else:
                if made_mistake:
                    wrong_counter += 1
                    made_mistake = False

                phrase_color = incorrect
                user_text = user_text[:len(user_text) - 1] + '*'

        except:
            pass

        # if user text matches the given quote
        if user_text == phrase:
            done = True
            end = time.time()
            if len(begin_end) < 2:
                begin_end.append(end)

    # display results
    if done is True:
        canvas.blit(bg_image, (0, 0))
        calc_stats(wrong_counter)

    pygame.display.update()
