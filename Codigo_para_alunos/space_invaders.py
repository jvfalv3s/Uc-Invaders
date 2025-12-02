import turtle
import random
import time
import os
import sys

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

#ao terminar uma implementacao usar o # no lugar do print

# =========================
# Top Resultados (Highscores)
# =========================
def ler_highscores(filename):
    # Ler o ficheiro de highscores e retornar uma lista de tuplos (nome, score).
    # Função robusta: ignora linhas mal formadas e não tenta fechar um ficheiro
    # que já foi fechado (removida chamada incorreta a f.close()).
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
    # Atualiza o ficheiro de highscores com o score atual se for um dos TOP_N.
    # Não assume que o ficheiro exista; ler_highscores já é robusto.
    if not filename:
        return
    highscores = ler_highscores(filename)
    if len(highscores) < TOP_N or score > highscores[-1][1]:
        nome = input("Novo Highscore! Insira o seu nome: ")
        highscores.append((nome, score))
        highscores = sorted(highscores, key=lambda x: x[1], reverse=True)[:TOP_N]
        # Abre em modo write (cria o ficheiro se necessário)
        with open(filename, "w") as f:
            for nome, sc in highscores:
                f.write(f"{nome} {sc}\n")

# =========================
# Guardar / Carregar estado (texto)
# =========================
def guardar_estado_txt(filename, state):
    #print("[guardar_estado_txt] por implementar")
    #guardar dados no ficheiro de texto savegame.txt ao pressionar a tecla g
    #criar um ficheiro com o nome filename e guardar os dados do state nele
    with open(filename, "w") as f:
        #guardar posicao do jogador
        player = state["player"]
        f.write(f"PLAYER {player.xcor()} {player.ycor()}\n")
        
        #guardar posicoes dos inimigos
        enemies = state["enemies"]
        f.write("ENEMIES\n")
        for enemy in enemies:
            f.write(f"{enemy.xcor()} {enemy.ycor()}\n")

        #guardar movimentos dos inimigos
        enemy_moves = state["enemy_moves"]
        f.write("ENEMY_MOVES\n")
        for move in enemy_moves:
            f.write(f"{move}\n")

        #guardar balas do jogador
        player_bullets = state["player_bullets"]
        f.write("PLAYER_BULLETS\n")
        for bullet in player_bullets:
            f.write(f"{bullet.xcor()} {bullet.ycor()}\n")
        
        #guardar balas dos inimigos
        enemy_bullets = state["enemy_bullets"]
        f.write("ENEMY_BULLETS\n")
        for bullet in enemy_bullets:
            f.write(f"{bullet.xcor()} {bullet.ycor()}\n")

    # O 'with' já fecha o ficheiro; não é necessário chamar f.close()

def carregar_estado_txt(filename):
    #print("[carregar_estado_txt] por implementar")
    #carregar dados do ficheiro de texto savegame.txt ao iniciar o jogo
    #se o ficheiro nao existir, retorna False
    if not filename or not os.path.exists(filename):
        return False
    else:
        with open(filename, "r") as f:
            lines = f.readlines()
        state = STATE
        enemies = []
        enemy_moves = []
        player_bullets = []
        enemy_bullets = []
        section = None

        for line in lines:
            line = line.strip()
            if line.startswith("PLAYER"):
                _, x, y = line.split()
                state["player"] = criar_entidade(float(x), float(y), "player")
            elif line == "ENEMIES":
                section = "ENEMIES"
            elif line == "ENEMY_MOVES":
                section = "ENEMY_MOVES"
            elif line == "PLAYER_BULLETS":
                section = "PLAYER_BULLETS"
            elif line == "ENEMY_BULLETS":
                section = "ENEMY_BULLETS"
            else:
                if section == "ENEMIES":
                    x, y = map(float, line.split())
                    enemy = criar_entidade(x, y, "enemy")
                    enemies.append(enemy)
                elif section == "ENEMY_MOVES":
                    move = int(line)
                    enemy_moves.append(move)
                elif section == "PLAYER_BULLETS":
                    x, y = map(float, line.split())
                    bullet = criar_bala(x, y, "player")
                    player_bullets.append(bullet)
                elif section == "ENEMY_BULLETS":
                    x, y = map(float, line.split())
                    bullet = criar_bala(x, y, "enemy")
                    enemy_bullets.append(bullet)
        state["enemies"] = enemies
        state["enemy_moves"] = enemy_moves
        state["player_bullets"] = player_bullets
        state["enemy_bullets"] = enemy_bullets  
    return True

# =========================
# Criação de entidades (jogador, inimigo e balas)
# =========================
def criar_entidade(x,y, tipo="enemy"):
    t = turtle.Turtle(visible=False)
    t.shape("player.gif" if tipo == "player" else "enemy.gif")
    if tipo == "enemy":
        t.setheading(-90)
    t.penup()
    t.goto(x,y)

    t.showturtle()
    return t 

def criar_bala(x, y, tipo):
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
    #print("[restaurar_balas] por implementar")
    #restaura balas a partir de lista de posições
    if tipo == "enemy":
        state["enemy_bullets"] = [pos for pos in lista_pos]
    elif tipo == "player":
        state["player_bullets"] = [pos for pos in lista_pos]
    return

