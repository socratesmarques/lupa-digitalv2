from time import monotonic

from config.joystick import DEBOUNCE_MS, GPIO_ATIVO, JOYSTICK_PIN_KEYS
from hardware.controles import Acao


KEY_TO_ACTION = {
    "UP": Acao.CIMA,
    "DOWN": Acao.BAIXO,
    "LEFT": Acao.ESQUERDA,
    "RIGHT": Acao.DIREITA,
    "+": Acao.ZOOM_MAIS,
    "PLUS": Acao.ZOOM_MAIS,
    "-": Acao.ZOOM_MENOS,
    "MINUS": Acao.ZOOM_MENOS,
    "SPACE": Acao.FREEZE,
    "ENTER": Acao.CENTRALIZAR,
    "C": Acao.CENTRALIZAR,
    "F": Acao.PROXIMO_MODO,
    "S": Acao.CAPTURAR,
    "G": Acao.GUIA_LEITURA,
    "F11": Acao.FULLSCREEN,
    "ESC": Acao.SAIR,
    "NONE": Acao.NENHUMA,
}


class BotoesGPIO:
    def __init__(self):
        self.disponivel = False
        self.wiringpi = None
        self._pins = {}
        self._state = {}
        self._last_event = {}

        for pin, key in JOYSTICK_PIN_KEYS.items():
            normalized = str(key).strip().upper()
            action = KEY_TO_ACTION.get(normalized)

            if action is None:
                print(
                    f"[GPIO] Tecla '{key}' ignorada no pino físico {pin}. "
                    "Confira config/joystick.py."
                )
                continue

            if action != Acao.NENHUMA:
                self._pins[int(pin)] = action

    def iniciar(self):
        if self.disponivel:
            return True
        if not GPIO_ATIVO:
            return False

        try:
            import wiringpi
            from wiringpi import GPIO

            self.wiringpi = wiringpi

            # Numeração PHYSICAL: os números em config/joystick.py são os
            # próprios números impressos no conector de 40 pinos.
            result = wiringpi.wiringPiSetupPhys()
            if result not in (0, None):
                return False

            for pin in self._pins:
                wiringpi.pinMode(pin, GPIO.INPUT)
                try:
                    wiringpi.pullUpDnControl(pin, GPIO.PUD_UP)
                except Exception:
                    pass

                self._state[pin] = int(wiringpi.digitalRead(pin))
                self._last_event[pin] = 0.0

            self.disponivel = True
            print("[GPIO] Joystick configurável ativado.")
            for pin, action in self._pins.items():
                print(f"[GPIO] Pino físico {pin} -> {action.name}")
            return True

        except Exception as exc:
            print(
                "[GPIO] Indisponível; interface e teclado continuam ativos: "
                f"{exc}"
            )
            return False

    def ler(self):
        if not self.disponivel:
            return Acao.NENHUMA

        now = monotonic()

        for pin, action in self._pins.items():
            try:
                current = int(self.wiringpi.digitalRead(pin))
            except Exception:
                continue

            previous = self._state.get(pin, 1)
            self._state[pin] = current

            if (
                previous == 1
                and current == 0
                and now - self._last_event.get(pin, 0) >= DEBOUNCE_MS / 1000
            ):
                self._last_event[pin] = now
                return action

        return Acao.NENHUMA

    def encerrar(self):
        self.disponivel = False
