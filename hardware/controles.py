from enum import Enum, auto


class Acao(Enum):
    NENHUMA = auto(); ZOOM_MAIS = auto(); ZOOM_MENOS = auto()
    ESQUERDA = auto(); DIREITA = auto(); CIMA = auto(); BAIXO = auto()
    CENTRALIZAR = auto(); FREEZE = auto(); PROXIMO_MODO = auto()
    GUIA_LEITURA = auto(); HUD = auto(); FULLSCREEN = auto(); CAPTURAR = auto(); SAIR = auto()