# =========================
# Handlers de tecla 
# =========================
def mover_esquerda_handler():
    state = STATE
    player = state["player"]
    new_x = player.xcor() - PLAYER_SPEED
    if new_x < -BORDA_X:
        new_x = -BORDA_X
    player.setx(new_x)

def mover_direita_handler():
    state = STATE
    player = state["player"]
    new_x = player.xcor() + PLAYER_SPEED
    if new_x > BORDA_X:
        new_x = BORDA_X
    player.setx(new_x)

def disparar_handler():
    #criar uma bala e por na lista de balas do jogador
    state = STATE
    player = state["player"]
    bullet = criar_bala(player.xcor(), player.ycor() + 10, "player")
    state["player_bullets"].append(bullet)

def gravar_handler():
    print("[gravar_handler] por implementar")
    #ao precionar a tecla g, grava TODOS os dados do estado atual para um ficheiro de texto?
    guardar_estado_txt(SAVE_FILE, STATE)

def terminar_handler():
    # Fecha o jogo e atualiza os highscores antes de sair.
    # Usa a variável global STATE corretamente e trata exceções.
    global STATE
    if STATE is not None:
        # Tenta atualizar highscores (cria o ficheiro se necessário)
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
    #print("[atualizar_balas_player] por implementar")
    for bullet in state["player_bullets"]:
        #atualiza a posicao da bala com o speed + foward
        bullet.forward(PLAYER_BULLET_SPEED)
        #se a bala sair do ecra, remove-a da lista e esconde-a
        if bullet.ycor() > BORDA_Y:
            bullet.hideturtle()
            state["player_bullets"].remove(bullet)


def atualizar_balas_inimigos(state):
    #print("[atualizar_balas_inimigos] por implementar")
    for bullet in state["enemy_bullets"]:
        # Atualiza a posição da bala com o speed + forward
        bullet.forward(ENEMY_BULLET_SPEED)
        # Se a bala sair do ecrã, remove-a da lista e esconde-a
        if bullet.ycor() < -BORDA_Y:
            bullet.hideturtle()
            state["enemy_bullets"].remove(bullet)

def atualizar_inimigos(state):
    #print("[atualizar_inimigos] por implementar")
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
    #print("[inimigos_disparam] por implementar")
    enemies = state["enemies"]
    for enemy in enemies:
        if random.random() < ENEMY_FIRE_PROB:
            bullet = criar_bala(enemy.xcor(), enemy.ycor() - 10, "enemy")
            state["enemy_bullets"].append(bullet)
    return

def verificar_colisoes_player_bullets(state):
    #print("[verificar_colisoes_player_bullets] por implementar")
    #verifica se alguma bala do jogador colidiu com algum inimigo
    state = STATE
    player_bullets = state["player_bullets"]
    enemies = state["enemies"]
    for bullet in player_bullets: #verifica cada bala do jogador
        for enemy in enemies: #verifica cada inimigo
            distance = bullet.distance(enemy) #calcula a distancia entre a bala e o inimigo
            if distance < COLLISION_RADIUS: # se a distancia entre a bala e o inimigo for menor que o raio de colisao
                # Colisão detectada
                bullet.hideturtle() #esconde a bala
                enemy.hideturtle() #esconde o inimigo
                state["score"] += 10  # Incrementa a pontuação
                player_bullets.remove(bullet) #remove a bala da lista de balas do jogador
                enemies.remove(enemy) #remove o inimigo da lista de inimigos
                return  # Sai da função após a colisão para evitar erros


def verificar_colisoes_enemy_bullets(state):
    #print("[verificar_colisoes_enemy_bullets] por implementar")
    state = STATE
    player = state["player"]
    enemy_bullets = state["enemy_bullets"]
    for bullet in enemy_bullets: #verifica cada bala inimiga
        distance = bullet.distance(player) #calcula a distancia entre a bala e o jogador
        if distance < COLLISION_RADIUS: # se a distancia entre a bala e o jogador for menor que o raio de colisao
            # Colisão detectada
            bullet.hideturtle() #esconde a bala
            enemy_bullets.remove(bullet) #remove a bala da lista de balas inimigas
            return True  # Retorna True se houve colisão
    return False  # Retorna False se não houve colisão

def inimigo_chegou_ao_fundo(state):
    #print("[inimigo_chegou_ao_fundo] por implementar")
    state = STATE
    enemies = state["enemies"]
    for enemy in enemies:
        if enemy.ycor() <= -BORDA_Y + ENEMY_SIZE:
            return True
    return False

def verificar_colisao_player_com_inimigos(state):
    #print("[verificar_colisao_player_com_inimigos] por implementar")
    state = STATE
    player = state["player"]
    enemies = state["enemies"]
    for enemy in enemies:
        distance = enemy.distance(player)
        if distance < COLLISION_RADIUS:
            return True  # Retorna True se houve colisão
    return False  # Retorna False se não houve colisão

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
        #modificar o STATE com os dados carregados
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
