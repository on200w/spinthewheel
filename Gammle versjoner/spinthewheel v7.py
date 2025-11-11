import importlib
import subprocess
import sys

# Sjekk og installer nødvendige pakker
REQUIRED_PACKAGES = ["customtkinter"]

def ensure_packages():
    for pkg in REQUIRED_PACKAGES:
        try:
            importlib.import_module(pkg)
        except ImportError:
            print(f"Pakke '{pkg}' mangler. Installerer...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

ensure_packages()

import customtkinter as ctk
import tkinter as tk
import random, math, time, json, os

KLASSEMAPPE = "klasser"

class SpinWheelGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Spin the Wheel 🛞")

        # Mørkt tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        os.makedirs(KLASSEMAPPE, exist_ok=True)

        self.klasse = None
        self.navn_liste = []
        self.siste_vinner = None
        self.konfetti = []
        self.spinning = False

        # Toppramme
        top_frame = ctk.CTkFrame(self, fg_color="#323333")
        top_frame.pack(fill="x", pady=10)

        self.klasse_var = tk.StringVar(value="Velg klasse")
        self.klasse_menu = ctk.CTkOptionMenu(top_frame, variable=self.klasse_var,
                                             values=self.hent_klasser() or ["Velg klasse"],
                                             command=self.bytt_klasse)
        self.klasse_menu.pack(side="left", padx=5)

        ctk.CTkButton(top_frame, text="Opprett ny klasse", command=self.ny_klasse).pack(side="left", padx=5)
        ctk.CTkButton(top_frame, text="Reset klasse", command=self.reset_klasse).pack(side="left", padx=5)

        # Hovedramme
        main_frame = ctk.CTkFrame(self, fg_color="#323333")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Venstre side: navneliste
        list_frame = ctk.CTkFrame(main_frame, fg_color="#323333")
        list_frame.pack(side="left", fill="y", padx=10)

        self.listbox = tk.Listbox(list_frame, font=("Segoe UI", 12), height=20, width=20,
                                  bg="#3A3A3A", fg="white", highlightthickness=0, bd=0)
        self.listbox.pack(side="left", fill="y")

        self.entry = ctk.CTkEntry(list_frame, placeholder_text="Skriv navn")
        self.entry.pack(pady=5)

        ctk.CTkButton(list_frame, text="Legg til", command=self.legg_til_navn).pack(pady=5)
        ctk.CTkButton(list_frame, text="Fjern", command=self.fjern_navn).pack(pady=5)

        # Høyre side: hjul
        wheel_frame = ctk.CTkFrame(main_frame, fg_color="#323333")
        wheel_frame.pack(side="left", fill="both", expand=True, padx=20)

        self.result_label = ctk.CTkLabel(wheel_frame, text="", font=("Segoe UI", 20, "bold"), text_color="white")
        self.result_label.pack(pady=10)

        self.spin_button = ctk.CTkButton(wheel_frame, text="SPINN HJULET 🎉", command=self.spinn_hjul)
        self.spin_button.pack(pady=10)

        self.canvas_size = 500
        self.canvas_padding = 20

        self.wheel_canvas = tk.Canvas(
            wheel_frame,
            width=self.canvas_size,
            height=self.canvas_size,
            bg="#323333",
            highlightthickness=0
        )
        self.wheel_canvas.pack(expand=True)

        self.angle_offset = 0.0
        self.tegn_hjul()

        self.after(100, lambda: self.state("zoomed"))

    # ---------- Klassehåndtering ----------
    def hent_klasser(self):
        return [f.replace(".json", "") for f in os.listdir(KLASSEMAPPE) if f.endswith(".json")]

    def ny_klasse(self):
        navn = ctk.CTkInputDialog(text="Skriv inn klassenavn:", title="Ny klasse").get_input()
        if navn:
            self.klasse = navn
            self.klasse_var.set(navn)
            self.navn_liste = []
            self.lagre_navn()
            self.oppdater_listbox()
            self.tegn_hjul()
            self.klasse_menu.configure(values=self.hent_klasser())

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
            self.result_label.configure(text="Ingen klasse valgt!")
            return
        self.navn_liste = self.last_navn(self.klasse)
        self.oppdater_listbox()
        self.tegn_hjul()
        self.result_label.configure(text=f"Klassen '{self.klasse}' ble reset.")

    # ---------- GUI-funksjoner ----------
    def oppdater_listbox(self):
        self.listbox.delete(0, tk.END)
        for navn in self.navn_liste:
            self.listbox.insert(tk.END, navn)

        # Hvis det bare er ett navn igjen, vis popup automatisk
        if len(self.navn_liste) == 1:
            self.siste_vinner = self.navn_liste[0]
            self.vis_siste_vinner(self.siste_vinner)

    def tegn_hjul(self):
        self.wheel_canvas.delete("all")
        if not self.navn_liste:
            return
        num_segments = len(self.navn_liste)
        angle_per_segment = 360 / num_segments
        center = self.canvas_size // 2
        radius = self.canvas_size // 2 - self.canvas_padding

        colors = [
            "#BF616A", "#5E81AC", "#A3BE8C", "#EBCB8B", "#B48EAD",
            "#FF6F61", "#6A0572", "#00BFFF", "#FF1493", "#32CD32",
            "#FFA500", "#00CED1", "#FFD700", "#DC143C", "#8A2BE2",
            "#FF4500", "#7FFF00", "#40E0D0", "#FF69B4", "#1E90FF"
        ]

        for i, navn in enumerate(self.navn_liste):
            start_angle = i * angle_per_segment + self.angle_offset
            color = colors[i % len(colors)]
            self.wheel_canvas.create_arc(
                self.canvas_padding, self.canvas_padding,
                self.canvas_size - self.canvas_padding, self.canvas_size - self.canvas_padding,
                start=start_angle, extent=angle_per_segment,
                fill=color, outline="#323333"
            )
            mid_deg = start_angle + angle_per_segment / 2
            mid_rad = math.radians(mid_deg)
            tx = center + (radius * 0.65) * math.cos(mid_rad)
            ty = center - (radius * 0.65) * math.sin(mid_rad)
            self.wheel_canvas.create_text(tx, ty, text=navn, font=("Segoe UI", 14, "bold"), fill="white")

        tip_y = self.canvas_padding + 30
        base_y = self.canvas_padding - 2
        self.wheel_canvas.create_polygon(
            center, tip_y,
            center - 15, base_y,
            center + 15, base_y,
            fill="red", outline="black", width=3
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
        if self.spinning:
            return
        if not self.navn_liste:
            self.result_label.configure(text="Ingen navn på hjulet!")
            return

        if len(self.navn_liste) == 1:
            self.siste_vinner = self.navn_liste[0]
            self.vis_siste_vinner(self.siste_vinner)
            return

        self.spinning = True
        self.spin_button.configure(state="disabled")

        num_segments = len(self.navn_liste)
        self.angle_offset = random.uniform(0, 360)
        vinkel_hastighet = random.uniform(18, 28)
        friksjon = 0.98
        min_hastighet = 0.6
        ekstra = random.uniform(360, 1080)

        while vinkel_hastighet > min_hastighet or ekstra > 0:
            self.angle_offset = (self.angle_offset + vinkel_hastighet) % 360
            self.tegn_hjul()
            self.update()
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
        self.result_label.configure(text=f"🎉 Vinneren er: {vinner}!")

        # Start konfetti – spinneknapp forblir låst til fjerning er ferdig
        self.vis_konfetti()

    # ---------- Konfetti på wheel_canvas ----------
    def vis_konfetti(self):
        for pid, *_ in self.konfetti:
            self.wheel_canvas.delete(pid)
        self.konfetti = []

        farger = ["#FFD166", "#EF476F", "#06D6A0", "#118AB2", "#FFFFFF", "#9C27B0", "#00E5FF"]

        width = self.wheel_canvas.winfo_width()
        height = self.wheel_canvas.winfo_height()

        for _ in range(200):
            x = random.randint(0, width)
            y = random.randint(0, 40)
            r = random.randint(3, 6)
            farge = random.choice(farger)
            pid = self.wheel_canvas.create_oval(x-r, y-r, x+r, y+r, fill=farge, outline="")
            vx = random.uniform(-2, 2)
            vy = random.uniform(2.0, 5.0)
            gravity = random.uniform(0.05, 0.1)
            self.konfetti.append([pid, vx, vy, gravity])

        self.animer_konfetti()

    def animer_konfetti(self):
        if not self.konfetti:
            self.fjern_vinner_automatisk()
            return

        levende = []
        height = self.wheel_canvas.winfo_height()
        for pid, vx, vy, gravity in self.konfetti:
            vy += gravity
            self.wheel_canvas.move(pid, vx, vy)
            coords = self.wheel_canvas.coords(pid)
            if coords and coords[1] < height + 10:
                levende.append([pid, vx, vy, gravity])
            else:
                self.wheel_canvas.delete(pid)

        self.konfetti = levende
        if self.konfetti:
            self.after(16, self.animer_konfetti)
        else:
            self.fjern_vinner_automatisk()

    def fjern_vinner_automatisk(self):
        if self.siste_vinner and self.siste_vinner in self.navn_liste:
            self.navn_liste.remove(self.siste_vinner)
            self.oppdater_listbox()
            self.tegn_hjul()

        # Hvis listen nå er tom, vis popup med siste vinner
        if not self.navn_liste and self.siste_vinner:
            self.vis_siste_vinner(self.siste_vinner)

        self.siste_vinner = None
        self.result_label.configure(text="")
        self.spinning = False
        self.spin_button.configure(state="normal")

    # ---------- Popup for siste vinner ----------
    def vis_siste_vinner(self, navn):
        popup = ctk.CTkToplevel(self)
        popup.title("Siste vinner")

        # Sett størrelse og plasser midt på skjermen
        w, h = 400, 200
        ws = popup.winfo_screenwidth()
        hs = popup.winfo_screenheight()
        x = (ws // 2) - (w // 2)
        y = (hs // 2) - (h // 2)
        popup.geometry(f"{w}x{h}+{x}+{y}")

        label = ctk.CTkLabel(popup, text=f"🎉 Siste vinner er: {navn} 🎉",
                             font=("Segoe UI", 24, "bold"), text_color="white")
        label.pack(pady=40)

        def reset_og_lukk():
            self.reset_klasse()
            popup.destroy()

        reset_btn = ctk.CTkButton(popup, text="Reset klasse", command=reset_og_lukk)
        reset_btn.pack(pady=20)

        # Sørg for at popupen havner foran og låser hovedvinduet
        popup.lift()
        popup.focus_force()
        popup.grab_set()

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
    app = SpinWheelGUI()
    app.mainloop()