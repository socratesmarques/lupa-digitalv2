"""Configuração do Joystick Shield usando numeração física dos pinos.

O projeto usa wiringPiSetupPhys(), então as chaves abaixo são os números
PHYSICAL do conector GPIO do Orange Pi 3 LTS.

Altere somente JOYSTICK_PIN_KEYS para trocar a função de cada pino.
Teclas aceitas:
UP, DOWN, LEFT, RIGHT, +, -, SPACE, ENTER, C, F, S, G, F11, ESC e NONE.
"""

GPIO_ATIVO = True
DEBOUNCE_MS = 180

# pino físico -> tecla/atalho
JOYSTICK_PIN_KEYS = {
    11: "UP",
    13: "RIGHT",
    15: "DOWN",
    16: "LEFT",
    24: "-",
    22: "+",
    18: "SPACE",
}
