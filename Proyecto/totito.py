import random
import math
import tkinter as tk
from tkinter import messagebox

class TresEnRaya:
    def __init__(self, root):
        self.root = root
        self.tablero = ['-' for _ in range(9)]
        if random.randint(0, 1) == 1:
            self.jugadorHumano = 'X'
            self.jugadorBot = "O"
        else:
            self.jugadorHumano = "O"
            self.jugadorBot = "X"
        self.bot = JugadorComputadora(self.jugadorBot, self)
        self.humano = JugadorHumano(self.jugadorHumano, self)
        self.botones = []
        self.crear_tablero()

    def crear_tablero(self):
        for i in range(3):
            fila = []
            for j in range(3):
                boton = tk.Button(self.root, text='', font=('normal', 40), width=5, height=2,
                                  command=lambda fila=i, col=j: self.humano.movimiento_humano(fila * 3 + col))
                boton.grid(row=i, column=j)
                fila.append(boton)
            self.botones.append(fila)

    def mostrar_tablero(self):
        for i in range(3):
            for j in range(3):
                self.botones[i][j]['text'] = self.tablero[i * 3 + j]

    def tablero_lleno(self, estado):
        return '-' not in estado

    def ganador(self, estado, jugador):
        return (estado[0] == estado[1] == estado[2] == jugador or
                estado[3] == estado[4] == estado[5] == jugador or
                estado[6] == estado[7] == estado[8] == jugador or
                estado[0] == estado[3] == estado[6] == jugador or
                estado[1] == estado[4] == estado[7] == jugador or
                estado[2] == estado[5] == estado[8] == jugador or
                estado[0] == estado[4] == estado[8] == jugador or
                estado[2] == estado[4] == estado[6] == jugador)

    def revisar_ganador(self):
        if self.ganador(self.tablero, self.jugadorHumano):
            messagebox.showinfo("Juego terminado", f"¡Jugador {self.jugadorHumano} gana el juego!")
            self.root.quit()
            return True

        if self.ganador(self.tablero, self.jugadorBot):
            messagebox.showinfo("Juego terminado", f"¡Jugador {self.jugadorBot} gana el juego!")
            self.root.quit()
            return True

        if self.tablero_lleno(self.tablero):
            messagebox.showinfo("Juego terminado", "¡Empate!")
            self.root.quit()
            return True
        return False

    def iniciar(self):
        self.mostrar_tablero()

class JugadorHumano:
    def __init__(self, letra, juego):
        self.letra = letra
        self.juego = juego

    def movimiento_humano(self, casilla):
        if self.juego.tablero[casilla] == "-":
            self.juego.tablero[casilla] = self.letra
            self.juego.mostrar_tablero()
            if not self.juego.revisar_ganador():
                self.juego.root.after(500, self.juego.bot.movimiento_maquina)

class JugadorComputadora(TresEnRaya):
    def __init__(self, letra, juego):
        self.jugadorBot = letra
        self.jugadorHumano = "X" if letra == "O" else "O"
        self.juego = juego

    def jugadores(self, estado):
        x = sum(1 for s in estado if s == "X")
        o = sum(1 for s in estado if s == "O")
        if self.jugadorHumano == "X":
            return "X" if x == o else "O"
        return "O" if x == o else "X"

    def acciones(self, estado):
        return [i for i, x in enumerate(estado) if x == "-"]

    def resultado(self, estado, accion):
        nuevoEstado = estado.copy()
        jugador = self.jugadores(estado)
        nuevoEstado[accion] = jugador
        return nuevoEstado

    def terminal(self, estado):
        return self.juego.ganador(estado, "X") or self.juego.ganador(estado, "O")

    def minimax(self, estado, jugador):
        jugador_max = self.jugadorHumano
        otro_jugador = 'O' if jugador == 'X' else 'X'
        if self.terminal(estado):
            return {'posicion': None, 'puntuacion': 1 * (len(self.acciones(estado)) + 1) if otro_jugador == jugador_max else -1 * (len(self.acciones(estado)) + 1)}
        elif self.juego.tablero_lleno(estado):
            return {'posicion': None, 'puntuacion': 0}

        mejor = {'posicion': None, 'puntuacion': -math.inf} if jugador == jugador_max else {'posicion': None, 'puntuacion': math.inf}
        for posible_movimiento in self.acciones(estado):
            nuevoEstado = self.resultado(estado, posible_movimiento)
            sim_score = self.minimax(nuevoEstado, otro_jugador)
            sim_score['posicion'] = posible_movimiento
            if jugador == jugador_max:
                if sim_score['puntuacion'] > mejor['puntuacion']:
                    mejor = sim_score
            else:
                if sim_score['puntuacion'] < mejor['puntuacion']:
                    mejor = sim_score
        return mejor

    def movimiento_maquina(self):
        casilla = self.minimax(self.juego.tablero, self.jugadorBot)['posicion']
        self.juego.tablero[casilla] = self.jugadorBot
        self.juego.mostrar_tablero()
        self.juego.revisar_ganador()

# Iniciar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Tres en Raya")
    juego = TresEnRaya(root)
    juego.iniciar()
    root.mainloop()