UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3
TERMINAL = 4
OBSTACLE = 5

action_list = [
    'UP',
    'DOWN',
    'LEFT',
    'RIGHT',
    'TERMINAL',
    'OBSTACLE'
]

default_transition_model = {
            'UP': {
                'UP': 0.8,
                'DOWN': 0,
                'LEFT': 0.1,
                'RIGHT': 0.1
            },
            'DOWN': {
                'UP': 0,
                'DOWN': 0.8,
                'LEFT': 0.1,
                'RIGHT': 0.1
            },
            'LEFT': {
                'UP': 0.1,
                'DOWN': 0.1,
                'LEFT': 0.8,
                'RIGHT': 0
            },
            'RIGHT': {
                'UP': 0.1,
                'DOWN': 0.1,
                'LEFT': 0,
                'RIGHT': 0.8
            }
        }

blank_transition_model = {
            'UP': {
                'UP': 0,
                'DOWN': 0,
                'LEFT': 0,
                'RIGHT': 0
            },
            'DOWN': {
                'UP': 0,
                'DOWN': 0,
                'LEFT': 0,
                'RIGHT': 0
            },
            'LEFT': {
                'UP': 0,
                'DOWN': 0,
                'LEFT': 0,
                'RIGHT': 0
            },
            'RIGHT': {
                'UP': 0,
                'DOWN': 0,
                'LEFT': 0,
                'RIGHT': 0
            }
        }

blank_state_action_dict = {
            'UP': 0,
            'DOWN': 0,
            'LEFT': 0,
            'RIGHT': 0
        }
