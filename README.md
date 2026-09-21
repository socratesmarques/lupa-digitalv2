# Lupa Digital V2 — Orange Pi 3 LTS

Aplicação reescrita em **PySide6 + OpenCV**, baseada na estrutura de câmera e
interface usada no projeto `deteccao-facial`. Não usa mais `cv2.imshow()`.

## Funções

- câmera responsiva, mantendo a proporção da imagem;
- zoom de 1× a 4× e movimentação da área ampliada;
- congelamento e captura da imagem;
- seis modos de leitura e melhoria opcional de texto;
- guia horizontal de leitura;
- fullscreen automático no Orange Pi;
- reconexão automática quando a câmera falhar;
- teclado, toque e Joystick Shield GPIO.

## Instalação no Orange Pi

```bash
sudo apt update
sudo apt install -y python3-venv python3-opencv

git clone https://github.com/socratesmarques/lupa-digital.git
cd lupa-digital
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -r requirements-orange-pi.txt
python main.py
```

Não execute com `sudo` dentro da sessão gráfica. Use o Python do ambiente
virtual no autostart.

## Selecionar a câmera externa

Por padrão, a lupa testa automaticamente as câmeras `0`, `2`, `1` e `3`.
Para fixar uma câmera específica:

```bash
LUPA_CAMERA=/dev/video2 python main.py
```

No autostart:

```bash
env LUPA_CAMERA=/dev/video2 /caminho/lupa-digital/.venv/bin/python /caminho/lupa-digital/main.py
```

Também existem `LUPA_WIDTH`, `LUPA_HEIGHT`, `LUPA_FPS` e `LUPA_FULLSCREEN`
(`1` ou `0`). O padrão ARM é 640×480 a 24 FPS para reduzir travamentos.

## Configurar o joystick GPIO

A configuração do joystick fica em:

```text
config/joystick.py
```

O projeto usa `wiringPiSetupPhys()`, então os números são os **pinos físicos**
do conector GPIO do Orange Pi.

Exemplo:

```python
JOYSTICK_PIN_KEYS = {
    11: "UP",
    13: "RIGHT",
    15: "DOWN",
    16: "LEFT",
    24: "-",
    22: "+",
    18: "SPACE",
}
```

Para mudar a função de um botão, altere apenas o valor à direita. Por exemplo,
para fazer o pino físico 18 salvar uma captura:

```python
18: "S",
```

Teclas aceitas:

| Tecla configurada | Ação |
|---|---|
| `UP` | mover para cima |
| `DOWN` | mover para baixo |
| `LEFT` | mover para esquerda |
| `RIGHT` | mover para direita |
| `+` ou `PLUS` | aumentar zoom |
| `-` ou `MINUS` | diminuir zoom |
| `SPACE` | congelar / retomar |
| `ENTER` ou `C` | centralizar |
| `F` | trocar modo de leitura |
| `S` | salvar captura |
| `G` | ativar / desativar guia de leitura |
| `F11` | alternar tela cheia |
| `ESC` | fechar a aplicação |
| `NONE` | desativar o pino |

Também é possível alterar `DEBOUNCE_MS` em `config/joystick.py` para ajustar a
sensibilidade contra cliques repetidos.

## Atalhos

| Tecla | Função |
|---|---|
| `+` / `-` | aumentar / diminuir zoom |
| `Espaço` | congelar / retomar |
| `F` | trocar modo de leitura |
| `S` | salvar captura |
| `C` | centralizar zoom |
| `F11` | alternar tela cheia |
| `Esc` | sair da tela cheia |
