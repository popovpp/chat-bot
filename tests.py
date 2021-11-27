import pytest

import tbot1


@pytest.fixture(scope='module')
def set_triggers_states():
    
    triggers_states = [[('большую', tbot1.states[1]),
                       ('наличкой', tbot1.states[3]),
                       ('да', tbot1.states[7]),
                       ('нет', tbot1.states[11]),
                       ('До свидания', tbot1.states[10]),
                       ('/start', tbot1.states[0])
                      ],
                      [('большую', tbot1.states[1]),
                       ('картой', tbot1.states[4]),
                       ('да', tbot1.states[7]),
                       ('нет', tbot1.states[11]),
                       ('До свидания', tbot1.states[10]),
                       ('/start', tbot1.states[0])
                      ],
                      [('маленькую', tbot1.states[2]),
                       ('наличкой', tbot1.states[5]),
                       ('да', tbot1.states[7]),
                       ('нет', tbot1.states[11]),
                       ('До свидания', tbot1.states[10]),
                       ('/start', tbot1.states[0])
                      ],
                      [('маленькую', tbot1.states[2]),
                       ('картой', tbot1.states[6]),
                       ('да', tbot1.states[7]),
                       ('нет', tbot1.states[11]),
                       ('До свидания', tbot1.states[10]),
                       ('/start', tbot1.states[0])
                      ],
                      [('маленькую', tbot1.states[2]),
                       ('картой', tbot1.states[6]),
                       ('нет', tbot1.states[8]),
                       ('нет', tbot1.states[11]),
                       ('До свидания', tbot1.states[10]),
                       ('/start', tbot1.states[0])
                      ]
                      ]
    return triggers_states

def test_start_state():
    assert tbot1.lump.state == tbot1.states[0]

def test_all_states(set_triggers_states):
	for chain in set_triggers_states:
		for trigger_state in chain:
		    tbot1.lump.trigger(trigger_state[0])
		    assert tbot1.lump.state == trigger_state[1]
