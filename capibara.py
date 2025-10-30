import pygame
import sys
import random
import os
from datetime import datetime
import mysql.connector


def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # tu contraseña si tenés
        database="juego_colisiones"
    )

# 🧑‍💻 Insertar usuario
def guardar_usuario(id_usuario, usuario, contraseña):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="juego_colisiones"
    )
    cursor = conn.cursor()

    # Verificar si el ID ya existe
    cursor.execute("SELECT COUNT(*) FROM registro_usuario WHERE id_usuario = %s", (id_usuario,))
    existe = cursor.fetchone()[0]

    if existe == 0:
        sql = "INSERT INTO registro_usuario (id_usuario, usuario, contraseña) VALUES (%s, %s, %s)"
        cursor.execute(sql, (id_usuario, usuario, contraseña))
        conn.commit()
        print(f"✅ Usuario {usuario} guardado en la base de datos.")
    else:
        print(f"⚠️ El usuario con ID {id_usuario} ya existe. No se insertó.")

    cursor.close()
    conn.close()

# 🎮 Insertar partida
def guardar_partida(id_partida, id_usuario, fecha, numero_partida, nivel):
    conn = conectar()
    cursor = conn.cursor()
    sql = "INSERT INTO registro_partidas (id_partida, id_usuario, fecha, numero_partida, nivel) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(sql, (id_partida, id_usuario, fecha, numero_partida, nivel))
    conn.commit()
    cursor.close()
    conn.close()

# 💥 Insertar colisión
def guardar_colision(id_usuario, id_partida, botella_vidrio, papel_reciclable, botella_plastico, residuo_electronico, fecha_hora):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="juego_colisiones"
    )
    cursor = conn.cursor()
    sql = """INSERT INTO registro_colisiones 
             (id_usuario, id_partida, botella_vidrio, papel_reciclable, botella_plastico, residuo_electronico, fecha_hora) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    valores = (id_usuario, id_partida, botella_vidrio, papel_reciclable, botella_plastico, residuo_electronico, fecha_hora)

    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()

# 📍 Insertar coordenada
def guardar_coordenada(id_partida, id_usuario, objeto_colisionador, objeto_colisionado, x, y, fecha_hora):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="juego_colisiones"
    )
    cursor = conn.cursor()
    sql = """INSERT INTO registro_coordenadas 
             (id_partida, id_usuario, objeto_colisionador, objeto_colisionado, x, y, fecha_hora) 
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""
    valores = (id_partida, id_usuario, objeto_colisionador, objeto_colisionado, x, y, fecha_hora)
    cursor.execute(sql, valores)
    conn.commit()
    cursor.close()
    conn.close()



