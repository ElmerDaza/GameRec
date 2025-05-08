import pygame
import sys
import random


pygame.mixer.pre_init(44100, -16, 2, 512)
# Inicializar PyGame
pygame.init()


# Sonidos
sonido_disparo = pygame.mixer.Sound("sonidos/golpeconraqueta.wav")
perdiste =pygame.mixer.Sound("sonidos/perdiste.wav")
pygame.mixer.music.load("sonidos/cancionJuegoTenis.wav")
sonido_disparo.set_volume(0.1)
# Configuración de la pantalla
ancho = 800
alto = 600
pantalla = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption("Game rec")

# Colores (RGB)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)
VERDE =(160, 200, 120)
CAFE=(168, 101, 35)
CAFE_CLARO=(255, 165, 93)
PURPLE=(58, 89, 209)
AZUL= (61, 144, 215)
GRIS= (219, 219, 219)
AMARILLO= (252, 242, 89)

# Opciones config
volumen_opciones = ["Bajo", "Medio", "Alto"]
dificultad_opciones = ["Fácil", "Media", "Difícil"]
volumen_idx = 1
dificultad_idx = 0

# Fuente
fuente = pygame.font.SysFont(None, 60)
fuente_2 = pygame.font.SysFont(None, 20)
fuente_3 = pygame.font.SysFont(None, 35)

#puntuacion
score = 0
mejor_puntuacion=0

#ejecucion del juego
ejecutando = False
# Bucle principal del menú
en_menu = True
#bucle config
confi=True

#colicion de rectangulos
def colicion_rec(rectangulo_1, rectangulo_2):
    return rectangulo_1.colliderect(rectangulo_2)

#colicion con el pryectil
def colision_circulo_rect(circulo_pos, radio, rect):
    # Encuentra el punto más cercano del rectángulo al centro del círculo
    cx, cy = circulo_pos
    rx = max(rect.left, min(cx, rect.right))
    ry = max(rect.top, min(cy, rect.bottom))
    distancia = ((cx - rx)**2 + (cy - ry)**2) ** 0.5
    return distancia < radio


def fin():
    global en_menu, ejecutando, mejor_puntuacion, score
    en_menu = True
    ejecutando = False
    if mejor_puntuacion< score:
        mejor_puntuacion=score
    pygame.mixer.music.stop()
    perdiste.play()
    menu()



