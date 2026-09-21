"""Teste simples dos botões do Joystick Shield no Orange Pi 3 LTS.

Usa wiringPiSetupPhys(), portanto os números abaixo são os pinos FÍSICOS
do conector GPIO do Orange Pi.
"""

import time

import wiringpi
from wiringpi import GPIO


BOTOES = {
    11: "BOTAO A",
    13: "BOTAO B",
    15: "BOTAO C",
    16: "BOTAO D",
    18: "BOTAO E",
    22: "BOTAO F",
    24: "CLIQUE JOYSTICK",
}


def iniciar_gpio():
    resultado = wiringpi.wiringPiSetupPhys()

    if resultado not in (0, None):
        print("Erro ao iniciar GPIO")
        return False

    for pino in BOTOES:
        wiringpi.pinMode(pino, GPIO.INPUT)

        try:
            wiringpi.pullUpDnControl(pino, GPIO.PUD_UP)
        except Exception:
            pass

    return True


def main():
    print("==============================")
    print(" TESTE JOYSTICK SHIELD")
    print("==============================")

    if not iniciar_gpio():
        return

    estados_anteriores = {}

    for pino in BOTOES:
        estados_anteriores[pino] = wiringpi.digitalRead(pino)

    print()
    print("Pressione os botoes do joystick...")
    print("CTRL+C para sair.")
    print()

    try:
        while True:
            for pino, nome in BOTOES.items():
                estado_atual = wiringpi.digitalRead(pino)
                estado_anterior = estados_anteriores[pino]

                if estado_anterior == 1 and estado_atual == 0:
                    print(f"[PRESSIONADO] {nome} | pino fisico {pino}")

                elif estado_anterior == 0 and estado_atual == 1:
                    print(f"[SOLTO]       {nome} | pino fisico {pino}")

                estados_anteriores[pino] = estado_atual

            time.sleep(0.01)

    except KeyboardInterrupt:
        print()
        print("Teste encerrado.")


if __name__ == "__main__":
    main()
