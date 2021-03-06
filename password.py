import pygame, sys
from pygame.locals import *
from time import sleep
import random

# CONTEXT

ctx = {
  # CONFIG
  'font_face': 'couriernew',
  'font_height': 18,
  'line_height': 20,
  'window_width': 32, # window dimensions in lines
  'window_height': 24,
  'window_title': 'PASSWORD_HACK >',
  'colour_bg': (46, 46, 46),
  'colour_text': (126, 224, 126),
  'colour_alpha': (86, 135, 86), # TODO: extract this to a function

  # CONTENT
  'word_sets': [
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
  ],
  'decoy_chars': '1234567890QWERTYUIOPASDFGHJKLZXCVBNM`~!@#$%^&*()-_=+[{]}\|;:,<.>/?',
  'attempts': 4,
}


# SETUP

ctx['words'] = ctx['word_sets'][random.randint(0, len(ctx['word_sets'])-1)]
random.shuffle(ctx['words'])
ctx['password'] = ctx['words'][random.randint(0, len(ctx['words'])-1)]


pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption(ctx['window_title'])

window = pygame.display.set_mode([ctx['line_height'] * ctx['window_width'], ctx['line_height'] * ctx['window_height']])
window.fill(ctx['colour_bg'])

# TODO: is there some way to package a font so we can get it to render the same cross-platform?
font = pygame.font.SysFont(ctx['font_face'], ctx['font_height'])
# font.set_bold(True)


# METHODS

def line_offset(px):
  if px == 'center':
    return ctx['line_height']
    # TODO: write centering logic
  else:
    return ctx['line_height'] * px

def window_print(*, str, colour = ctx['colour_text'], x, y):
  window.blit(
    font.render(str, True, colour, ctx['colour_bg']),
    (line_offset(x), line_offset(y))
  )
  pygame.display.update()
  # TODO: set up delayed printing
    
def window_input(prompt, x, y):
  input_str = []
  delimiter = ''
  
  window.blit(
    font.render(prompt + '_______', True, ctx['colour_text'], ctx['colour_bg']),
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
          font.render(display_line, True, ctx['colour_text'], ctx['colour_bg']),
          (line_offset(x), line_offset(y))
        )
        pygame.display.update()
  
  # TODO: handle window exit in this loop
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

def handle_guess(attempts, password):
  guess = window_input('ENTER PASSWORD > ', 1, 18+4-attempts)
  matching_positions = evaluate_guess(guess, password)
  
  if (guess != password):
    window_print(
      str = "%s INCORRECT" %(guess),
      x = 17, y = 1 + ((4 - attempts) *3))
      # TODO: upgrade window_print to allow a negative integer as right offset
    window_print(
      str = "%s/7 IN MATCHING POSITIONS" %(matching_positions),
      x = 17, y = 2 + ((4 - attempts) *3))
    attempts = attempts - 1
    window_print(str = "%s ATTEMPT(S) LEFT" %(attempts), x = 1, y = 2)
    
  if (guess == password):
    window.fill(ctx['colour_bg'])
    window_print(str = 'LOGIN SUCCESSFUL', x = 'center', y = 9)
    window_print(str = 'WELCOME BACK, COMMANDER', x = 'center', y = 11)
    window_print(str = 'PRESS ENTER TO EXIT', x = 'center', y = 13)
    enter_to_exit()
    return
  
  if (attempts == 0 and guess != password):
    window.fill(ctx['colour_bg'])
    window_print(str = 'LOGIN FAILURE', x = 'center', y = 9)
    window_print(str = 'INITIATING SYSTEM LOCKDOWN', x = 'center', y = 11)
    window_print(str = 'PRESS ENTER TO EXIT', x = 'center', y = 13)
    enter_to_exit()
    return
    
  if (attempts > 0):
    handle_guess(attempts, password)
# end handle_guess
    
  
# SCRIPT

window_print(str = 'PASSWORD RECOVERY CONSOLE', x = 1, y = 1)
window_print(str = "%s ATTEMPT(S) LEFT" %(ctx['attempts']), x = 1, y = 2)

for num, word in enumerate(ctx['words'], start = 4):
  decoy_length = 9
  total_length = 24
  prefix_length = random.randint(1, total_length - len(word) + 1)
  decoy_bg = ''
  decoy_prefix = ''

  for i in range(0, total_length):
    decoy_bg = decoy_bg + ctx['decoy_chars'][random.randint(0, len(ctx['decoy_chars'])-1)]
  for i in range(0, prefix_length):
    decoy_prefix = decoy_prefix + decoy_bg[i]
  
  window_print(str = decoy_bg, colour = ctx['colour_alpha'], x = 1, y = num)
  window_print(str = decoy_prefix + word, x = 1, y = num)
  window_print(str = decoy_prefix, colour = ctx['colour_alpha'], x = 1, y = num)
  
# guess = window_input(prompt = 'ENTER PASSWORD > ', x = 1, y = 18 + 4 - attempts)
handle_guess(ctx['attempts'], ctx['password'])


# Make the window closable
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(20)
    