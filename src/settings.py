# game setup
WIDTH    = 900
HEIGHT   = 600
FPS      = 60
TILESIZE = 60.3

# ui
BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 149
ENERGY_BAR_WIDTH = 101
ITEM_BOX_SIZE = 90
UI_FONT = '../gameproj/graphics/font/joystix.ttf'
UI_FONT_SIZE = 18

# general colors
WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#242526'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

# ui colors
HEALTH_COLOR = 'crimson'
ENERGY_COLOR = 'deepskyblue'
UI_BORDER_COLOR_ACTIVE = 'gold'

# weapons
weapon_data = {
	'axe': {'cooldown': 300, 'damage': 15, 'graphic':'../gameproj/graphics/weapons/axe/axe_full.png'},
	'lance': {'cooldown': 400, 'damage': 20,'graphic':'../gameproj/graphics/weapons/lance/lance_full.png'},
	'sword': {'cooldown': 100, 'damage': 30,'graphic':'../gameproj/graphics/weapons/sword/sword_full.png'}}

# magic heheheha

magic_data = {
	'flame':{'strength':5, 'cost':20, 'graphic':'../gameproj/graphics/flame/fire.png' },
	'heal':{'strength':5, 'cost':5, 'graphic':'../gameproj/graphics/heal/heal.png'}
}
# enemy
monster_data = {

	'carrot': {'health': 300,'exp':10,'damage':3,'attack_type': 'thunder','attack_sound':'slash.wav','speed': 3, 'resistance': 4, 'attack_radius': 40, 'notice_radius': 200},
	'onigiri': {'health': 200,'exp':10,'damage':5,'attack_type': 'slash','attack_sound':'claw.wav','speed': 3, 'resistance': 4, 'attack_radius': 50, 'notice_radius': 200},}
