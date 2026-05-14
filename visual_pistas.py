# -*- coding: utf-8 -*-
"""
Created on Wed May 13 17:20:35 2026

@author: shado
"""

import cv2
import numpy as np
import pygame

# 🔹 Inicializar Pygame
pygame.init()

# 🔹 Crear fuentes
font = pygame.font.SysFont(None, 10)  # fuente normal
font_pregunta = pygame.font.SysFont("arial", 35, bold=True)  # fuente llamativa

# --- Cargar y escalar imagen base ---
base_img = pygame.image.load("12 peleadores SELECTOR.png")

ventana_ancho, ventana_alto = 640, 480
img_ancho, img_alto = base_img.get_size()
nuevo_ancho = ventana_ancho
nuevo_alto = int(img_alto * (ventana_ancho / img_ancho))
base_scaled = pygame.transform.scale(base_img, (nuevo_ancho, nuevo_alto))

# --- Generar posiciones automáticamente ---
nombres = ["Ryu","E. Honda","Blanka","Guile","Balrog","Vega",
           "Ken","Chun-Li","Zangief","Dhalsim","Sagat", "M. Bison"]

ancho, alto = base_scaled.get_size()
col_w = ancho // 6
row_h = alto // 2

posiciones = {}
for i, nombre in enumerate(nombres):
    fila = i // 6
    col = i % 6
    x = col * col_w
    y = fila * row_h
    posiciones[nombre] = (x, y, col_w, row_h)


# --- Generar posiciones automáticamente ---
nombres = ["Ryu","E. Honda","Blanka","Guile","Balrog","Vega",
           "Ken","Chun-Li","Zangief","Dhalsim","Sagat", "M. Bison"]

ancho, alto = base_scaled.get_size()
col_w = ancho // 6
row_h = alto // 2

posiciones = {}
for i, nombre in enumerate(nombres):
    fila = i // 6
    col = i % 6
    x = col * col_w
    y = fila * row_h
    posiciones[nombre] = (x, y, col_w, row_h)

# --- Para que las preguntas no se desborden de la ventana ---
def draw_text_multiline(text, screen, font, color=(255,255,0), max_width=600, start_y=270):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + " " + word if current_line else word
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    # Dibujar cada línea centrada
    for i, line in enumerate(lines):
        surface = font.render(line, True, color)
        rect = surface.get_rect(center=(320, start_y + i*40))
        screen.blit(surface, rect)
        
# --- Conversión a blanco y negro ---
def to_grayscale(surface):
    arr = pygame.surfarray.array3d(surface)
    gray = cv2.cvtColor(arr, cv2.COLOR_RGB2GRAY)
    gray3 = np.stack((gray,)*3, axis=-1)
    return pygame.surfarray.make_surface(gray3)

# --- Mostrar pista interactiva ---
def mostrar_pista(atributo, candidatos, screen, font, clock, pregunta_texto=None):
    running = True
    respuesta = None

    while running:
        screen.fill((0,0,0))

        # Dibujar todos los personajes en cuadrícula
        for nombre in nombres:
            if nombre in posiciones:
                x,y,w,h = posiciones[nombre]
                recorte = base_scaled.subsurface((x,y,w,h))

                personaje = next((p for p in candidatos if p["nombre"] == nombre), None)

                if personaje and atributo in personaje:  # atributo booleano
                    if personaje[atributo]:
                        screen.blit(recorte, (x,y))
                    else:
                        gris = to_grayscale(recorte)
                        screen.blit(gris, (x,y))
                elif atributo == nombre:  # atributo es nombre de personaje
                    screen.blit(recorte, (x,y))
                else:
                    gris = to_grayscale(recorte)
                    screen.blit(gris, (x,y))


        if pregunta_texto:
            # Texto centrado
            draw_text_multiline(pregunta_texto, screen, font_pregunta, (255,255,0), max_width=600, start_y=270)


        # Leyenda
        leyenda = font.render("NOTA: Los personajes en COLOR son un SI", True, (255,255,255))
        screen.blit(leyenda, leyenda.get_rect(center=(320, 370)))

        # Botones
        btn_si = pygame.Rect(170, 400, 120, 50)
        btn_no = pygame.Rect(350, 400, 120, 50)
        pygame.draw.rect(screen, (0,128,0), btn_si)
        pygame.draw.rect(screen, (128,0,0), btn_no)

        si_label = font.render("Sí", True, (255,255,255))
        no_label = font.render("No", True, (255,255,255))
        screen.blit(si_label, si_label.get_rect(center=btn_si.center))
        screen.blit(no_label, no_label.get_rect(center=btn_no.center))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if btn_si.collidepoint(event.pos):
                    respuesta = "s"
                    running = False
                elif btn_no.collidepoint(event.pos):
                    respuesta = "n"
                    running = False

        clock.tick(30)

    screen.fill((0,0,0))
    pygame.display.update()
    return respuesta






