import pyautogui
import time
from pynput import mouse, keyboard

# Variáveis para armazenar os movimentos, cliques e teclas capturadas
movimentos = []
teclas = []
capturando = True  # Variável de controle para parar a captura
parar_programa = False  # Variável para controlar o término das repetições

# Inicialização dos listeners
mouse_listener = None
keyboard_listener = None

# Função que captura os movimentos do mouse
def on_move(x, y):
    if capturando and not parar_programa:
        movimentos.append((x, y, 'move', time.time() - start_time))

# Função que captura cliques do mouse (esquerdo e direito)
def on_click(x, y, button, pressed):
    if capturando and pressed and not parar_programa:
        if button == mouse.Button.left:
            movimentos.append((x, y, 'left_click', time.time() - start_time))
        elif button == mouse.Button.right:
            movimentos.append((x, y, 'right_click', time.time() - start_time))

# Função que captura teclas pressionadas
def on_press(key):
    if capturando and not parar_programa:
        try:
            teclas.append((key.char, time.time() - start_time))  # Captura a tecla pressionada e o tempo
        except AttributeError:
            teclas.append((str(key), time.time() - start_time))  # Captura teclas especiais

# Função para detectar a tecla "Esc"
def on_press_cancel(key):
    global parar_programa
    if key == keyboard.Key.esc:
        print("Tecla 'Esc' pressionada, interrompendo...")  # Mensagem ao pressionar "Esc"
        parar_programa = True  # Sinaliza para parar a captura e repetições
        return False  # Para o listener de teclado

# Função para capturar os movimentos, cliques e teclas
def capturar_movimentos(duracao):
    global start_time, mouse_listener, keyboard_listener, capturando
    start_time = time.time()

    print(f"Capturando movimentos e teclas por {duracao} segundos. Mova o mouse e pressione teclas como desejar...")

    # Cria e inicia os listeners
    mouse_listener = mouse.Listener(on_move=on_move, on_click=on_click)
    keyboard_listener = keyboard.Listener(on_press=on_press)
    
    mouse_listener.start()  # Inicia o listener de mouse
    keyboard_listener.start()  # Inicia o listener de teclado

    time.sleep(duracao)  # Dura o tempo definido para captura

    capturando = False  # Para a captura após o tempo especificado
    
    mouse_listener.stop()  # Para o listener de mouse
    keyboard_listener.stop()  # Para o listener de teclado

    print("Captura concluída.")

# Função que repete os movimentos, cliques e teclas
def repetir_movimentos(movimentos, teclas, repeticoes):
    print(f"Repetindo os movimentos e teclas {repeticoes} vez(es)...")

    global keyboard_listener
    keyboard_listener = keyboard.Listener(on_press=on_press_cancel)
    keyboard_listener.start()  # Inicia o listener de teclado

    for repeticao in range(repeticoes):
        if parar_programa:
            break  # Se "Esc" for pressionado, interrompe as repetições

        start_time = time.time()
        print(f"Repetição {repeticao + 1}/{repeticoes}")

        # Reproduzir os movimentos do mouse
        for x, y, evento, t in movimentos:
            if parar_programa:
                break  # Interrompe no meio da execução se "Esc" for pressionado

            # Calcula o tempo restante para o próximo movimento
            tempo_espera = t - (time.time() - start_time)
            if tempo_espera > 0:
                time.sleep(tempo_espera)  # Somente dorme se o valor for positivo

            if evento == 'move':
                pyautogui.moveTo(x, y, duration=0)  # Movimenta o mouse rapidamente
            elif evento == 'left_click':
                pyautogui.click(x, y, button='left')
            elif evento == 'right_click':
                pyautogui.click(x, y, button='right')

        # Reproduzir as teclas pressionadas
        for tecla, t in teclas:
            if parar_programa:
                break  # Interrompe no meio da execução se "Esc" for pressionado

            # Calcula o tempo restante para o próximo evento de tecla
            tempo_espera = t - (time.time() - start_time)
            if tempo_espera > 0:
                time.sleep(tempo_espera)  # Somente dorme se o valor for positivo

            # Pressiona a tecla
            if tecla.startswith('Key.'):  # Para teclas especiais
                pyautogui.press(tecla.split('.')[1])  # Pressiona a tecla correspondente
            else:
                pyautogui.press(tecla)  # Pressiona a tecla normal

        print(f"Repetição {repeticao + 1} concluída.")

    keyboard_listener.stop()  # Para o listener de teclado ao sair do loop

    print("Repetições concluídas ou interrompidas.")

# Definir duração da captura e quantidade de repetições
duracao_captura = 10  # Capturar movimentos por 10 segundos
quantidade_repeticoes = 15  # Número de vezes para repetir os movimentos capturados

# Capturar movimentos e teclas
capturar_movimentos(duracao_captura)

# Repetir os movimentos e teclas capturados
time.sleep(2)  # Tempo de espera antes de repetir
repetir_movimentos(movimentos, teclas, quantidade_repeticoes)
