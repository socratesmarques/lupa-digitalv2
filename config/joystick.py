"""Configuração do Joystick Shield usando numeração física dos pinos.

O projeto usa wiringPiSetupPhys(), então as chaves abaixo são os números
PHYSICAL do conector GPIO do Orange Pi 3 LTS.

Mapeamento pensado para usar os BOTÕES do Joystick Shield:
D2=A, D3=B, D4=C, D5=D, D6=E, D7=F e D8=clique do joystick.

Altere somente JOYSTICK_PIN_KEYS para trocar a função de cada entrada.
Teclas aceitas:
UP, DOWN, LEFT, RIGHT, +, -, SPACE, ENTER, C, F, S, G, F11, ESC e NONE.
"""

GPIO_ATIVO = True
DEBOUNCE_MS = 180

# Orange Pi físico -> ação
# Shield D2 (A) -> OPi 11
# Shield D3 (B) -> OPi 12
# Shield D4 (C) -> OPi 13
# Shield D5 (D) -> OPi 15
# Shield D6 (E) -> OPi 16
# Shield D7 (F) -> OPi 18
# Shield D8 (clique) -> OPi 22
JOYSTICK_PIN_KEYS = {
    11: "UP",
    12: "DOWN",
    13: "LEFT",
    15: "RIGHT",
    16: "+",
    18: "-",
    22: "SPACE",
}
