from time import monotonic

from hardware.controles import Acao
from hardware.pinos import DEBOUNCE_MS, GPIO_ATIVO, PIN_SHIELD_A, PIN_SHIELD_B, PIN_SHIELD_C, PIN_SHIELD_D, PIN_SHIELD_E, PIN_SHIELD_F, PIN_SHIELD_K


class BotoesGPIO:
    def __init__(self):
        self.disponivel = False; self.wiringpi = None
        self._pins = {
            PIN_SHIELD_A: Acao.CIMA, PIN_SHIELD_B: Acao.DIREITA,
            PIN_SHIELD_C: Acao.BAIXO, PIN_SHIELD_D: Acao.ESQUERDA,
            PIN_SHIELD_E: Acao.ZOOM_MENOS, PIN_SHIELD_F: Acao.ZOOM_MAIS,
            PIN_SHIELD_K: Acao.FREEZE,
        }
        self._state, self._last_event = {}, {}

    def iniciar(self):
        if self.disponivel: return True
        if not GPIO_ATIVO: return False
        try:
            import wiringpi
            from wiringpi import GPIO
            self.wiringpi = wiringpi
            result = wiringpi.wiringPiSetupPhys()
            if result not in (0, None): return False
            for pin in self._pins:
                wiringpi.pinMode(pin, GPIO.INPUT)
                try: wiringpi.pullUpDnControl(pin, GPIO.PUD_UP)
                except Exception: pass
                self._state[pin] = int(wiringpi.digitalRead(pin)); self._last_event[pin] = 0.0
            self.disponivel = True
            print("[GPIO] Joystick Shield ativado.")
            return True
        except Exception as exc:
            print(f"[GPIO] Indisponível; interface e teclado continuam ativos: {exc}")
            return False

    def ler(self):
        if not self.disponivel: return Acao.NENHUMA
        now = monotonic()
        for pin, action in self._pins.items():
            try: current = int(self.wiringpi.digitalRead(pin))
            except Exception: continue
            previous = self._state.get(pin, 1)
            self._state[pin] = current
            if previous == 1 and current == 0 and now - self._last_event.get(pin, 0) >= DEBOUNCE_MS / 1000:
                self._last_event[pin] = now
                return action
        return Acao.NENHUMA

    def encerrar(self): self.disponivel = False
