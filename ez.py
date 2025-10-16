import tkinter as tk
import threading
import time
import keyboard
from pynput.mouse import Controller, Button

class AutoClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("lec")
        self.running = False
        self.thread = None
        self.mouse_button = tk.StringVar(value="left")

        self.root.configure(bg="black")

        tk.Label(root, text="CPS", bg="black", fg="white").grid(row=0, column=0, padx=10, pady=10)
        self.cps_entry = tk.Entry(root, bg="gray20", fg="white", insertbackground="white")
        self.cps_entry.grid(row=0, column=1, padx=10, pady=10)
        self.cps_entry.insert(0, "10")

        tk.Label(root, text="Hotkey", bg="black", fg="white").grid(row=1, column=0, padx=10, pady=10)
        self.hotkey_entry = tk.Entry(root, bg="gray20", fg="white", insertbackground="white")
        self.hotkey_entry.grid(row=1, column=1, padx=10, pady=10)
        self.hotkey_entry.insert(0, "z")

        tk.Label(root, text="Left/Right", bg="black", fg="white").grid(row=2, column=0, padx=10, pady=10)
        self.left_btn = tk.Button(root, text="Left", width=8, bg="gray30", fg="white", activebackground="gray40", activeforeground="white", command=lambda: self.select_button("left"))
        self.left_btn.grid(row=2, column=1, sticky="w", padx=4)
        self.right_btn = tk.Button(root, text="Right", width=8, bg="gray30", fg="white", activebackground="gray40", activeforeground="white", command=lambda: self.select_button("right"))
        self.right_btn.grid(row=2, column=1, sticky="e", padx=4)
        self.select_button("left")

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        threading.Thread(target=self.listen_hotkey, daemon=True).start()

    def select_button(self, value):
        self.mouse_button.set(value)
        if value == "left":
            self.left_btn.config(bg="gray60")
            self.right_btn.config(bg="gray30")
        else:
            self.right_btn.config(bg="gray60")
            self.left_btn.config(bg="gray30")

    def autoclick(self, cps, button):
        mouse = Controller()
        delay = 1.0 / cps
        btn = Button.left if button == "left" else Button.right
        while self.running:
            mouse.click(btn)
            time.sleep(delay)

    def listen_hotkey(self):
        last_state = False
        while True:
            if keyboard.is_pressed("insert"):
                self.on_close()
                break
            hotkey = self.hotkey_entry.get().strip().lower()
            button = self.mouse_button.get()
            try:
                cps = float(self.cps_entry.get())
            except:
                cps = 10
            if keyboard.is_pressed(hotkey):
                if not self.running and not last_state:
                    self.running = True
                    self.thread = threading.Thread(target=self.autoclick, args=(cps, button), daemon=True)
                    self.thread.start()
                    last_state = True
                    time.sleep(0.3)
                elif self.running and not last_state:
                    self.running = False
                    last_state = True
                    time.sleep(0.3)
            else:
                last_state = False
            time.sleep(0.01)

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoClickerApp(root)
    root.mainloop()
