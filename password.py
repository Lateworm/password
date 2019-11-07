import pygame, sys
from pygame.locals import *
from time import sleep
import random

# Constants

line_height = 20
window_dimensions = [640, 480] # 32 x 24 lines
(colour_bg, colour_text) = ((46,46,46), (126, 224, 126))
attempts = 4

word_sets = [
  [
    'PUTTING', 'CUTTING',            # _UTTING
    'HUNTING', 'SETTING',            # ___TING
    'HEARING', 'NOTHING', 'FINDING', # ____ING
    'PROVIDE', 'SURVIVE', 'REALIZE', # ____I_E
    'CANTINA', 'HUNTERS',            # __NT___
    'OVERLAP',
  ], [
    'SAILING', 'BAILING', # _AILING
    'GRAVELY', 'BRAVELY', # _RAVELY
    'TACKING', 'SINKING', # ___KING            
    'NETTING', 'BETTING', # _ETTING
    'WILDCAT', 'TARGETS',
    'HUNTING',
    'RAISINS', 'WETSUIT'
  ]
]

decoy_chars = [
  # TODO: store this as a string
  '`', '~', '!', '#', '$', '%', '^', '*', '(', ')', '-', '_', '+', '=',
  '{', '}', '[', ']', '|',
  ':', ';', '"', "'",
  ',', '<', '.', '>', '/', '?',
]

words = word_sets[random.randint(0, len(word_sets)-1)]
random.shuffle(words)
password = words[random.randint(0, len(words)-1)]


# Setup

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('PASSWORD_HACK >')

window = pygame.display.set_mode(window_dimensions)
window.fill(colour_bg)

font = pygame.font.SysFont('ubuntumono', 18)
# font.set_bold(True)


# methods

def line_offset(px):
  if px == 'center':
    return line_height
    # TODO: write centering logic
  else:
    return line_height * px

def window_print(*, str, colour = colour_text, x, y):
  window.blit(
    font.render(str, True, colour, colour_bg),
    (line_offset(x), line_offset(y))
  )
  pygame.display.update()
    
def window_input(prompt, x, y):
  input_str = []
  delimiter = ''
  
  window.blit(
    font.render(prompt + '_______', True, colour_text, colour_bg),
    (line_offset(x), line_offset(y))
  )
  pygame.display.update()
  
  while len(input_str) <= 7:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == K_BACKSPACE:
          input_str = input_str[0:-1]
          
        elif event.key == 13: # enter
          return delimiter.join(input_str)
        
        elif 97 <= event.key <= 127 and len(input_str) < 7:
          input_str.append(chr(event.key).upper())
        
        display_str = delimiter.join(input_str)
        for n in range(0, 7-len(input_str)):
          display_str = display_str + '_'
          
        display_line = prompt + display_str
        window.blit(
          font.render(display_line, True, colour_text, colour_bg),
          (line_offset(x), line_offset(y))
        )
        pygame.display.update()
  
  # TODO: avoid immediately returning on 7th character
  return delimiter.join(input_str)
# end window_input

def enter_to_exit():
  while True:
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == K_RETURN:
          pygame.quit()
          sys.exit()
    clock.tick(20)
# end enter_to_exit

def evaluate_guess(guess, password):
  matching_positions = 0
  for letter in enumerate(guess, start=0):
    if(letter[0] < len(password)):
      if(letter[1] == password[letter[0]]):
        matching_positions = matching_positions + 1
  return matching_positions
# end evaluate_guess

def handle_guess(attempts):
  guess = window_input('ENTER PASSWORD > ', 1, 18+4-attempts)
  matching_positions = evaluate_guess(guess, password)
  
  if (guess != password):
    window_print(
      str = "%s INCORRECT" %(guess),
      x = 20, y = 1 + ((4 - attempts) *3))
      # TODO: upgrade window_print to allow a negative integer as right offset
    window_print(
      str = "%s/7 IN MATCHING POSITIONS" %(matching_positions),
      x = 20, y = 2 + ((4 - attempts) *3))
    attempts = attempts - 1
    window_print(str = "%s ATTEMPT(S) LEFT" %(attempts), x = 1, y = 2)
    
  if (guess == password):
    window.fill(colour_bg)
    window_print(str = 'LOGIN SUCCESSFUL', x = 'center', y = 10)
    window_print(str = 'WELCOME BACK, COMMANDER', x = 'center', y = 12)
    window_print(str = 'PRESS ENTER TO EXIT', x = 'center', y = 14)
    enter_to_exit()
    return
  
  if (attempts == 0 and guess != password):
    window.fill(colour_bg)
    window_print(str = 'LOGIN FAILURE', x = 'center', y = 10)
    window_print(str = 'INITIATING SYSTEM LOCKDOWN', x = 'center', y = 12)
    window_print(str = 'PRESS ENTER TO EXIT', x = 'center', y = 14)
    enter_to_exit()
    return
    
  if (attempts > 0):
    handle_guess(attempts)
# end handle_guess
    
    
# Script

window_print(str = 'PASSWORD RECOVERY CONSOLE', x = 1, y = 1)
window_print(str = "%s ATTEMPT(S) LEFT" %(attempts), x = 1, y = 2)

for num, word in enumerate(words, start = 4):
  decoy_length = 9
  prefix_length = random.randint(1, decoy_length)
  postfix_length = decoy_length - prefix_length
  
  for i in range(0, prefix_length):
    word = decoy_chars[random.randint(0, len(decoy_chars)-1)] + word
  for i in range(0, postfix_length):
    word = word + decoy_chars[random.randint(0, len(decoy_chars)-1)]
    
  window_print(str = word, x = 1, y = num)
  
# guess = window_input(prompt = 'ENTER PASSWORD > ', x = 1, y = 18 + 4 - attempts)
handle_guess(attempts)


# Make the window closable
 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(20)
    