#-----------------------------------------------------JUEGO---------------------------------------------------------
# Funcion para mostrar el menu principal
def menu_principal(pantalla, ANCHO, ALTO):
    fuente = pygame.font.SysFont("Nintendo DS BIOS", 40)
    opciones = ["Jugar", "Multiplayer", "Información", "Créditos","Salir"]
    seleccion = 0
    reloj = pygame.time.Clock()

    # 🖼️ Fondo del menú
    fondo = pygame.image.load("fondo_menu.png").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    # 🎵 Música del menú
    pygame.mixer.music.load("musica_menu.wav")
    pygame.mixer.music.play(-1)

    ejecutando = True
    while ejecutando:
        pantalla.blit(fondo, (0, 0))

        for i, texto in enumerate(opciones):
            color = (255, 255, 255) if i == seleccion else (180, 180, 180)
            render = fuente.render(texto, True, color)
            pantalla.blit(render, (ANCHO//2 - 100, 200 + i * 60))

        pygame.display.flip()
        reloj.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(opciones)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(opciones)
                elif evento.key == pygame.K_RETURN:
                    if opciones[seleccion] == "Jugar":
                        pygame.mixer.music.stop()
                        return "jugar"
                    elif opciones[seleccion] == "Multiplayer":
                        print("Multiplayer aún no implementado")
                    elif opciones[seleccion] == "Información":
                        pygame.mixer.music.stop()
                        return "informacion"
                    elif opciones[seleccion] == "Créditos":
                        pygame.mixer.music.stop()
                        mostrar_creditos(pantalla)
                    elif opciones[seleccion] == "Salir":
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

# Funcion para mostrar la informacion del reciclaje
def mostrar_informacion(pantalla):
    ANCHO, ALTO = pantalla.get_width(), pantalla.get_height()
    fuente = pygame.font.SysFont("Nintendo DS BIOS", 34)

    iconos = [
    pygame.image.load("papel_reciclable.png"),
    pygame.image.load("botella_vidrio.png"),
    pygame.image.load("botella_plastico.png"),
    pygame.image.load("residuo_electronico.png"),
    pygame.image.load("residuo_no_reciclable.png"),
    pygame.image.load("tacho_reciclaje.png")
    ]
    iconos = [pygame.transform.scale(img, (60, 60)) for img in iconos]

    reloj = pygame.time.Clock()

    # 🖼️ Cargar imagen de fondo
    fondo = pygame.image.load("fondo_info.png").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    # 🎵 Reproducir música
    pygame.mixer.music.load("musica_info.wav")
    pygame.mixer.music.play(-1)  # -1 = loop infinito

    textos = [
        "Papel: reciclable si está limpio y seco.",
        "Vidrio: reciclable infinitas veces.",
        "Plástico: reciclable, pero tarda siglos en degradarse.",
        "Electrónicos: reciclables en puntos especiales.",
        "No reciclables: pañales, bolsas metalizadas, papel sucio.",
        "Consejo: separá los residuos en origen para facilitar el reciclaje."
    ]

    ejecutando = True
    while ejecutando:
        pantalla.blit(fondo, (0, 0))  # 🖼️ Dibujar fondo

        for i, texto in enumerate(textos):
            y = 80 + i * 60  # Espaciado vertical
            pantalla.blit(iconos[i], (80, y))  # Ícono a la izquierda
            render = fuente.render(texto, True, (0, 0, 0))
            pantalla.blit(render, (140, y + 5))  # Texto alineado a la derecha del ícono


        render_volver = fuente.render("Presioná ESC para volver", True, (200, 200, 200))
        pantalla.blit(render_volver, (50, ALTO - 40))

        pygame.display.flip()
        reloj.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()  # 🛑 Detener música al salir
                ejecutando = False

# Funcion para mostrar los creditos del juego
def mostrar_creditos(pantalla):
    ANCHO, ALTO = pantalla.get_width(), pantalla.get_height()
    fuente_titulo = pygame.font.SysFont("Nintendo DS BIOS", 48)
    fuente_texto = pygame.font.SysFont("Nintendo DS BIOS", 34)
    reloj = pygame.time.Clock()

    # 🖼️ Fondo
    fondo = pygame.image.load("fondo_creditos.png").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

    # 🎵 Música
    pygame.mixer.music.load("musica_creditos.wav")
    pygame.mixer.music.play(-1)

    textos = [
        "Juego de Reciclaje Educativo",
        "Desarrollado por Matías y Tatiana",
        "Diseño de sprites y HUD: Matías y Tatiana",
        "Integración de IA y lógica: Matías y Tatiana",
        "Música generada en Sonic Pi",
        "Asistencia técnica: Copilot",
        "Gracias por jugar "
    ]

    ejecutando = True
    while ejecutando:
        pantalla.blit(fondo, (0, 0))

        for i, texto in enumerate(textos):
            render = fuente_texto.render(texto, True, (2,0,19))
            x = ANCHO // 2 - render.get_width() // 2
            y = 100 + i * 50
            pantalla.blit(render, (x, y))

        titulo = fuente_titulo.render("Créditos", True, (128,128,128))
        pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 30))

        volver = fuente_texto.render("Presioná ESC para volver", True, (200, 200, 200))
        pantalla.blit(volver, (ANCHO // 2 - volver.get_width() // 2, ALTO - 40))

        pygame.display.flip()
        reloj.tick(30)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                pygame.mixer.music.stop()
                ejecutando = False

# Funcion para mostrar la pantalla de inicio
def pantalla_inicio(pantalla, ANCHO, ALTO):
    fuente = pygame.font.SysFont("Nintendo DS BIOS", 32)
    reloj = pygame.time.Clock()

    usuario = ""
    contraseña = ""
    activo_usuario = True
    mensaje = ""

    # 🎵 Música de fondo
    pygame.mixer.music.load("musica_inicio.wav")
    pygame.mixer.music.play(-1)

    # 🖼️ Fondo
    fondo = pygame.image.load("fondo_inicio.png").convert()
    fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))
    # 🐾 Logo del capibara
    logo_capibara = pygame.image.load("tacho_reciclaje.png").convert_alpha()
    logo_capibara = pygame.transform.scale(logo_capibara, (100, 100))  # Ajustá tamaño si querés

    # 🔘 Campos
    campo_usuario = pygame.Rect(ANCHO//2 - 100, 250, 300, 40)
    campo_contraseña = pygame.Rect(ANCHO//2 - 100, 310, 300, 40)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if evento.key in [pygame.K_UP, pygame.K_DOWN]:
                    activo_usuario = not activo_usuario
                elif evento.key == pygame.K_BACKSPACE:
                    if activo_usuario:
                        usuario = usuario[:-1]
                    else:
                        contraseña = contraseña[:-1]
                elif evento.key == pygame.K_RETURN:
                    id_usuario = verificar_o_crear_usuario(usuario, contraseña)
                    if id_usuario:
                        pygame.mixer.music.stop()
                        return id_usuario, usuario, contraseña
                    else:
                        mensaje = "❌ Usuario o contraseña incorrectos"
                        usuario = ""
                        contraseña = ""
                elif evento.key == pygame.K_ESCAPE:
                    pygame.mixer.music.stop()
                    return None  # Volver al menú principal
                else:
                    letra = evento.unicode
                    if activo_usuario:
                        usuario += letra
                    else:
                        contraseña += letra

        pantalla.blit(fondo, (0, 0))
        pos_logo_x = 600
        pos_logo_y = 120
        pantalla.blit(logo_capibara, (pos_logo_x, pos_logo_y))
        


        # 🔲 Campos con borde activo
        color_usuario = (0, 120, 255) if activo_usuario else (180, 180, 180)
        color_contraseña = (0, 120, 255) if not activo_usuario else (180, 180, 180)

        pygame.draw.rect(pantalla, color_usuario, campo_usuario, 2)
        pygame.draw.rect(pantalla, color_contraseña, campo_contraseña, 2)

        texto_usuario = fuente.render(usuario, True, (0, 0, 0))
        texto_contraseña = fuente.render("*" * len(contraseña), True, (0, 0, 0))
        pantalla.blit(texto_usuario, (campo_usuario.x + 10, campo_usuario.y + 5))
        pantalla.blit(texto_contraseña, (campo_contraseña.x + 10, campo_contraseña.y + 5))

        # 📝 Etiquetas
        etiqueta_usuario = fuente.render("Usuario:", True, (0, 0, 0))
        etiqueta_contraseña = fuente.render("Contraseña:", True, (0, 0, 0))
        pantalla.blit(etiqueta_usuario, (campo_usuario.x - 100, campo_usuario.y))
        pantalla.blit(etiqueta_contraseña, (campo_contraseña.x - 140, campo_contraseña.y))

        # 🔘 Indicaciones
        pantalla.blit(fuente.render("Usá flechas para seleccionar campo", True, (0, 0, 0)), (ANCHO//2 - 210, 380))
        pantalla.blit(fuente.render("Presioná ENTER para ingresar", True, (0, 0, 0)), (ANCHO//2 - 180, 530))
        pantalla.blit(fuente.render("Presioná ESC para volver", True, (0, 0, 0)), (ANCHO//2 - 160, 580))

        # ❗ Mensaje de error
        if mensaje:
            texto_mensaje = fuente.render(mensaje, True, (255, 0, 0))
            pantalla.blit(texto_mensaje, (ANCHO//2 - texto_mensaje.get_width()//2, 430))
            
            # 🐾 Mensaje narrativo del capibara
        fuente_capibara = pygame.font.SysFont("Nintendo DS BIOS", 48)
        mensaje_capibara = "Soy un capibara. ¡Ayudame a limpiar el río!"
        texto_capibara = fuente_capibara.render(mensaje_capibara, True, (0, 0, 0))
        pantalla.blit(texto_capibara, (ANCHO // 2 - texto_capibara.get_width() // 2, 50))
        
        
        pygame.display.flip()
        reloj.tick(60)

# Funcion para mostrar la pantalla de fin
def pantalla_fin(pantalla, ANCHO, ALTO, puntos):
    fuente = pygame.font.SysFont("Nintendo DS BIOS", 36)
    reloj = pygame.time.Clock()

    # 🖼️ Fondo opcional
    fondo = pygame.Surface((ANCHO, ALTO))
    fondo.fill((240, 240, 240))  # gris claro

    # 🔘 Botones
    boton_reiniciar = pygame.Rect(ANCHO//2 - 200, 300, 150, 50)
    boton_menu = pygame.Rect(ANCHO//2 - 75, 300, 150, 50)
    boton_salir = pygame.Rect(ANCHO//2 + 50, 300, 150, 50)

    mensaje = "⏱️ ¡Fin del juego!"
    texto_puntaje = f"Puntaje final: {puntos}"

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(evento.pos):
                    return "reiniciar"
                elif boton_menu.collidepoint(evento.pos):
                    return "menu"
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()

        pantalla.blit(fondo, (0, 0))

        # 📝 Mensajes
        texto_mensaje = fuente.render(mensaje, True, (0, 0, 0))
        texto_final = fuente.render(texto_puntaje, True, (0, 100, 0))
        
        pantalla.blit(texto_mensaje, ((ANCHO - texto_mensaje.get_width()) // 2, 180))
        pantalla.blit(texto_final, ((ANCHO - texto_final.get_width()) // 2, 230))

        # 🔘 Botones
        pygame.draw.rect(pantalla, (0, 120, 255), boton_reiniciar)
        pygame.draw.rect(pantalla, (100, 100, 100), boton_menu)
        pygame.draw.rect(pantalla, (200, 0, 0), boton_salir)

        pantalla.blit(fuente.render("Reiniciar", True, (255, 255, 255)), (boton_reiniciar.x + 10, boton_reiniciar.y + 10))
        pantalla.blit(fuente.render("Menú", True, (255, 255, 255)), (boton_menu.x + 30, boton_menu.y + 10))
        pantalla.blit(fuente.render("Salir", True, (255, 255, 255)), (boton_salir.x + 30, boton_salir.y + 10))

        pygame.display.flip()
        reloj.tick(60)

# funcion para jugar la partida
def jugar_partida(pantalla, ANCHO, ALTO, id_usuario, usuario, contraseña):
    # Guardar usuario y registrar partida
    guardar_usuario(id_usuario, usuario, contraseña)
    id_partida = registrar_partida(id_usuario)
    guardar_partida(id_partida, id_usuario, datetime.now(), numero_partida=1, nivel=1)

    # 🎵 Música del juego
    pygame.mixer.music.load("musica_juego.wav")
    pygame.mixer.music.play(-1)

    print(f"✅ Sesión iniciada. ID: {id_usuario}")

    # ⏱️ Tiempo de partida
    tiempo_limite = 30  # segundos
    tiempo_inicio = pygame.time.get_ticks()
    reloj = pygame.time.Clock()

    # Fuentes
    fuente_tiempo = pygame.font.SysFont("Nintendo DS BIOS", 28)
    fuente_hud = pygame.font.SysFont("Nintendo DS BIOS", 20)
    fuente_puntos = pygame.font.SysFont("Nintendo DS BIOS", 28)
    fuente = pygame.font.SysFont("Nintendo DS BIOS", 24)  

    # Colores
    CELESTE = (67, 179, 183)
    BLANCO = (255, 255, 255)
    
    # 📝 Mensaje educativo
    mensaje_educativo_actual = obtener_mensaje_educativo()
    tiempo_mensaje_educativo = pygame.time.get_ticks()


    # 🎯 Puntajes por color
    puntajes = {
        "azul": 3,
        "verde": 2,
        "amarillo": 5,
        "violeta": 5
    }

    # Puntos
    puntos = 0
    puntos_verde = 0
    puntos_azul = 0
    puntos_amarillo = 0
    puntos_violeta = 0
    contaminantes_tocados = 0

    # Velocidad
    velocidad = 25

    # Cargar imágenes
    tacho_img = pygame.image.load("tacho_reciclaje.png").convert_alpha()
    tacho_img = pygame.transform.scale(tacho_img, (80, 80))
    botella_img = pygame.image.load("botella_vidrio.png").convert_alpha()
    botella_img = pygame.transform.scale(botella_img, (50, 50))
    plastico_img = pygame.image.load("botella_plastico.png").convert_alpha()
    plastico_img = pygame.transform.scale(plastico_img, (40, 40))
    papel_img = pygame.image.load("papel_reciclable.png").convert_alpha()
    papel_img = pygame.transform.scale(papel_img, (40, 40))
    electronico_img = pygame.image.load("residuo_electronico.png").convert_alpha()
    electronico_img = pygame.transform.scale(electronico_img, (60, 60))
    residuo_img = pygame.image.load("residuo_no_reciclable.png").convert_alpha()
    residuo_img = pygame.transform.scale(residuo_img, (50, 50))
    comida_img = pygame.image.load("comida.png").convert_alpha()
    comida_img = pygame.transform.scale(comida_img, (40, 40))
#-----------------------------------------------------Objetos--------------------------------------------------------
    # 🔴 Jugador tacho_reciclaje
    rojo_x, rojo_y = 25, 25
    rojo_ancho, rojo_alto = 40, 40
    rect_rojo = pygame.Rect(rojo_x, rojo_y, rojo_ancho, rojo_alto)

    # 🔵 Azul papel_reciclable
    azul_ancho, azul_alto = 40, 40
    azul_x = random.randint(0, ANCHO - azul_ancho)
    azul_y = random.randint(0, ALTO - azul_alto)
    rect_azul = pygame.Rect(azul_x, azul_y, azul_ancho, azul_alto)

    # 🟢 Verde botella_vidrio
    verde_ancho, verde_alto = 50, 50
    verde_x = random.randint(0, ANCHO - verde_ancho)
    verde_y = random.randint(0, ALTO - verde_alto)
    rect_verde = pygame.Rect(verde_x, verde_y, verde_ancho, verde_alto)

    # 🟡 Amarillo botella_plastico
    amarillo_ancho, amarillo_alto = 40, 40
    amarillo_x = random.randint(0, ANCHO - amarillo_ancho)
    amarillo_y = random.randint(0, ALTO - amarillo_alto)
    rect_amarillo = pygame.Rect(amarillo_x, amarillo_y, amarillo_ancho, amarillo_alto)

    # 🟣 Violeta
    violeta_ancho, violeta_alto = 60, 60
    violeta_x = random.randint(0, ANCHO - violeta_ancho)
    violeta_y = random.randint(0, ALTO - violeta_alto)
    rect_violeta = pygame.Rect(violeta_x, violeta_y, violeta_ancho, violeta_alto)

    # ⚪ Blanco (contaminante)
    blanco_ancho, blanco_alto = 50, 50
    blanco_x = random.randint(0, ANCHO - blanco_ancho)
    blanco_y = random.randint(0, ALTO - blanco_alto)
    rect_blanco = pygame.Rect(blanco_x, blanco_y, blanco_ancho, blanco_alto)
    direccion_blanco = [random.choice([-1, 1]), random.choice([-1, 1])]

    # Bonus
    rect_bonus = pygame.Rect(-100, -100, comida_img.get_width(), comida_img.get_height()) # Oculto inicialmente
    bonus_activo = False
    ultimo_umbral_bonus = 0
    TIEMPO_INICIAL = 30  # segundos
    tiempo_limite = TIEMPO_INICIAL
    tiempo_inicio = pygame.time.get_ticks()

    # --------------------------------------------Bucle principal--------------------------------------------------------
    corriendo = True
    while corriendo:
        
        # FIX: Procesar eventos para que Pygame actualice el estado de las teclas
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        # Movimiento del rojo
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT]:
            rect_rojo.x -= velocidad
        if teclas[pygame.K_RIGHT]:
            rect_rojo.x += velocidad
        if teclas[pygame.K_UP]:
            rect_rojo.y -= velocidad
        if teclas[pygame.K_DOWN]:
            rect_rojo.y += velocidad

        # 🔒 Limitar movimiento
        # Limitar movimiento horizontal
        rect_rojo.x = min(max(rect_rojo.x, 0), ANCHO - rect_rojo.width)


        # Limitar movimiento vertical (dejando espacio para el HUD)
        MARGEN_SUPERIOR = 100  # espacio para logo, mensaje y HUD superior
        MARGEN_INFERIOR = 50   # espacio para HUD inferior
        rect_rojo.y = max(20, min(rect_rojo.y, ALTO - rect_rojo.height - MARGEN_SUPERIOR))



#------------------------------------------------------Colisiones--------------------------------------------------------
        #  Rojo
        # Penalización por tocar el blanco
        if rect_rojo.colliderect(rect_blanco):
            puntos = max(0, puntos - 5)
            rect_blanco.x = random.randint(0, ANCHO - blanco_ancho)
            rect_blanco.y = random.randint(MARGEN_SUPERIOR, ALTO - blanco_alto - MARGEN_INFERIOR)
            contaminantes_tocados += 1

        # 🔵 Azul
        if rect_rojo.colliderect(rect_azul):
            puntos += puntajes["azul"]
            puntos_azul += puntajes["azul"]
            registrar_coordenada(id_usuario, id_partida, "tacho_reciclaje", "papel_reciclable", rect_azul.x, rect_azul.y)
            rect_azul.x = random.randint(0, ANCHO - azul_ancho)
            rect_azul.y = random.randint(MARGEN_SUPERIOR, ALTO - azul_alto - MARGEN_INFERIOR)

        if rect_blanco.colliderect(rect_azul):
            registrar_coordenada(id_usuario, id_partida, "residuo_no_reciclable", "papel_reciclable", rect_azul.x, rect_azul.y)
            rect_azul.x = random.randint(0, ANCHO - azul_ancho)
            rect_azul.y = random.randint(MARGEN_SUPERIOR, ALTO - azul_alto - MARGEN_INFERIOR)

        # 🟢 Verde
        if rect_rojo.colliderect(rect_verde):
            puntos += puntajes["verde"]
            puntos_verde += puntajes["verde"]
            registrar_coordenada(id_usuario, id_partida, "tacho_reciclaje", "botella_vidrio", rect_verde.x, rect_verde.y)
            rect_verde.x = random.randint(0, ANCHO - verde_ancho)
            rect_verde.y = random.randint(MARGEN_SUPERIOR, ALTO - verde_alto - MARGEN_INFERIOR)

        if rect_blanco.colliderect(rect_verde):
            registrar_coordenada(id_usuario, id_partida, "residuo_no_reciclable", "botella_vidrio", rect_verde.x, rect_verde.y)
            rect_verde.x = random.randint(0, ANCHO - verde_ancho)
            rect_verde.y = random.randint(MARGEN_SUPERIOR, ALTO - verde_alto - MARGEN_INFERIOR)

        # 🟡 Amarillo
        if rect_rojo.colliderect(rect_amarillo):
            puntos += puntajes["amarillo"]
            puntos_amarillo += puntajes["amarillo"]
            registrar_coordenada(id_usuario, id_partida, "tacho_reciclaje", "botella_plastico", rect_amarillo.x, rect_amarillo.y)
            rect_amarillo.x = random.randint(0, ANCHO - rect_amarillo.width)
            rect_amarillo.y = random.randint(MARGEN_SUPERIOR, ALTO - rect_amarillo.height - MARGEN_INFERIOR)

        if rect_blanco.colliderect(rect_amarillo):
            registrar_coordenada(id_usuario, id_partida, "residuo_no_reciclable", "botella_plastico", rect_amarillo.x, rect_amarillo.y)
            rect_amarillo.x = random.randint(0, ANCHO - rect_amarillo.width)
            rect_amarillo.y = random.randint(MARGEN_SUPERIOR, ALTO - rect_amarillo.height - MARGEN_INFERIOR)

        # 🟣 Violeta
        if rect_rojo.colliderect(rect_violeta):
            puntos += puntajes["violeta"]
            puntos_violeta += puntajes["violeta"]
            registrar_coordenada(id_usuario, id_partida, "tacho_reciclaje", "residuo_electronico", rect_violeta.x, rect_violeta.y)
            rect_violeta.x = random.randint(0, ANCHO - rect_violeta.width)
            rect_violeta.y = random.randint(MARGEN_SUPERIOR, ALTO - rect_violeta.height - MARGEN_INFERIOR)

        if rect_blanco.colliderect(rect_violeta):
            registrar_coordenada(id_usuario, id_partida, "residuo_no_reciclable", "residuo_electronico", rect_violeta.x, rect_violeta.y)
            rect_violeta.x = random.randint(0, ANCHO - rect_violeta.width)
            rect_violeta.y = random.randint(MARGEN_SUPERIOR, ALTO - rect_violeta.height - MARGEN_INFERIOR)



        # ⚪ Blanco
        if rect_blanco.colliderect(rect_azul):
            registrar_coordenada(id_usuario, id_partida, "residuo_no_reciclable", "papel_reciclable", rect_azul.x, rect_azul.y)

        if rect_blanco.colliderect(rect_verde):
            registrar_coordenada(id_usuario, id_partida, "residuo_no_reciclable", "botella_vidrio", rect_verde.x, rect_verde.y)

        if rect_blanco.colliderect(rect_amarillo):
            registrar_coordenada(id_usuario, id_partida, "residuo_no_reciclable", "botella_plastico", rect_amarillo.x, rect_amarillo.y)

        if rect_blanco.colliderect(rect_violeta):
            registrar_coordenada(id_usuario, id_partida, "residuo_no_reciclable", "residuo_electronico", rect_violeta.x, rect_violeta.y)

        # Bonus
        if bonus_activo and rect_rojo.colliderect(rect_bonus):
            tiempo_inicio = pygame.time.get_ticks()  # Reinicia el cronómetro
            bonus_activo = False
            rect_bonus.x = -100  # Ocultarlo nuevamente
            rect_bonus.y = -100


        # ⏱️ Calcular tiempo restante
        tiempo_actual = pygame.time.get_ticks()
        tiempo_restante = max(0, tiempo_limite - ((tiempo_actual - tiempo_inicio) // 1000))


        # 🛑 Terminar partida si se acaba el tiempo
        if tiempo_restante == 0:
            
            #Registrar colisiones al finalizar la partida
            registrar_colisiones(id_usuario, id_partida,
                botella_vidrio=puntos_verde,
                papel_reciclable=puntos_azul,
                botella_plastico=puntos_amarillo,
                residuo_electronico=puntos_violeta
            )


            resultado = pantalla_fin(pantalla, ANCHO, ALTO, puntos)
            if resultado == "reiniciar":
                return "reiniciar"  # Reiniciar la partida
            elif resultado == "menu":
                return "menu"  # Volver al menú principal

        # 🖥️ Mostrar cronómetro en pantalla
        texto_tiempo = fuente_tiempo.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 255))

        # Movimiento aleatorio del blanco
        rect_blanco.x += direccion_blanco[0] * 5
        rect_blanco.y += direccion_blanco[1] * 5

        # Rebote en bordes
        if rect_blanco.left <= 0 or rect_blanco.right >= ANCHO:
            direccion_blanco[0] *= -1
        if rect_blanco.top <= 0 or rect_blanco.bottom >= ALTO:
            direccion_blanco[1] *= -1

        #Bonus aparece al llegar a 50 puntos
        if puntos >= ultimo_umbral_bonus + 50 and not bonus_activo:
            rect_bonus.x = random.randint(0, ANCHO - rect_bonus.width)
            rect_bonus.y = random.randint(MARGEN_SUPERIOR, ALTO - rect_bonus.height - MARGEN_INFERIOR)
            bonus_activo = True
            ultimo_umbral_bonus += 50  # Avanzar al siguiente umbral


        # Actualizar mensaje educativo cada 30 segundos
        if pygame.time.get_ticks() - tiempo_mensaje_educativo > 30000:  # 30 segundos
            mensaje_educativo_actual = obtener_mensaje_educativo()
            tiempo_mensaje_educativo = pygame.time.get_ticks()


        # Dibujar
        pantalla.fill(CELESTE)  # Fondo celeste
        pantalla.blit(tacho_img, rect_rojo)  # Dibujar Tacho de basura (jugador)
        pantalla.blit(botella_img, rect_verde)  # Botella de vidrio (verde)
        pantalla.blit(plastico_img, rect_amarillo)  # Botella de plástico (amarillo)
        pantalla.blit(papel_img, rect_azul)  # Papel reciclable (azul)
        pantalla.blit(electronico_img, rect_violeta)  # Residuo electrónico (violeta)
        pantalla.blit(residuo_img, rect_blanco)  # Residuo no reciclable (blanco)
        if bonus_activo:
            pantalla.blit(comida_img, rect_bonus)  # Bonus (comida)
                   

        
        # Dibujar HUD
        dibujar_hud(pantalla, fuente_hud, puntos, puntos_azul, puntos_verde, puntos_amarillo, puntos_violeta, contaminantes_tocados, tiempo_restante)
        fuente = pygame.font.SysFont("Nintendo DS BIOS", 20)
        dibujar_mensaje_educativo(pantalla, fuente, mensaje_educativo_actual, tiempo_mensaje_educativo)
        
        pygame.display.flip()
        reloj.tick(60)

    pygame.quit()
    sys.exit()
    
#-----------------------------------------------------REGISTRO---------------------------------------------------------
# Funcion para registrar la partida
def registrar_partida(id_usuario):
    archivo = "registro_partidas.txt"
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            pass  # Crea el archivo si no existe

    # Leer todas las partidas previas
    with open(archivo, "r") as f:
        lineas = f.readlines()

    # Contar cuántas partidas jugó este usuario
    partidas_usuario = [linea for linea in lineas if linea.strip().split(";")[1] == str(id_usuario)]
    numero_partida = len(partidas_usuario) + 1
    id_partida = len(lineas) + 1

    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
    nivel = "nivel_1"

    nueva_linea = f"{id_partida};{id_usuario};{fecha_actual};{numero_partida};{nivel}\n"

    with open(archivo, "a") as f:
        f.write(nueva_linea)

    return id_partida

# Funcion para registrar colisiones
def registrar_colisiones(id_usuario, id_partida, botella_vidrio, papel_reciclable, botella_plastico, residuo_electronico):
    archivo = "registro_colisiones.txt"
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            pass

    with open(archivo, "r") as f:
        lineas = f.readlines()

    id_colision = len(lineas) + 1
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")

    nueva_linea = f"{id_colision};{id_usuario};{id_partida};{botella_vidrio};{papel_reciclable};{botella_plastico};{residuo_electronico};{fecha_actual}\n"

    with open(archivo, "a") as f:
        f.write(nueva_linea)

    guardar_colision(id_usuario, id_partida, botella_vidrio, papel_reciclable, botella_plastico, residuo_electronico, datetime.now())

# Funcion para registrar coordenadas
def registrar_coordenada(id_usuario, id_partida, objeto_colisionador, objeto_colisionado, x, y):
    archivo = "registro_coordenadas.txt"
    encabezado = "id_coordenada;id_partida;id_usuario;objeto_colisionador;objeto_colisionado;x;y;fecha_hora\n"

    if not os.path.exists(archivo) or os.path.getsize(archivo) == 0:
        with open(archivo, "w") as f:
            f.write(encabezado)

    with open(archivo, "r") as f:
        lineas = f.readlines()

    id_coordenada = len(lineas)
    fecha_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    nueva_linea = f"{id_coordenada};{id_partida};{id_usuario};{objeto_colisionador};{objeto_colisionado};{x};{y};{fecha_hora}\n"

    with open(archivo, "a") as f:
        f.write(nueva_linea)
     
    guardar_coordenada(id_partida, id_usuario, objeto_colisionador, objeto_colisionado, x, y, datetime.now())

# Funcion para verificar o crear usuario
def verificar_o_crear_usuario(usuario, contraseña):
    archivo = "registro_usuario.txt"
    if not os.path.exists(archivo):
        with open(archivo, "w") as f:
            pass

    with open(archivo, "r") as f:
        lineas = f.readlines()

    for linea in lineas:
        partes = linea.strip().split(";")
        if len(partes) == 3 and partes[1] == usuario:
            if partes[2] == contraseña:
                return partes[0]  # ID válido
            else:
                return None

    nuevo_id = str(len(lineas) + 1)
    with open(archivo, "a") as f:
        f.write(f"{nuevo_id};{usuario};{contraseña}\n")
    guardar_usuario(nuevo_id, usuario, contraseña)
    return nuevo_id

# Función para dibujar el HUD
def dibujar_hud(pantalla, fuente, puntos, puntos_azul, puntos_verde, puntos_amarillo, puntos_violeta, contaminantes_tocados,tiempo_restante):
    # Fondo del HUD
    pygame.draw.rect(pantalla, (30, 30, 30), (0, 0, pantalla.get_width(), 40))
    fuente = pygame.font.SysFont("Nintendo DS BIOS", 20)
    # Textos
    texto_puntos = fuente.render(f"Puntos: {puntos}", True, (255, 255, 255))
    pantalla.blit(texto_puntos, (10, 10))
    texto_tiempo = fuente.render(f"Tiempo: {tiempo_restante}s", True, (255, 255, 255))
    pantalla.blit(texto_tiempo, (800, 10))  # Ajustá la posición según tu resolución

    pantalla.blit(fuente.render(f"Papel: {puntos_azul}", True, (100, 150, 255)), (150, 10))
    pantalla.blit(fuente.render(f"Vidrio: {puntos_verde}", True, (100, 255, 100)), (250, 10))
    pantalla.blit(fuente.render(f"Plástico: {puntos_amarillo}", True, (255, 255, 100)), (370, 10))
    pantalla.blit(fuente.render(f"Electrónicos: {puntos_violeta}", True, (200, 100, 255)), (500, 10))
    pantalla.blit(fuente.render(f"Contaminantes: {contaminantes_tocados}", True, (255, 100, 100)), (650, 10))

# Función para obtener mensaje educativo
def obtener_mensaje_educativo():
    mensajes = [
        "Reciclar es un pequeño gesto con gran impacto.",
        "Cada botella reciclada ahorra energía y recursos.",
        "El papel puede reciclarse hasta 4 veces.",
        "El plástico reciclado puede convertirse en ropa o muebles.",
        "El vidrio se recicla infinitamente sin perder calidad.",
        "Los electrónicos contienen metales valiosos. ¡Reciclalos con cuidado!",
        "Cuidar el río es cuidar la vida que depende de él.",
        "¡Tu capibara está orgulloso de vos!",
        "Cada acción cuenta. ¡Seguí así!",
        "El planeta te lo agradece.",
        "Separar residuos es el primer paso hacia un mundo mejor.",
        "Aprender a reciclar es enseñar a cuidar.",
        "La naturaleza te necesita. ¡Gracias por ayudar!",
        "Lo que hacés hoy, florece mañana.",
        "Un río limpio es un hogar seguro para todos.",
        "Reutilizá antes de desechar.",
        "Compostar también es reciclar.",
        "¡Tu esfuerzo limpia más que el juego!",
        "Aprender jugando es la mejor forma de crecer."
    ]
    return random.choice(mensajes)

# Función para dibujar mensaje educativo
def dibujar_mensaje_educativo(pantalla, fuente, mensaje, tiempo_mensaje, duracion=30000):
    tiempo_actual = pygame.time.get_ticks()
    if mensaje and tiempo_actual - tiempo_mensaje < duracion:
        alto_mensaje = 40
        pygame.draw.rect(pantalla, (40, 40, 40), (0, pantalla.get_height() - alto_mensaje, pantalla.get_width(), alto_mensaje))
        texto = fuente.render(mensaje, True, (255, 255, 255))
        pantalla.blit(texto, (20, pantalla.get_height() - alto_mensaje + 10))

# Función principal
def main():
    pygame.init()
    ANCHO, ALTO = 1280, 720
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Juego de Reciclaje")

    while True:
        opcion = menu_principal(pantalla, ANCHO, ALTO)

        if opcion == "jugar":
            resultado_inicio = pantalla_inicio(pantalla, ANCHO, ALTO)
            if resultado_inicio is None:
                continue  # Volver al menú si se presionó ESC

            id_usuario, usuario, contraseña = resultado_inicio

            resultado_juego = jugar_partida(pantalla, ANCHO, ALTO, id_usuario, usuario, contraseña)

            if resultado_juego == "reiniciar":
                # Reiniciar la partida directamente
                jugar_partida(pantalla, ANCHO, ALTO, id_usuario, usuario, contraseña)
            elif resultado_juego == "menu":
                continue  # Volver al menú

        elif opcion == "informacion":
            mostrar_informacion(pantalla)
            continue  # Volver al menú

        elif opcion == "creditos":
            mostrar_creditos(pantalla)
            continue  # Volver al menú

        elif opcion == "salir":
            pygame.quit()
            sys.exit()


# Modificación en la ejecución principal (al final del archivo)
if __name__ == "__main__":
    main()