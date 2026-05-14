# -*- coding: utf-8 -*-
"""
Created on Tue May 12 22:00:58 2026

@author: shado
"""

import json
import random
import pygame
import cv2
from collections import Counter
from visual_pistas import mostrar_pista

# 🔹 Video de fondo para las preguntas
cap_fondo = cv2.VideoCapture("SELECTION SF2.mp4")

def draw_video_background(screen):
    ret, frame = cap_fondo.read()
    if not ret:
        cap_fondo.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap_fondo.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = cv2.resize(frame, (320, 240))

    # 🔹 Convertir el frame de OpenCV a Surface de Pygame
    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))

    # Calcular posición centrada en X y arriba en Y
    x_offset = (640 - 320) // 2  # =160
    y_offset = 0                 # hasta arriba

    screen.blit(frame_surface, (x_offset, y_offset))

def fade_in(screen, clock):
    overlay = pygame.Surface((640, 480))
    overlay.fill((0,0,0))

    # 🔹 Fade in: de negro total a transparente
    for alpha in range(255, -1, -10):  # empieza en 255 (oscuro) y baja hasta 0
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0,0))
        pygame.display.update()
        clock.tick(30)

def juego(screen, clock):
    pygame.display.set_caption("Street Fighter 2: AKINATOR EDITION")
    font = pygame.font.SysFont(None, 36)

    # 🔹 Música de fondo en loop
    pygame.mixer.music.load("GUILE THEME.mp3")  # tu canción
    pygame.mixer.music.set_volume(0.7)          # volumen ajustable
    pygame.mixer.music.play(-1)                 # -1 = loop infinito

    # 🔹 Fade in al iniciar el juego
    fade_in(screen, clock)
    
    # Cargar dataset
    with open("StreetFighter_V2.json", "r", encoding="utf-8") as f:
        personajes = json.load(f)

    # Cargar historial
    try:
        with open("historial.json", "r", encoding="utf-8") as f:
            historial = json.load(f)
    except FileNotFoundError:
        historial = []

    frases_atributos = {
        "USA": "¿Tu personaje es estadounidense?",
        "rubio": "¿Tu personaje es rubio?",
        "proyectil": "¿Tu personaje lanza proyectiles?",
        "ropa_militar": "¿Tu personaje usa ropa militar?",
        "pecho_destapado": "¿Tu personaje pelea con el pecho al descubierto?",
        "usa_zapatos": "¿Tu personaje usa zapatos?"
    }

    frases_detalle = {
        "Ryu": "¿Tu personaje usa un traje de judo blanco?",
        "Ken": "¿Tu personaje usa un traje de judo rojo?",
        "Chun-Li": "¿Tu personaje es mujer?",
        "Guile": "¿Tu personaje tiene una bandera tatuada en el brazo?",
        "E. Honda": "¿Tu personaje parece un peleador de sumo?",
        "Blanka": "¿Tu personaje tiene la piel verde?",
        "Zangief": "¿Tu personaje tiene barba?",
        "Dhalsim": "¿Tu personaje lleva un collar con cráneos?",
        "Balrog": "¿Tu personaje es boxeador?",
        "Vega": "¿Tu personaje usa una garra como arma?",
        "Sagat": "¿Tu personaje usa un parche en el ojo?",
        "M. Bison": "¿Tu personaje usa sombrero y capa?"
    }

    atributos = ["USA", "rubio", "proyectil", "ropa_militar", "pecho_destapado", "usa_zapatos"]
    candidatos = personajes

    def mostrar_gif(nombre, screen):
        try:
            ruta = f"{nombre}.gif"
            gif = pygame.image.load(ruta)
            gif = pygame.transform.scale(gif, (250, 250))
            rect = gif.get_rect(center=(320, 240))
            screen.blit(gif, rect)
        except Exception as e:
            print(f"No se pudo cargar el gif de {nombre}: {e}")

    def draw_text_multiline(text, y, screen, font, color=(255,255,255)):
        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if font.size(test_line)[0] <= 600:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
    
        for i, line in enumerate(lines):
            surface = font.render(line, True, color)
            rect = surface.get_rect(center=(320, y + i*40))
            screen.blit(surface, rect)

    def draw_button(text, x, y, w, h):
        rect = pygame.Rect(x, y, w, h)
        pygame.draw.rect(screen, (0,128,255), rect)
        label = font.render(text, True, (255,255,255))
        label_rect = label.get_rect(center=rect.center)
        screen.blit(label, label_rect)
        return rect

    def preguntar(pregunta, atributo=None):
        
        # 🔹 Fuente más grande y llamativa para el resultado
        font_pregunta = pygame.font.SysFont("arial", 40, bold=True)
        
        while True:
            # 🔹 Primero dibuja el fondo (video)
            draw_video_background(screen)
    
            # 🔹 Luego limpia la zona de las preguntas con un rectángulo negro
            # (opcional si el video cubre todo, pero útil si quieres asegurar)
            pygame.draw.rect(screen, (0,0,0), (0,240,640,240))
    
            # 🔹 Ahora sí dibuja la nueva pregunta y botones
            draw_text_multiline(pregunta, 280, screen, font_pregunta)
            btn_si = draw_button("Sí", 120, 370, 120, 50)
            btn_no = draw_button("No", 260, 370, 120, 50)
            btn_ns = draw_button("No sé", 400, 370, 120, 50)
    
            pygame.display.update()
    
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if btn_si.collidepoint(event.pos):
                        return "s"
                    elif btn_no.collidepoint(event.pos):
                        return "n"
                    elif btn_ns.collidepoint(event.pos):
                        resp = mostrar_pista(atributo, candidatos, screen, font, clock, pregunta_texto=pregunta)
                        return resp
            clock.tick(30)

    def mostrar_resultado(nombre, historial):
        
        # 🔹 Fuente más grande y llamativa para el resultado
        font_resultado = pygame.font.SysFont("arial", 43, bold=True)
        font_letrero = pygame.font.SysFont("arial", 30, bold=True)
        
        # 🔹 Detener música al revelar personaje
        pygame.mixer.music.stop()
        
        # 🔹 Sonido de victoria
        victoria = pygame.mixer.Sound("Win Theme.mp3")
        victoria.set_volume(1.0)
        victoria.play()
    
        historial.append(nombre)
        historial = historial[-5:]
        with open("historial.json", "w", encoding="utf-8") as f:
            json.dump(historial, f, ensure_ascii=False, indent=2)
    
        running = True
        while running:
            screen.fill((0,0,0))
            # Línea 1
            linea1 = font_letrero.render("Tu personaje es:", True, (255,255,255))
            rect1 = linea1.get_rect(center=(320, 35))
            screen.blit(linea1, rect1)
            
            # Línea 2 (nombre del personaje)
            linea2 = font_resultado.render(nombre, True, (255,255,0))
            rect2 = linea2.get_rect(center=(320, 80))
            screen.blit(linea2, rect2)        
            mostrar_gif(nombre, screen)
    
            # 🔹 Solo mostrar el botón cuando el sonido ya terminó
            if not pygame.mixer.get_busy():
                btn_inicio = pygame.Rect(220, 400, 200, 50)
                pygame.draw.rect(screen, (0,128,255), btn_inicio)
                inicio_label = font.render("Volver al inicio", True, (255,255,255))
                screen.blit(inicio_label, inicio_label.get_rect(center=btn_inicio.center))
    
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "salir"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # 🔹 Solo funciona si el botón ya está visible
                    if not pygame.mixer.get_busy() and btn_inicio.collidepoint(event.pos):
                        return "intro"
            clock.tick(30)


    # --- Lógica del historial ---
    conteo = Counter(historial[-5:])
    personaje_dominante = None
    for nombre, veces in conteo.items():
        if veces >= 3:
            personaje_dominante = nombre
            break

    if personaje_dominante and personaje_dominante in frases_detalle:
        resp = preguntar(frases_detalle[personaje_dominante], atributo=personaje_dominante)
        if resp == "s":
            return mostrar_resultado(personaje_dominante, historial)
        elif resp == "n":
            candidatos = [p for p in candidatos if p["nombre"] != personaje_dominante]

    # --- Lógica del juego ---
    random.shuffle(atributos)
    for atributo in atributos:
        valores = set([p[atributo] for p in candidatos])
        if len(valores) == 1:
            continue

        resp = preguntar(frases_atributos[atributo], atributo)
        if resp == "s":
            candidatos = [p for p in candidatos if p[atributo] == True]
        elif resp == "n":
            candidatos = [p for p in candidatos if p[atributo] == False]
        elif resp == "salir":
            return "salir"

        if len(candidatos) == 1:
            elegido = candidatos[0]["nombre"]
            return mostrar_resultado(elegido, historial)

    # --- Preguntas de detalle ---
    if len(candidatos) > 1:
        for i, p in enumerate(candidatos):
            resp = preguntar(frases_detalle[p["nombre"]], atributo=p["nombre"])
            if resp == "s":
                return mostrar_resultado(p["nombre"], historial)
            elif resp == "n" and len(candidatos) == 2:
                otro = candidatos[1 - i]
                return mostrar_resultado(otro["nombre"], historial)
            elif resp == "salir":
                return "salir"

    return "intro"