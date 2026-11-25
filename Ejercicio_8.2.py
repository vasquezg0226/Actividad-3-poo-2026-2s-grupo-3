import math
import tkinter as tk
from tkinter import messagebox

NUM_NOTAS = 5
NOTA_MIN = 0.0  
NOTA_MAX = 5.0

class VentanaNotas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Notas del estudiante")
        self.resizable(False, False)

        self.entradas = []
        self._crear_panel_ingreso()
        self._crear_panel_resultados()

    # Interfaz
    def _crear_panel_ingreso(self):
        panel = tk.LabelFrame(self, text="Ingreso de notas", padx=10, pady=10)
        panel.pack(padx=10, pady=10, fill="x")

        for i in range(NUM_NOTAS):
            tk.Label(panel, text=f"Nota {i + 1}:").grid(row=i, column=0, sticky="e", pady=3)
            entrada = tk.Entry(panel, width=12, justify="center")
            entrada.grid(row=i, column=1, padx=8, pady=3)
            self.entradas.append(entrada)

        botones = tk.Frame(panel)
        botones.grid(row=NUM_NOTAS, column=0, columnspan=2, pady=(10, 0))
        tk.Button(botones, text="Calcular", command=self.calcular).pack(side="left", padx=5)
        tk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        self.entradas[0].focus()

    def _crear_panel_resultados(self):
        panel = tk.LabelFrame(self, text="Resultados", padx=10, pady=10)
        panel.pack(padx=10, pady=(0, 10), fill="x")

        self.lbl_promedio = tk.Label(panel, text="Promedio: -", anchor="w")
        self.lbl_desviacion = tk.Label(panel, text="Desviación estándar: -", anchor="w")
        self.lbl_mayor = tk.Label(panel, text="Mayor nota: -", anchor="w")
        self.lbl_menor = tk.Label(panel, text="Menor nota: -", anchor="w")

        for lbl in (self.lbl_promedio, self.lbl_desviacion, self.lbl_mayor, self.lbl_menor):
            lbl.pack(fill="x", pady=2)

    # Eventos 
    def calcular(self):
        notas = self._leer_notas()
        if notas is None:
            return

        promedio = sum(notas) / len(notas)
        varianza = sum((n - promedio) ** 2 for n in notas) / len(notas)
        desviacion = math.sqrt(varianza)  # desviación estándar poblacional

        self.lbl_promedio.config(text=f"Promedio: {promedio:.2f}")
        self.lbl_desviacion.config(text=f"Desviación estándar: {desviacion:.2f}")
        self.lbl_mayor.config(text=f"Mayor nota: {max(notas):.2f}")
        self.lbl_menor.config(text=f"Menor nota: {min(notas):.2f}")

    def limpiar(self):
        for entrada in self.entradas:
            entrada.delete(0, tk.END)
        self.lbl_promedio.config(text="Promedio: -")
        self.lbl_desviacion.config(text="Desviación estándar: -")
        self.lbl_mayor.config(text="Mayor nota: -")
        self.lbl_menor.config(text="Menor nota: -")
        self.entradas[0].focus()

    # Utilidades 
    def _leer_notas(self):
        notas = []
        for i, entrada in enumerate(self.entradas, start=1):
            texto = entrada.get().strip().replace(",", ".")
            try:
                valor = float(texto)
            except ValueError:
                messagebox.showerror("Dato inválido", f"La nota {i} no es un número válido.")
                entrada.focus()
                return None
            if not (NOTA_MIN <= valor <= NOTA_MAX):
                messagebox.showerror(
                    "Fuera de rango",
                    f"La nota {i} debe estar entre {NOTA_MIN} y {NOTA_MAX}.",
                )
                entrada.focus()
                return None
            notas.append(valor)
        return notas


if __name__ == "__main__":
    VentanaNotas().mainloop()