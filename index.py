import tkinter as tk
from tkinter import ttk

class TowerOfHanoi:
    def __init__(self, root):
        self.root = root
        self.root.title("Tower of Hanoi Visual Simulator")
        self.root.geometry("850x550")
        self.root.configure(bg="#182848")

        self.n = 3
        self.towers = [[], [], []]
        self.moves = 0
        self.solution = []
        self.step = 0
        self.running = False
        self.paused = False
        self.after_id = None

        tk.Label(
            root,
            text="TOWER OF HANOI",
            font=("Arial", 24, "bold"),
            bg="#182848",
            fg="#ffd166"
        ).pack(pady=10)

        controls = tk.Frame(root, bg="#182848")
        controls.pack()

        tk.Label(
            controls, text="Number of Disks:",
            bg="#182848", fg="white"
        ).pack(side="left", padx=5)

        self.disk_choice = ttk.Combobox(
            controls,
            values=[3, 4, 5, 6, 7],
            width=5,
            state="readonly"
        )
        self.disk_choice.set(3)
        self.disk_choice.pack(side="left", padx=5)
        self.disk_choice.bind(
            "<<ComboboxSelected>>",
            lambda event: self.reset()
        )

        self.start_btn = tk.Button(
            controls, text="Start",
            command=self.start,
            bg="#06d6a0", width=9
        )
        self.start_btn.pack(side="left", padx=5)

        self.pause_btn = tk.Button(
            controls, text="Pause",
            command=self.pause,
            bg="#ffd166", width=9
        )
        self.pause_btn.pack(side="left", padx=5)

        tk.Button(
            controls, text="Reset",
            command=self.reset,
            bg="#ef476f", fg="white", width=9
        ).pack(side="left", padx=5)

        self.canvas = tk.Canvas(
            root,
            width=800,
            height=340,
            bg="#f5f7fa",
            highlightthickness=0
        )
        self.canvas.pack(pady=15)

        self.status = tk.Label(
            root,
            text="Click Start to solve the puzzle!",
            font=("Arial", 12),
            bg="#182848",
            fg="white"
        )
        self.status.pack()

        self.counter = tk.Label(
            root, text="Moves: 0 | Minimum Moves: 7",
            font=("Arial", 14, "bold"),
            bg="#182848", fg="#ffd166"
        )
        self.counter.pack(pady=8)

        self.reset()

    def generate_moves(self, n, source, auxiliary, target):
        if n == 0:
            return

        self.generate_moves(
            n - 1, source, target, auxiliary
        )
        self.solution.append((source, target))
        self.generate_moves(
            n - 1, auxiliary, source, target
        )

    def draw(self):
        self.canvas.delete("all")

        positions = [150, 400, 650]
        base_y = 300

        for i, x in enumerate(positions):
            self.canvas.create_rectangle(
                x - 5, 90, x + 5, base_y,
                fill="#8d5524", outline=""
            )
            self.canvas.create_rectangle(
                x - 100, base_y, x + 100, base_y + 12,
                fill="#8d5524", outline=""
            )
            self.canvas.create_text(
                x, 325,
                text=f"Tower {'ABC'[i]}",
                font=("Arial", 13, "bold"),
                fill="#182848"
            )

            for j, disk in enumerate(self.towers[i]):
                width = 30 + disk * 22
                y = base_y - (j + 1) * 25

                color = [
                    "#ef476f", "#ffd166", "#06d6a0",
                    "#118ab2", "#9b5de5", "#f15bb5",
                    "#fb8500"
                ][(disk - 1) % 7]

                self.canvas.create_rectangle(
                    x - width // 2, y,
                    x + width // 2, y + 22,
                    fill=color,
                    outline="white",
                    width=2
                )

                self.canvas.create_text(
                    x, y + 11,
                    text=str(disk),
                    fill="white",
                    font=("Arial", 10, "bold")
                )

    def reset(self):
        if self.after_id is not None:
            self.root.after_cancel(self.after_id)
            self.after_id = None

        self.running = False
        self.paused = False
        self.n = int(self.disk_choice.get())
        self.towers = [
            list(range(self.n, 0, -1)), [], []
        ]
        self.moves = 0
        self.step = 0
        self.solution = []

        self.pause_btn.config(text="Pause")
        self.start_btn.config(state="normal")

        minimum = 2 ** self.n - 1
        self.counter.config(
            text=f"Moves: 0 | Minimum Moves: {minimum}"
        )
        self.status.config(text="Ready to solve the puzzle!")

        self.draw()

    def start(self):
        if self.running:
            return

        self.solution = []
        self.generate_moves(self.n, 0, 1, 2)
        self.step = 0
        self.running = True
        self.paused = False

        self.start_btn.config(state="disabled")
        self.pause_btn.config(text="Pause")
        self.status.config(text="Solving the puzzle...")
        self.animate()

    def animate(self):
        if not self.running or self.paused:
            return

        if self.step >= len(self.solution):
            self.running = False
            self.after_id = None
            self.start_btn.config(state="normal")
            self.status.config(text="Puzzle Solved Successfully!")
            return

        source, target = self.solution[self.step]
        disk = self.towers[source].pop()
        self.towers[target].append(disk)

        self.moves += 1
        self.step += 1

        self.counter.config(
            text=(
                f"Moves: {self.moves} | "
                f"Minimum Moves: {2 ** self.n - 1}"
            )
        )

        self.status.config(
            text=(
                f"Move disk {disk}: "
                f"Tower {'ABC'[source]} to Tower {'ABC'[target]}"
            )
        )

        self.draw()
        self.after_id = self.root.after(700, self.animate)

    def pause(self):
        if not self.running:
            return

        if not self.paused:
            self.paused = True
            if self.after_id is not None:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            self.pause_btn.config(text="Resume")
            self.status.config(text="Animation Paused")
        else:
            self.paused = False
            self.pause_btn.config(text="Pause")
            self.status.config(text="Solving the puzzle...")
            self.animate()


if __name__ == "__main__":
    root = tk.Tk()
    app = TowerOfHanoi(root)
    root.mainloop()