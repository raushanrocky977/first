import tkinter as tk
from tkinter import messagebox
import heapq

# --- ALGORITHM LOGIC ---
def a_star_algorithm(start, goal, walls, rows, cols):
    def heuristic(a, b):
        # Manhattan Distance: abs(x1-x2) + abs(y1-y2)
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    # Priority Queue: (f_score, node_coordinates)
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    
    visited_nodes_in_order = []

    while open_set:
        current = heapq.heappop(open_set)[1]
        
        if current == goal:
            # Path reconstruct karo agar goal mil gaya
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1], visited_nodes_in_order

        if current in visited_nodes_in_order:
            continue
            
        visited_nodes_in_order.append(current)

        # 4 Directions: Up, Down, Left, Right
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Boundary check aur Wall check
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols:
                if neighbor in walls:
                    continue
                
                tentative_g_score = g_score[current] + 1
                
                if tentative_g_score < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))
                    
    return None, visited_nodes_in_order

# --- GUI APPLICATION ---
class PathfindingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Pathfinding Visualizer - A* Search")
        self.root.config(bg="#1e293b")
        
        self.rows = 20
        self.cols = 40
        self.cell_size = 25
        
        self.start_node = (5, 5)
        self.goal_node = (15, 35)
        self.walls = set()

        # Header
        self.label = tk.Label(root, text="A* Pathfinding Visualizer", font=("Segoe UI", 20, "bold"), bg="#1e293b", fg="#38bdf8")
        self.label.pack(pady=10)

        # Canvas for the Grid
        self.canvas = tk.Canvas(root, width=self.cols * self.cell_size, height=self.rows * self.cell_size, bg="white", highlightthickness=0)
        self.canvas.pack(padx=20, pady=10)

        # Controls
        self.btn_frame = tk.Frame(root, bg="#1e293b")
        self.btn_frame.pack(pady=10)

        self.start_btn = tk.Button(self.btn_frame, text="Visualize A*", command=self.start_visualization, bg="#22c55e", fg="white", font=("Segoe UI", 12, "bold"), bd=0, padx=15, pady=5)
        self.start_btn.grid(row=0, column=0, padx=10)

        self.reset_btn = tk.Button(self.btn_frame, text="Reset Board", command=self.reset_board, bg="#ef4444", fg="white", font=("Segoe UI", 12, "bold"), bd=0, padx=15, pady=5)
        self.reset_btn.grid(row=0, column=1, padx=10)

        self.draw_grid()
        
        # Mouse Bindings for Wall Drawing
        self.canvas.bind("<B1-Motion>", self.paint_wall)
        self.canvas.bind("<Button-1>", self.paint_wall)

    def draw_grid(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                color = "white"
                if (r, c) == self.start_node: color = "#22c55e" # Green
                elif (r, c) == self.goal_node: color = "#ef4444" # Red
                elif (r, c) in self.walls: color = "#0f172a" # Dark Blue/Black
                
                self.canvas.create_rectangle(c * self.cell_size, r * self.cell_size, (c + 1) * self.cell_size, (r + 1) * self.cell_size, outline="#cbd5e1", fill=color, tags=f"node-{r}-{c}")

    def paint_wall(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if 0 <= row < self.rows and 0 <= col < self.cols:
            node = (row, col)
            if node != self.start_node and node != self.goal_node:
                self.walls.add(node)
                self.canvas.itemconfig(f"node-{row}-{col}", fill="#0f172a")

    def start_visualization(self):
        path, visited = a_star_algorithm(self.start_node, self.goal_node, self.walls, self.rows, self.cols)
        
        if not path:
            messagebox.showinfo("Result", "No Path Possible!")
            return

        # Animate Visited Nodes
        for node in visited:
            if node != self.start_node and node != self.goal_node:
                self.root.after(10, self.update_cell_color(node, "#38bdf8")) # Light Blue
                self.root.update()

        # Animate Shortest Path
        for node in path:
            if node != self.goal_node:
                self.root.after(30, self.update_cell_color(node, "#facc15")) # Yellow
                self.root.update()

    def update_cell_color(self, node, color):
        r, c = node
        self.canvas.itemconfig(f"node-{r}-{c}", fill=color)

    def reset_board(self):
        self.walls.clear()
        self.draw_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingVisualizer(root)
    root.mainloop()