# Botones
def dibujar_boton(texto, x, y, ancho, alto, color, color_hover, accion=None, fuente = fuente):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + ancho and y < mouse[1] < y + alto:
        pygame.draw.rect(pantalla, color_hover, (x, y, ancho, alto))
        if click[0] == 1 and accion:
            accion()
    else:
        pygame.draw.rect(pantalla, color, (x, y, ancho, alto))

    texto_superficie = fuente.render(texto, True, NEGRO)
    texto_rect = texto_superficie.get_rect(center=(x + ancho // 2, y + alto // 2))
    pantalla.blit(texto_superficie, texto_rect)
#texto config
def dibujar_texto(texto, x, y, seleccionado=False, fuente=fuente):
    color = ROJO if seleccionado else NEGRO
    texto_render = fuente.render(texto, True, color)
    pantalla.blit(texto_render, (x, y))
# Acciones
def jugar():
    global en_menu, ejecutando,score
    en_menu = False
    ejecutando = True
    pygame.mixer.music.play(-1)  # -1 significa que se repite infinitamente
    pygame.mixer.music.set_volume(0.5)  # Volumen entre 0.0 y 1.0
    score=0
    juego()


def salir():
    pygame.quit()
    sys.exit()

def btn_vol():
    global volumen_idx
    volumen_idx = (volumen_idx + 1) % len(volumen_opciones)
def btn_dif(): 
    global dificultad_idx 
    dificultad_idx = (dificultad_idx + 1) % len(dificultad_opciones)

def menu():
    while en_menu:
        pantalla.fill(BLANCO)

        # Título
        titulo = fuente.render("¡Bienvenido al Juego!", True, AZUL)
        pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 100))
        instrucciones = fuente_2.render("¡Tu eres el cuadro rojo!, dispara con la tecla espacio, muevete y no dejes que nada te toque", True, ROJO)
        pantalla.blit(instrucciones, (ancho // 2 - instrucciones.get_width() // 2, alto-120))
        score = fuente_3.render(f"Mejor puntuacion: {mejor_puntuacion}", True, NEGRO)
        pantalla.blit(score, (20, 20))

        # Botones
        dibujar_boton("Jugar", 300, 200, 200, 60, GRIS, AZUL, jugar)
        dibujar_boton("Config",300,275,200,60,GRIS,AZUL, config)
        dibujar_boton("Salir", 300, 350, 200, 60, GRIS, ROJO, salir)
        

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                salir()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def config():
    global volumen_idx, dificultad_idx
    
    confi=True
    while confi:
        pantalla.fill(BLANCO)

        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    confi = False
                    menu()
                elif evento.key == pygame.K_RIGHT:
                    volumen_idx = (volumen_idx + 1) % len(volumen_opciones)
                elif evento.key == pygame.K_LEFT:
                    volumen_idx = (volumen_idx - 1) % len(volumen_opciones)
                elif evento.key == pygame.K_DOWN:
                    dificultad_idx = (dificultad_idx + 1) % len(dificultad_opciones)
                elif evento.key == pygame.K_UP:
                    dificultad_idx = (dificultad_idx - 1) % len(dificultad_opciones)

        # Dibujar textos
        dibujar_texto("CONFIGURACIÓN", 200, 50)
        dibujar_texto(f"Volumen: {volumen_opciones[volumen_idx]}", 250, 200, True,fuente_3)
        dibujar_texto(f"Dificultad: {dificultad_opciones[dificultad_idx]}", 250, 300, True,fuente_3)
        dibujar_texto("Presiona ESC para volver al menú", 200, 500,fuente=fuente_2)
        dibujar_boton(">",450,190,35,35,GRIS,VERDE,btn_vol)
        dibujar_boton(">",450,290,35,35,GRIS,VERDE,btn_dif)
        dibujar_boton("X",20,20,40,40,GRIS,ROJO,fin,fuente_3)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

# Bucle principal del juego
def juego():
    global ejecutando, score, mejor_puntuacion, dificultad_idx
    # Posición inicial del jugador
    jugador_pos = [2, alto-120]
    jugador_tam = 50
    velocidad = 5

    #proyectilES
    proyectil_1_pos=[ancho,0]
    numero = random.randint(ancho/2, ancho)
    proyectil_2_pos=[numero,0]
    ajuste=random.randint(50, 200)
    proyectil_3_pos=[ancho+ajuste,0]
    proyectil_tam=10

    #enemigos
    enemigos =[]
    frecuencia_enemigos = 1000
    


    match dificultad_idx:
        case 0:
            pro_velocidad = 3
            pro_velocidad_2 = random.randint(2, 6)
            velocidad_enemigo = 3

        case 1:
            pro_velocidad = 7
            pro_velocidad_2 = random.randint(5, 10)
            velocidad_enemigo = 6

        case 2:
            pro_velocidad = 10
            pro_velocidad_2 = random.randint(10, 15)
            velocidad_enemigo = 7

        case _:
            print("Opción no válida")

    #lineas 1
    line_1=[20,alto-40,0,alto-10]
    line_2=[40,alto-40,20,alto-10]
    line_3=[60,alto-40,40,alto-10]
    line_vel=1

    # Disparos
    velocidad_disparo = 12
    disparos = []  # Lista para almacenar disparos activos
    # milisegundos (1000 ms / 2 = 500 ms por disparo = 2 por segundo)
    frecuencia_disparo = 250  
    # Tiempo del último disparo
    ultimo_disparo = 0        

    # Reloj para controlar FPS
    reloj = pygame.time.Clock()
    
    while ejecutando:
        if score>=1500:
            dificultad_idx=1
        if score>=3000:
            dificultad_idx=2
        
        # Procesar eventos
        for evento in pygame.event.get():
            # Cerrar la ventana
            if evento.type == pygame.QUIT:
                ejecutando = False
        
        # Capturar teclas presionadas
        teclas = pygame.key.get_pressed()
        
        # Mover el jugador
        if teclas[pygame.K_LEFT]:
            jugador_pos[0] -= velocidad
        if teclas[pygame.K_RIGHT]:
            jugador_pos[0] += velocidad

        tiempo_actual = pygame.time.get_ticks()
        # Verifica si ha pasado suficiente tiempo desde el último disparo
        if teclas[pygame.K_SPACE] and tiempo_actual - ultimo_disparo >= frecuencia_disparo:
            disparo_nuevo = [jugador_pos[0] + jugador_tam, jugador_pos[1] + jugador_tam//2]
            disparos.append(disparo_nuevo)
            ultimo_disparo = tiempo_actual
        """if teclas[pygame.K_UP]:
            jugador_pos[1] -= velocidad
        if teclas[pygame.K_DOWN]:
            jugador_pos[1] += velocidad"""

        
        #crear enemigos
        if enemigos == []:
            
            for i in range(0,random.randint(1, 3)):
                enemi = [ancho+jugador_tam, (alto-120)-(len(enemigos)*jugador_tam)]
                enemigos.append(enemi)
            

        #mover proyectiles
        proyectil_1_pos[0]-=pro_velocidad
        proyectil_1_pos[1]+=pro_velocidad
        proyectil_2_pos[1]+=pro_velocidad_2
        proyectil_2_pos[0]-=pro_velocidad_2
        proyectil_3_pos[0]-=pro_velocidad-1
        proyectil_3_pos[1]+=pro_velocidad-1

        
        # Mantener al jugador dentro de los límites
        jugador_pos[0] = max(0, min(jugador_pos[0], ancho - jugador_tam))
        jugador_pos[1] = max(0, min(jugador_pos[1], alto - jugador_tam))

        #mover lineas del suelo
        line_1[0]-=line_vel
        line_1[2]-=line_vel
        line_2[0]-=line_vel
        line_2[2]-=line_vel
        line_3[0]-=line_vel
        line_3[2]-=line_vel

        


        # Limpiar pantalla
        pantalla.fill(NEGRO)
        #score
        titulo = fuente.render(f"Score: {score}", True, GRIS)
        pantalla.blit(titulo, (ancho // 2 - titulo.get_width() // 2, 20))
        titulo = fuente.render(f"{dificultad_opciones[dificultad_idx]}", True, GRIS)
        pantalla.blit(titulo, (20, 20))


        # Mover y dibujar disparos
        for disparo in disparos[:]:  
            disparo[0] += velocidad_disparo
            pygame.draw.rect(pantalla, ROJO, (disparo[0], disparo[1], 10, 5))
            if disparo[0] > ancho:
                disparos.remove(disparo)
        #mover y dibujar enemigos
        for enemigo in enemigos[:]:
            enemigo[0]-=velocidad_enemigo
            pygame.draw.rect(pantalla,PURPLE,(enemigo[0],enemigo[1],jugador_tam, jugador_tam))
        
        # Dibujar al jugador (un cuadrado rojo)
        pygame.draw.rect(pantalla, ROJO, 
                        (jugador_pos[0], jugador_pos[1], jugador_tam, jugador_tam))
        
        # dibujar proyectiles
        if(proyectil_1_pos[1]< alto-20):
            pygame.draw.circle(pantalla,ROJO,(proyectil_1_pos[0]+7,proyectil_1_pos[1]-7),proyectil_tam-4,0)
            pygame.draw.circle(pantalla,AMARILLO,(proyectil_1_pos[0]+4,proyectil_1_pos[1]-4),proyectil_tam-2,0)
            pygame.draw.circle(pantalla,BLANCO,(proyectil_1_pos[0],proyectil_1_pos[1]),proyectil_tam,0)
            
            
        else:
            proyectil_1_pos=[ancho,0]
            score+=1
        if(proyectil_2_pos[1]< alto-20):
            pygame.draw.circle(pantalla,ROJO,(proyectil_2_pos[0]+7,proyectil_2_pos[1]-7),proyectil_tam-4,0)
            pygame.draw.circle(pantalla,AMARILLO,(proyectil_2_pos[0]+4,proyectil_2_pos[1]-4),proyectil_tam-2,0)
            pygame.draw.circle(pantalla,BLANCO,(proyectil_2_pos[0],proyectil_2_pos[1]),proyectil_tam,0)
        else:
            proyectil_2_pos=[random.randint(ancho/2, ancho),0]
            pro_velocidad_2 = random.randint(2, 6)
            score+=1
        if(proyectil_3_pos[1]< alto-20):
            pygame.draw.circle(pantalla,ROJO,(proyectil_3_pos[0]+7,proyectil_3_pos[1]-7),proyectil_tam-4,0)
            pygame.draw.circle(pantalla,AMARILLO,(proyectil_3_pos[0]+4,proyectil_3_pos[1]-4),proyectil_tam-2,0)
            pygame.draw.circle(pantalla,BLANCO,(proyectil_3_pos[0],proyectil_3_pos[1]),proyectil_tam,0)
        else:
            proyectil_3_pos=[ancho+ajuste,0]
            match dificultad_idx:
                case 0:
                    pro_velocidad = random.randint(2, 6)
                case 1:
                    pro_velocidad = random.randint(5, 7)
                case 2:
                    pro_velocidad = random.randint(7, 10)
                case _:
                    print("Opción no válida")
            score+=1
        
        
        #dibujar suelo
        pygame.draw.rect(pantalla, CAFE, (0, alto-50, ancho, 50))
        pygame.draw.rect(pantalla, VERDE, (0, alto-70, ancho, 20))
        #primera fila de lineas
        pygame.draw.line(pantalla, CAFE_CLARO,(line_1[0],line_1[1]),(line_1[2],line_1[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_2[0],line_2[1]),(line_2[2],line_2[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_3[0],line_3[1]),(line_3[2],line_3[3]),5)
        #segunda fila de lineas
        pygame.draw.line(pantalla, CAFE_CLARO,(line_1[0]+150,line_1[1]),(line_1[2]+150,line_1[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_2[0]+150,line_2[1]),(line_2[2]+150,line_2[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_3[0]+150,line_3[1]),(line_3[2]+150,line_3[3]),5)
        #tercera fila de lineas
        pygame.draw.line(pantalla, CAFE_CLARO,(line_1[0]+300,line_1[1]),(line_1[2]+300,line_1[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_2[0]+300,line_2[1]),(line_2[2]+300,line_2[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_3[0]+300,line_3[1]),(line_3[2]+300,line_3[3]),5)

        #cuarta fila de lineas
        pygame.draw.line(pantalla, CAFE_CLARO,(line_1[0]+450,line_1[1]),(line_1[2]+450,line_1[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_2[0]+450,line_2[1]),(line_2[2]+450,line_2[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_3[0]+450,line_3[1]),(line_3[2]+450,line_3[3]),5)
        #quinta fila de lineas
        pygame.draw.line(pantalla, CAFE_CLARO,(line_1[0]+600,line_1[1]),(line_1[2]+600,line_1[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_2[0]+600,line_2[1]),(line_2[2]+600,line_2[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_3[0]+600,line_3[1]),(line_3[2]+600,line_3[3]),5)
        #SEXTA fila de lineas
        pygame.draw.line(pantalla, CAFE_CLARO,(line_1[0]+750,line_1[1]),(line_1[2]+750,line_1[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_2[0]+750,line_2[1]),(line_2[2]+750,line_2[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_3[0]+750,line_3[1]),(line_3[2]+750,line_3[3]),5)
        #SEPTIMA fila de lineas
        pygame.draw.line(pantalla, CAFE_CLARO,(line_1[0]+900,line_1[1]),(line_1[2]+900,line_1[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_2[0]+900,line_2[1]),(line_2[2]+900,line_2[3]),5)
        pygame.draw.line(pantalla, CAFE_CLARO,(line_3[0]+900,line_3[1]),(line_3[2]+900,line_3[3]),5)

        #repetir el bucle de las lineas
        if line_1[2]==-150:
            line_1=[20,alto-40,0,alto-10]
            line_2=[40,alto-40,20,alto-10]
            line_3=[60,alto-40,40,alto-10]

        #verificar colicion con los enemigos
        rect = pygame.Rect(jugador_pos[0], jugador_pos[1], jugador_tam, jugador_tam)
        for i in enemigos[:]:   
            rect_2= pygame.Rect(i[0], i[1], jugador_tam, jugador_tam)
            if colicion_rec(rect, rect_2):
                fin()

        #verificar colicion con los disparos
        rect = pygame.Rect(enemigos[0][0], enemigos[0][1], jugador_tam, jugador_tam)
        for i in disparos[:]:   
            rect_2= pygame.Rect(i[0], i[1], jugador_tam, jugador_tam)
            if colicion_rec(rect, rect_2):
                sonido_disparo.play()
                for i in range(0,len(enemigos)):
                    if enemigos[i][1]==480:
                        enemigos.pop(i)
                        score+=5
                        break
        #decender enemigos      
        if enemigos != [] and enemigos[0][1]<480:
            for enemigo in enemigos:
                enemigo[1]+= 2

        #colicion con los proyectiles
        rect = pygame.Rect(jugador_pos[0], jugador_pos[1], jugador_tam, jugador_tam)
        if colision_circulo_rect(proyectil_1_pos, proyectil_tam-3, rect):
            fin()
        if colision_circulo_rect(proyectil_2_pos, proyectil_tam-3, rect):
            fin()
        if colision_circulo_rect(proyectil_3_pos, proyectil_tam-3, rect):
            fin()

        # Actualizar pantalla
        pygame.display.flip()
        
        # Controlar la velocidad del juego (60 FPS)
        reloj.tick(60)

menu()