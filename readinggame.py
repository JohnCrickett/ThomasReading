import argparse
import time
import os
import random
import pygame


def flash_screen(screen, duration):
    ticks = duration * 20
    count = 0
    colours = [(255,0,0),(255,255,0), (0,0,255), (255,0,255), (255,255,255)]
    clock = pygame.time.Clock()

    while ticks > 0:
        ticks -= 1
        screen.fill(colours[count])
        pygame.display.update()
        count += 1
        if count >= len(colours): count = 0
        clock.tick(500)

parser = argparse.ArgumentParser(description="Thomas' Reading Game.")
parser.add_argument("-s", "--start", type=int)
parser.add_argument("-t", "--top", type=int)
parser.add_argument("-c", "--count", type=int)
args = parser.parse_args()

words_start = 0
words_end = 10

if args.start and args.count:
    words_start = args.start
    words_end = words_start + args.count
    if words_end > 500:
        words_end = 500
elif args.top:
    words_end = args.top

words_count = words_end - words_start
print("Reading %s words from %s to %s" % (words_count, words_start, words_end))

words = []
with open('words.txt') as word_file:
    words = word_file.read().splitlines()

words = words[words_start:words_end]


freq = 71000     # audio CD quality
bitsize = -16    # unsigned 16 bit
channels = 2     # 1 is mono, 2 is stereo
buffer = 1024    # number of samples (experiment to get right sound)
pygame.mixer.pre_init(freq, bitsize, channels, buffer)
pygame.init()
pygame.mixer.init()
print(os.getcwd())
awesome = pygame.mixer.Sound("awesome.ogg")
pants = pygame.mixer.Sound("pants.ogg")
sun = pygame.mixer.Sound("cool.ogg")
duplon = pygame.mixer.Sound("duplon.ogg")

size = width, height = 1280,960
speed = [2, 2]
black = 0, 0, 0
white = 255,255,255
red = 255,255,0

screen = pygame.display.set_mode((size))
pygame.display.set_caption("Thomas' Reading Game")

font = pygame.font.Font('freesansbold.ttf',115)
scores_font = pygame.font.Font('freesansbold.ttf',42)


def render_screen(screen, word, score, guess):
    word_surface = font.render(word, True, black)
    word_rect = word_surface.get_rect()
    word_rect.center = ((width/2),(height/2))

    scores_surface = scores_font.render('Score: ' + str(score) + ' out of ' + str(guess), True, black)
    scores_rect = scores_surface.get_rect()
    scores_rect.center = ((width/2),(height-60))

    screen.fill(white)
    screen.blit(word_surface, word_rect)
    screen.blit(scores_surface, scores_rect)

    pygame.display.update()


def choose_next_word(words, word):
    next_word = random.choice(words)
    while next_word == word:
        next_word = random.choice(words)

    return next_word


done = False
guess = 0
score = 0
word = random.choice(words)
streak = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    guess += 1
                    streak = 0
                    word = choose_next_word(words, word)
                elif event.key == pygame.K_DOWN:
                    score += 1
                    guess += 1
                    streak += 1
                    word = choose_next_word(words, word)
                #elif event.key == pygame.K_RIGHT:
                #    flash_screen(screen, 5)
                #    awesome.play()
                elif event.key == pygame.K_ESCAPE:
                    done = True

        if streak == 10:
            awesome.play()
            awesome_words = ['You', 'are', 'on a', 'streak!', 'Everything', 'is', 'awesome!', 'Well', 'done!']
            index = 0
            streak += 1
            while pygame.mixer.get_busy():
                time.sleep(1)
                render_screen(screen, awesome_words[index], score, guess)
                index += 1
                if index == len(awesome_words): index = 0
        if streak == 21:
            pants.play()
            while pygame.mixer.get_busy():
                time.sleep(1)
            streak += 1
        if streak == 32:
            sun.play()
            while pygame.mixer.get_busy():
                time.sleep(1)
            streak += 1
        if streak == 43:
            duplon.play()
            while pygame.mixer.get_busy():
                time.sleep(1)
            streak = 0


        render_screen(screen, word, score, guess)





