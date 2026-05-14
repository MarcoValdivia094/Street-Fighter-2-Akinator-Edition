# -*- coding: utf-8 -*-
"""
Created on Tue May 12 22:12:03 2026

@author: shado
"""

import cv2
import pygame
import streetfighter_game

def fade_in(screen, clock):
    overlay = pygame.Surface((640, 480))
    overlay.fill((0,0,0))

    # 🔹 Fade in: de negro total a transparente
    for alpha in range(255, -1, -10):  # empieza en 255 (oscuro) y baja hasta 0
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0,0))
        pygame.display.update()
        clock.tick(30)

def transicion(screen, clock):
    # 🔹 Sonido de moneda
    credito = pygame.mixer.Sound("MONEDA.MP3")
    credito.set_volume(1.0)
    credito.play()

    # 🔹 Espera breve para que se escuche el sonido antes del fade
    pygame.time.delay(300)  # 300 ms (~0.3 segundos)
    
    # 🔹 Fade out
    overlay = pygame.Surface((640, 480))
    overlay.fill((0,0,0))
    for alpha in range(0, 255, 10):
        overlay.set_alpha(alpha)
        screen.blit(overlay, (0,0))
        pygame.display.update()
        clock.tick(30)

def pantalla_inicio(screen, clock):
    cap = cv2.VideoCapture("StreetFighter_INTRO.mp4")
    pygame.mixer.init()
    pygame.mixer.music.load("OpeningTheme.mp3")

    running = True
    audio_started = False

    while running:
        ret, frame = cap.read()
        if not ret:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            pygame.mixer.music.stop()
            pygame.mixer.music.play(-1)
            continue

        if not audio_started:
            pygame.mixer.music.play(-1)
            audio_started = True

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (640, 480))
        frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))

        screen.blit(frame_surface, (0,0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return "salir"
            elif event.type == pygame.KEYDOWN:
                pygame.mixer.music.stop()
                cap.release()
                transicion(screen, clock)  # 🔹 aquí se escucha el sonido y fade
                return "juego"

        clock.tick(30)

    cap.release()
    return "salir"


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    # 🔹 Inicializar Pygame
    pygame.init()
    
    # 🔹 Cargar tu icono (usa una imagen cuadrada, pequeña, tipo 32x32 o 64x64)
    icono = pygame.image.load("Zangief.gif")
    
    # 🔹 Asignar el icono a la ventana
    pygame.display.set_icon(icono)
    
    # 🔹 Título de la ventana
    pygame.display.set_caption("Street Fighter 2: AKINATOR EDITION")

    fade_in(screen, clock)  # 🔹 efecto de entrada suave
    estado = "intro"

    while True:
        if estado == "intro":
            estado = pantalla_inicio(screen, clock)
        elif estado == "juego":
            estado = streetfighter_game.juego(screen, clock)
        elif estado == "salir":
            break

    pygame.quit()

