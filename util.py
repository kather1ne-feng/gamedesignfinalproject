from pygame.math import Vector2
# screen
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
TILE_SIZE = 64

# overlay positions 
OVERLAY_POSITIONS = {
	'tool' : (40, SCREEN_HEIGHT - 15), 
	'seed': (70, SCREEN_HEIGHT - 5)}

PLAYER_TOOL_OFFSET = {
	'left': Vector2(-50,40),
	'right': Vector2(50,40),
	'up': Vector2(0,-10),
	'down': Vector2(0,50)
}

LAYERS = {
	'water': 0,
	'ground': 1,
	'soil': 2,
	'soil water': 3,
	'rain floor': 4,
	'house bottom': 5,
	'ground plant': 6,
	'main': 7,
	'house top': 8,
	'fruit': 9,
	'rain drops': 10
}

APPLE_POS = {
	'Small': [(18,17), (30,37), (12,50), (30,45), (20,30), (30,10)],
	'Large': [(30,24), (60,65), (50,50), (16,40),(45,50), (42,70)]
}

GROW_SPEED = {
	'corn': 1,
	'tomato': 0.7
}

SALE_PRICES = {
	'wood': 4,
	'apple': 2,
	'corn': 10,
	'tomato': 20
}
PURCHASE_PRICES = {
	'corn': 4,
	'tomato': 5
}

MENUS = {
    'help': 0,
    'info': 1,
    'credits': 2
}

PLANT_INFO = {
	'beautyberry': ['Beauty Berry:',
                        'This shrub is native to the American South',
                        'The berries are very important foods for birds',
                        'Its berries are also very pretty to look at!'],
	'buckthorn': ['Buckthorn:',
               'Nonnative tree in the American South',
               'Highly aggressive growing plant',
               'can outcompete native species',
               'Can regenerate from its roots and stump sprouts'],
	'liriope': ['Liriope:',
             'An ornamental perennial evergreen grass',
             'It is invasive to North America',
             'It uses underground roots to spread rapidly'],
	'fieldmushroom': ['Field Mushroom',
                   'This mushroom is found around the world',
                   'It is not dangerous and helps decompose materials']
}