import turtle
import random
import time
import os
import sys
#na parte de guardar carregar estado ficheiro guardar valores fixos para depoois voltar se for preciso tlgd ? poder usar split separar com espaços, é tipo a configuração das coisas do jogo 
# =========================
# Parâmetros / Constantes
# =========================
LARGURA, ALTURA = 600, 900
BORDA_X = (LARGURA // 2) - 20
BORDA_Y = (ALTURA // 2) - 10

PLAYER_SPEED = 20
PLAYER_BULLET_SPEED = 16

ENEMY_ROWS = 3
ENEMY_COLS = 10
ENEMY_SPACING_X = 60
ENEMY_SPACING_Y = 60
ENEMY_SIZE = 32
ENEMY_START_Y = BORDA_Y - ENEMY_SIZE    # topo visível
ENEMY_FALL_SPEED = 0.5
ENEMY_DRIFT_STEP = 2
ENEMY_FIRE_PROB = 0.006
ENEMY_BULLET_SPEED = 8
ENEMY_INVERT_CHANCE = 0.05
ENEMY_DRIFT_CHANCE = 0.5

COLLISION_RADIUS = 10
HIGHSCORES_FILE = "highscores.txt"
SAVE_FILE = "savegame.txt"
TOP_N = 10

STATE = None  # usado apenas para callbacks do teclado

# =========================
# Top Resultados (Highscores)
# =========================
def ler_highscores(filename):
    print("[ler_highscores] por implementar")
    highscores = []
    if not filename:
        return highscores
    if os.path.exists(filename):
        with open(filename, "r") as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 2:
                    continue
                nome = parts[0]
                try:
                    score = int(parts[1])
                except ValueError:
                    continue
                highscores.append((nome, score))
    highscores = sorted(highscores, key=lambda x: x[1], reverse=True)[:TOP_N]
    return highscores
def atualizar_highscores(filename, score):
    print("[atualizar_highscores] por implementar")
    if not filename:
        return
    highscores = ler_highscores(filename)
    if len(highscores) < TOP_N or score > highscores[-1][1]:
        nome = input("Novo Highscore! Insira o seu nome: ")
        highscores.append((nome, score))
        highscores = sorted(highscores, key=lambda x: x[1], reverse=True)[:TOP_N]
        with open(filename, "w") as f:
            for nome, sc in highscores:
                f.write(f"{nome} {sc}\n")

# =========================
# Guardar / Carregar estado (texto)
# =========================
def guardar_estado_txt(filename, state):
    print("[guardar_estado_txt] por implementar")
    state = STATE
    
    player = state["player"]  
    inimigos = state["enemies"]
    movimento_inimigo = state["enemy_moves"]
    balas_player = state["player_bullets"]
    bala_inimigos = state["enemy_bullets"]
    pontos = state["score"]
    frames = state["frames"]

    with open('savegame.txt', 'w') as save:
        save.write(f"pos_player: {player.pos()}\n")
        
        for inimigo in inimigos:
            pos_x_in = inimigo.xcor()
            pos_y_in = inimigo.ycor()
            save.write(f"pos_in: {pos_x_in} {pos_y_in}\n")

        for movimento in movimento_inimigo:
            proximo_movimento = str(movimento)
            save.write(f"movimento: {proximo_movimento}\n")

        for Bin in bala_inimigos:
            pos_x_bin = Bin.xcor()
            pos_y_bin = Bin.ycor()
            save.write(f"pos_bin: {pos_x_bin} {pos_y_bin}\n")

        for Bpl in balas_player:
            pos_x_Bpl = Bpl.xcor()
            pos_y_Bpl = Bpl.ycor()
            save.write(f"pos_bpl: {pos_x_Bpl} {pos_y_Bpl}")

        save.write(f"socore: {pontos}\n")
        save.write(f"frame_atual: {frames}")

def carregar_estado_txt(filename):
    print("[carregar_estado_txt] por implementar")

    save_player = []
    save_inimigos = []
    save_movimento_inimigo = []
    save_balas_inimigas = []
    save_balas_player = []
    save_score = []
    save_frame = []

    
    with open('savegame.txt', 'r') as save:
        dado = save.readlines()
        if dado.startswith("pos_player:"):
            save_player.append(dado)
        
        elif dado.startswith("pos_in:"):
            save_inimigos.append(dado)
        
        elif dado.startswith("movimento:"):
            save_movimento_inimigo.append(dado)
        
        elif dado.startswith("pos_bin:"):
            save_balas_inimigas.append(dado)
        
        elif dado.startswith("pos_bpl:"):
            save_balas_player.append(dado)
        
        elif dado.startswith("score:"):
            save_score.append(dado)
        
        elif dado.startwith("frame:"):
            save_frame.append(dado)
        
    
# =========================
# Criação de entidades (jogador, inimigo e balas)
# =========================
def criar_entidade(x,y, tipo="enemy"):
    t = turtle.Turtle(visible=False)
    if tipo == "player":
        t.shape("player.gif")
    else:
        t.shape("enemy.gif")
    
    print("[criar_entidade] por implementar")
    

    t.showturtle()
    return t 

def criar_bala(x, y, tipo):
    t = turtle.Turtle(visible=False)
    
    print("[criar_bala] por implementar")
    t = turtle.Turtle(visible=False)
    t.shape("square")
    t.color("yellow" if tipo == "player" else "red")
    t.shapesize(stretch_wid=0.2, stretch_len=0.8)
    t.setheading(90 if tipo == "player" else -90)
    t.penup()
    t.goto(x, y)
    t.showturtle()
    return t

def spawn_inimigos_em_grelha(state, posicoes_existentes, dirs_existentes=None):
    print("[spawn_inimigos_em_grelha] por implementar")

    enemies = []
    enemy_moves = []
    
    # Calcula posição inicial para centralizar a grelha
    start_x = -((ENEMY_COLS - 1) * ENEMY_SPACING_X) / 2
    start_y = ENEMY_START_Y
    
    # Cria inimigos em grelha
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x = start_x + col * ENEMY_SPACING_X
            y = start_y - row * ENEMY_SPACING_Y
            
            # Cria inimigo usando a função criar_entidade
            enemy = criar_entidade(x, y, "enemy")
            enemies.append(enemy)
            enemy_moves.append(1)

    state["enemies"] = enemies
    state["enemy_moves"] = enemy_moves
    state["enemy_bullets"] = [posicoes_existentes, dirs_existentes] if posicoes_existentes else []
    return
def restaurar_balas(state, lista_pos, tipo):
    print("[restaurar_balas] por implementar")
    if tipo == "enemy":
        state["enemy_bullets"] = [pos for pos in lista_pos]
    elif tipo == "player":
        state["player_bullets"] = [pos for pos in lista_pos]
    return

# =========================
# Handlers de tecla 
# =========================
def mover_esquerda_handler():
    print("[mover_esquerda_handler] por implementar")
    state = STATE
    player = state["player"]
    new_x = player.xcor() - PLAYER_SPEED
    if new_x < -BORDA_X: 
        new_x = -BORDA_X
    player.setx(new_x)


def mover_direita_handler():
    print("[mover_direita_handler] por implementar")
    state = STATE
    player = state["player"]
    new_x = player.xcor() + PLAYER_SPEED
    if new_x > BORDA_X: 
        new_x = BORDA_X
    player.setx(new_x)


def disparar_handler():
    print("[disparar_handler] por implementar")
    state = STATE
    player = state["player"]
    bullet = criar_bala(player.xcor(), player.ycor() + 10, "player")
    state["player_bullets"].append(bullet)

def gravar_handler():
    print("[gravar_handler] por implementar")
    global STATE
    guardar_estado_txt(SAVE_FILE, STATE)

def terminar_handler():
    print("[terminar_handler] por implementar")
    global STATE
    if STATE is not None:
        try:
            atualizar_highscores(STATE["files"]["highscores"], STATE["score"])
        except Exception as e:
            print("Erro ao atualizar highscores:", e)
        try:
            STATE["screen"].bye()
        except turtle.Terminator:
            pass
    sys.exit(0)

# =========================
# Atualizações e colisões
# =========================
def atualizar_balas_player(state):
    print("[atualizar_balas_player] por implementar")
    balas_player = state["player_bullets"]
    for mbp in balas_player: 
        mbp.forward(PLAYER_BULLET_SPEED)
      
def atualizar_balas_inimigos(state):
    print("[atualizar_balas_inimigos] por implementar")   
    balas_inimigas = state["enemy_bullets"]
    for mbi in balas_inimigas: 
        mbi.forward(ENEMY_BULLET_SPEED)
       
def atualizar_inimigos(state):
    print("[atualizar_inimigos] por implementar")
    enemies = state["enemies"]
    enemy_moves = state["enemy_moves"]
    
    for i, enemy in enumerate(enemies):
        # Move o inimigo para baixo constantemente
        enemy.sety(enemy.ycor() - ENEMY_FALL_SPEED)
        
        # Verifica se o inimigo deve se mover lateralmente (chance aleatória)
        if random.random() < ENEMY_DRIFT_CHANCE:
            # Move o inimigo na direção atual (independentemente)
            novo_x = enemy.xcor() + enemy_moves[i] * ENEMY_DRIFT_STEP
            
            # Verifica se o novo x está dentro dos limites
            if novo_x > BORDA_X - ENEMY_SIZE:
                novo_x = BORDA_X - ENEMY_SIZE
                enemy_moves[i] = -1  # Inverte para esquerda
            elif novo_x < -BORDA_X + ENEMY_SIZE:
                novo_x = -BORDA_X + ENEMY_SIZE
                enemy_moves[i] = 1  # Inverte para direita
            
            enemy.setx(novo_x)
        
        # O inimigo pode inverter a direção aleatoriamente
        if random.random() < ENEMY_INVERT_CHANCE:
            enemy_moves[i] *= -1
    
    state["enemies"] = enemies
    state["enemy_moves"] = enemy_moves
    return

def inimigos_disparam(state):
    print("[inimigos_disparam] por implementar")
    
def verificar_colisoes_player_bullets(state):
    print("[verificar_colisoes_player_bullets] por implementar")
    jogadores = state["player"]
    balas_inimigas = state["enemy_bullets"]
    
    
def verificar_colisoes_enemy_bullets(state):
    state = STATE
    player = state["player"]
    enemy_bullets = state["enemy_bullets"]
    for bullet in enemy_bullets: 
        distance = bullet.distance(player) 
        if distance < COLLISION_RADIUS: 
            bullet.hideturtle() 
            enemy_bullets.remove(bullet) 
            return True  
    return False 
           
def inimigo_chegou_ao_fundo(state):
    state = STATE
    enemies = state["enemies"]
    for enemy in enemies:
        if enemy.ycor() <= -BORDA_Y + ENEMY_SIZE:
            return True
    return False

def verificar_colisao_player_com_inimigos(state):
    
    state = STATE
    player = state["player"]
    enemies = state["enemies"]
    for enemy in enemies:
        dx = player.xcor() - enemy.xcor()
        dy = player.ycor() - enemy.ycor()
        distance = (dx**2 + dy**2)**0.5
        if distance < COLLISION_RADIUS:
            return True 
    return False 

# =========================
# Execução principal
# =========================
if __name__ == "__main__":
    # Pergunta inicial: carregar?
    filename = input("Carregar jogo? Se sim, escreva nome do ficheiro, senão carregue Return: ").strip()
    loaded = carregar_estado_txt(filename)

    # Ecrã
    screen = turtle.Screen()
    screen.title("Space Invaders IPRP")
    screen.bgcolor("black")
    screen.setup(width=LARGURA, height=ALTURA)
    screen.tracer(0)

    # Imagens obrigatórias
    for img in ["player.gif", "enemy.gif"]:
        if not os.path.exists(img):
            print("ERRO: imagem '" + img + "' não encontrada.")
            sys.exit(1)
        screen.addshape(img)

    # Estado base
    state = {
        "screen": screen,
        "player": None,
        "enemies": [],
        "enemy_moves": [],          
        "player_bullets": [],
        "enemy_bullets": [],
        "score": 0,
        "frame": 0,
        "files": {"highscores": HIGHSCORES_FILE, "save": SAVE_FILE}
    }

    # Construção inicial
    if loaded:
        print("[loaded=True] por implementar")
    else:
        print("New game!")
        state["player"] = criar_entidade(0, -350,"player")
        spawn_inimigos_em_grelha(state, None, None)

    # Variavel global para os keyboard key handlers
    STATE = state

    # Teclas
    screen.listen()
    screen.onkeypress(mover_esquerda_handler, "Left")
    screen.onkeypress(mover_direita_handler, "Right")
    screen.onkeypress(disparar_handler, "space")
    screen.onkeypress(gravar_handler, "g")
    screen.onkeypress(terminar_handler, "Escape")

    # Loop principal
    while True:
        atualizar_balas_player(STATE)
        atualizar_inimigos(STATE)
        inimigos_disparam(STATE)
        atualizar_balas_inimigos(STATE)
        verificar_colisoes_player_bullets(STATE)
        
        if verificar_colisao_player_com_inimigos(STATE):
            print("Colisão direta com inimigo! Game Over")
            terminar_handler()
        
        if verificar_colisoes_enemy_bullets(STATE):
            print("Atingido por inimigo! Game Over")
            terminar_handler()

        if inimigo_chegou_ao_fundo(STATE):
            print("Um inimigo chegou ao fundo! Game Over")
            terminar_handler()

        if len(STATE["enemies"]) == 0:
            print("Vitória! Todos os inimigos foram destruídos.")
            terminar_handler()

        STATE["frame"] += 1
        screen.update()
        time.sleep(0.016)
