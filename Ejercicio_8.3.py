import math
import tkinter as tk
from abc import ABC, abstractmethod
from tkinter import ttk, messagebox

# Jerarquía de clases 
class Figura(ABC):
    """Clase base abstracta para las figuras geométricas."""

    NOMBRE = ""
    CAMPOS = []  # Nombres de los datos que pide cada figura

    @abstractmethod
    def volumen(self):
        pass

    @abstractmethod
    def superficie(self):
        pass

class Cilindro(Figura):
    NOMBRE = "Cilindro"
    CAMPOS = ["Radio (cm)", "Altura (cm)"]

    def __init__(self, radio, altura):
        self.radio = radio
        self.altura = altura

    def volumen(self):
        return math.pi * self.radio ** 2 * self.altura

    def superficie(self):
        return 2 * math.pi * self.radio * (self.radio + self.altura)

class Esfera(Figura):
    NOMBRE = "Esfera"
    CAMPOS = ["Radio (cm)"]

    def __init__(self, radio):
        self.radio = radio

    def volumen(self):
        return 4 / 3 * math.pi * self.radio ** 3

    def superficie(self):
        return 4 * math.pi * self.radio ** 2

class Piramide(Figura):
    """Pirámide de base cuadrada."""

    NOMBRE = "Pirámide"
    CAMPOS = ["Base (cm)", "Altura (cm)", "Apotema (cm)"]

    def __init__(self, base, altura, apotema):
        self.base = base
        self.altura = altura
        self.apotema = apotema

    def volumen(self):
        return self.base ** 2 * self.altura / 3

    def superficie(self):
        # Área de la base + 4 caras triangulares (base * apotema / 2)
        return self.base ** 2 + 2 * self.base * self.apotema

FIGURAS = {f.NOMBRE: f for f in (Cilindro, Esfera, Piramide)}

# Interfaz gráfica 
class VentanaFiguras(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Volumen y superficie de figuras")
        self.resizable(False, False)

        self.entradas = []

        # Selector de figura
        panel_sel = tk.Frame(self, padx=10, pady=10)
        panel_sel.pack(fill="x")
        tk.Label(panel_sel, text="Figura:").pack(side="left")
        self.combo = ttk.Combobox(panel_sel, values=list(FIGURAS), state="readonly", width=15)
        self.combo.pack(side="left", padx=8)
        self.combo.current(0)
        # Listener: cuando cambia la figura, se reconstruyen los campos
        self.combo.bind("<<ComboboxSelected>>", self.cambiar_figura)

        # Panel de datos (se llena dinámicamente)
        self.panel_datos = tk.LabelFrame(self, text="Datos", padx=10, pady=10)
        self.panel_datos.pack(padx=10, fill="x")

        # Botones
        botones = tk.Frame(self, pady=8)
        botones.pack()
        tk.Button(botones, text="Calcular", command=self.calcular).pack(side="left", padx=5)
        tk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        # Resultados
        panel_res = tk.LabelFrame(self, text="Resultados", padx=10, pady=10)
        panel_res.pack(padx=10, pady=(0, 10), fill="x")
        self.lbl_volumen = tk.Label(panel_res, text="Volumen: -", anchor="w")
        self.lbl_superficie = tk.Label(panel_res, text="Superficie: -", anchor="w")
        self.lbl_volumen.pack(fill="x", pady=2)
        self.lbl_superficie.pack(fill="x", pady=2)

        self.cambiar_figura()

    # Eventos 
    def cambiar_figura(self, evento=None):
        for widget in self.panel_datos.winfo_children():
            widget.destroy()
        self.entradas = []

        clase = FIGURAS[self.combo.get()]
        for i, campo in enumerate(clase.CAMPOS):
            tk.Label(self.panel_datos, text=campo + ":").grid(row=i, column=0, sticky="e", pady=3)
            entrada = tk.Entry(self.panel_datos, width=12, justify="center")
            entrada.grid(row=i, column=1, padx=8, pady=3)
            self.entradas.append(entrada)

        self.entradas[0].focus()
        self._reiniciar_resultados()

    def calcular(self):
        valores = self._leer_valores()
        if valores is None:
            return

        figura = FIGURAS[self.combo.get()](*valores)
        self.lbl_volumen.config(text=f"Volumen: {figura.volumen():.2f} cm³")
        self.lbl_superficie.config(text=f"Superficie: {figura.superficie():.2f} cm²")

    def limpiar(self):
        for entrada in self.entradas:
            entrada.delete(0, tk.END)
        self._reiniciar_resultados()
        self.entradas[0].focus()

    # Utilidades
    def _reiniciar_resultados(self):
        self.lbl_volumen.config(text="Volumen: -")
        self.lbl_superficie.config(text="Superficie: -")

    def _leer_valores(self):
        clase = FIGURAS[self.combo.get()]
        valores = []
        for campo, entrada in zip(clase.CAMPOS, self.entradas):
            texto = entrada.get().strip().replace(",", ".")
            try:
                valor = float(texto)
            except ValueError:
                messagebox.showerror("Dato inválido", f"'{campo}' no es un número válido.")
                entrada.focus()
                return None
            if valor <= 0:
                messagebox.showerror("Dato inválido", f"'{campo}' debe ser mayor que cero.")
                entrada.focus()
                return None
            valores.append(valor)
        return valores

if __name__ == "__main__":
    VentanaFiguras().mainloop()