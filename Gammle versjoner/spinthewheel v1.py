import tkinter as tk
from tkinter import simpledialog
import random, math, time, json, os

KLASSEMAPPE = "klasser"

SEGMENT_FARGER = [
    "#FF6B6B", "#4D96FF", "#6BCB77", "#FFD93D", "#9D4EDD",
    "#30E3CA", "#F28482", "#43AA8B", "#F94144", "#277DA1",
    "#F3722C", "#90BE6D", "#577590", "#E6B8A2", "#B5179E"
]

class SpinWheelGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Spin the Wheel 🛞")

        os.makedirs(KLASSEMAPPE, exist_ok=True)

        self.klasse = None
        self.navn_liste = []
        self.siste_vinner = None

        # Klassevelger
        self.klasse_var = tk.StringVar(value="Velg klasse")
        klasser = self.hent_klasser()
        if klasser:
            self.klasse_menu = tk.OptionMenu(root, self.klasse_var, "Velg klasse", *klasser)
        else:
            self.klasse_menu = tk.OptionMenu(root, self.klasse_var, "Velg klasse")
        self.klasse_menu.pack(pady=5)

        self.klasse_var.trace_add("write", lambda *args: self.bytt_klasse(self.klasse_var.get()))

        self.new_class_button = tk.Button(root, text="Opprett ny klasse", command=self.ny_klasse)
        self.new_class_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Reset klasse", command=self.reset_klasse)
        self.reset_button.pack(pady=5)

        self.entry = tk.Entry(root, width=30)
        self.entry.pack(pady=5)

        self.add_button = tk.Button(root, text="Legg til navn", command=self.legg_til_navn)
        self.add_button.pack(pady=5)

        self.remove_button = tk.Button(root, text="Fjern valgt navn", command=self.fjern_navn)
        self.remove_button.pack(pady=5)

        self.listbox = tk.Listbox(root, width=40, height=8)
        self.listbox.pack(pady=10)

        self.spin_button = tk.Button(root, text="SPINN HJULET 🎉", command=self.spinn_hjul)
        self.spin_button.pack(pady=10)

        self.result_label = tk.Label(root, text="", font=("Arial", 14), fg="blue")
        self.result_label.pack(pady=10)

        self.canvas_size = 320
        self.canvas_padding = 12
        self.canvas = tk.Canvas(root, width=self.canvas_size, height=self.canvas_size)
        self.canvas.pack()

        self.angle_offset = 0.0
        self.tegn_hjul()

    # ---------- Klassehåndtering ----------
    def hent_klasser(self):
        return [f.replace(".json", "") for f in os.listdir(KLASSEMAPPE) if f.endswith(".json")]

    def ny_klasse(self):
        navn = simpledialog.askstring("Ny klasse", "Skriv inn klassenavn:")
        if navn:
            self.klasse = navn
            self.klasse_var.set(navn)
            self.navn_liste = []
            self.lagre_navn()
            self.oppdater_listbox()
            self.tegn_hjul()
            self.oppdater_klassemeny()

    def bytt_klasse(self, valgt):
        if valgt == "Velg klasse":
            self.klasse = None
            self.navn_liste = []
            self.oppdater_listbox()
            self.tegn_hjul()
            return
        self.klasse = valgt
        self.navn_liste = self.last_navn(self.klasse)
        self.oppdater_listbox()
        self.tegn_hjul()

    def reset_klasse(self):
        if not self.klasse:
            self.result_label.config(text="Ingen klasse valgt!")
            return
        self.navn_liste = self.last_navn(self.klasse)
        self.oppdater_listbox()
        self.tegn_hjul()
        self.result_label.config(text=f"Klassen '{self.klasse}' ble reset.")

    def oppdater_klassemeny(self):
        menu = self.klasse_menu["menu"]
        menu.delete(0, "end")
        menu.add_command(label="Velg klasse", command=lambda: self.klasse_var.set("Velg klasse"))
        for k in self.hent_klasser():
            menu.add_command(label=k, command=lambda v=k: self.klasse_var.set(v))

    # ---------- GUI-funksjoner ----------
    def oppdater_listbox(self):
        self.listbox.delete(0, tk.END)
        for navn in self.navn_liste:
            self.listbox.insert(tk.END, navn)

    def tegn_hjul(self):
        self.canvas.delete("all")
        if not self.navn_liste:
            return
        num_segments = len(self.navn_liste)
        angle_per_segment = 360 / num_segments
        center = self.canvas_size // 2
        radius = self.canvas_size // 2 - self.canvas_padding

        for i, navn in enumerate(self.navn_liste):
            start_angle = i * angle_per_segment + self.angle_offset
            color = SEGMENT_FARGER[i % len(SEGMENT_FARGER)]
            self.canvas.create_arc(
                self.canvas_padding, self.canvas_padding,
                self.canvas_size - self.canvas_padding, self.canvas_size - self.canvas_padding,
                start=start_angle, extent=angle_per_segment,
                fill=color, outline="black"
            )
            mid_deg = start_angle + angle_per_segment / 2
            mid_rad = math.radians(mid_deg)
            tx = center + (radius * 0.55) * math.cos(mid_rad)
            ty = center - (radius * 0.55) * math.sin(mid_rad)
            self.canvas.create_text(tx, ty, text=navn)

        # Pil øverst som peker ned mot hjulet
        tip_y = self.canvas_padding + 20   # spiss nedover
        base_y = self.canvas_padding - 2   # base øverst
        self.canvas.create_polygon(
            center, tip_y,          # spiss ned
            center - 12, base_y,    # venstre base
            center + 12, base_y,    # høyre base
            fill="red", outline="black"
        )

    def legg_til_navn(self):
        navn = self.entry.get().strip()
        if navn:
            self.navn_liste.append(navn)
            self.oppdater_listbox()
            self.entry.delete(0, tk.END)
            self.lagre_navn()
            self.tegn_hjul()

    def fjern_navn(self):
        valgt = self.listbox.curselection()
        if valgt:
            index = valgt[0]
            navn = self.listbox.get(index)
            self.navn_liste.remove(navn)
            self.oppdater_listbox()
            self.lagre_navn()
            self.tegn_hjul()

    def spinn_hjul(self):
        if not self.navn_liste:
            self.result_label.config(text="Ingen navn på hjulet!")
            return
        num_segments = len(self.navn_liste)
        self.angle_offset = random.uniform(0, 360)
        vinkel_hastighet = random.uniform(18, 28)
        friksjon = 0.98
        min_hastighet = 0.6
        ekstra = random.uniform(360, 1080)
        while vinkel_hastighet > min_hastighet or ekstra > 0:
            self.angle_offset = (self.angle_offset + vinkel_hastighet) % 360
            self.tegn_hjul()
            self.root.update()
            time.sleep(0.015)
            vinkel_hastighet *= friksjon
            if ekstra > 0:
                trinn = min(vinkel_hastighet, ekstra)
                ekstra -= trinn
        angle_per_segment = 360 / num_segments
        pekevinkel = (90 - self.angle_offset) % 360
        winning_index = int(pekevinkel // angle_per_segment) % num_segments
        vinner = self.navn_liste[winning_index]
        self.siste_vinner = vinner
        self.result_label.config(text=f"🎉 Vinneren er: {vinner}!")

        # Fjern vinneren automatisk fra hjulet
        self.navn_liste.remove(vinner)
        self.oppdater_listbox()
        self.tegn_hjul()

    # ---------- Filhåndtering ----------
    def lagre_navn(self):
        if not self.klasse:
            return
        fil = os.path.join(KLASSEMAPPE, f"{self.klasse}.json")
        with open(fil, "w", encoding="utf-8") as f:
            json.dump(self.navn_liste, f, ensure_ascii=False, indent=2)

    def last_navn(self, klasse):
        fil = os.path.join(KLASSEMAPPE, f"{klasse}.json")
        if os.path.exists(fil):
            try:
                with open(fil, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [str(x) for x in data if isinstance(x, str)]
            except Exception:
                return []
        return []

# Start programmet
if __name__ == "__main__":
    root = tk.Tk()
    app = SpinWheelGUI(root)
    root.mainloop()