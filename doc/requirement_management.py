import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os

class Requirement:
    def __init__(self, req_id, indication, content, parent=None):
        self.req_id = req_id
        self.indication = indication
        self.content = content
        self.parent = parent
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        return {
            'req_id': self.req_id,
            'indication': self.indication,
            'content': self.content,
            'parent': self.parent.req_id if self.parent else None,
            'children': [child.req_id for child in self.children]
        }

class RequirementManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Requirement Manager")
        self.master.geometry("800x600")
        self.master.configure(bg="#f0f0f0")
        
        self.requirements = []
        self.db_file = "requirements.txt"

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TLabel", background="#f0f0f0", font=("Arial", 10))
        self.style.configure("TButton", font=("Arial", 10, "bold"))
        self.style.configure("Treeview", font=("Arial", 9))
        self.style.configure("Treeview.Heading", font=("Arial", 10, "bold"))

        self.create_widgets()
        self.load_database()
        self.update_treeview()
        self.update_parent_combobox()

    def create_widgets(self):
        main_frame = ttk.Frame(self.master, padding="20 20 20 20", style="TFrame")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Input Frame
        input_frame = ttk.Frame(main_frame, padding="10 10 10 10", relief="groove", borderwidth=2)
        input_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))

        ttk.Label(input_frame, text="Requirement ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.req_id_entry = ttk.Entry(input_frame, width=20)
        self.req_id_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Parent/Child:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.indication_var = tk.StringVar()
        ttk.Combobox(input_frame, textvariable=self.indication_var, values=["Parent", "Child"], width=18).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Content:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.content_entry = ttk.Entry(input_frame, width=60)
        self.content_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Parent ID:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.parent_var = tk.StringVar()
        self.parent_combobox = ttk.Combobox(input_frame, textvariable=self.parent_var, width=18)
        self.parent_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)

        ttk.Button(button_frame, text="Add/Modify Requirement", command=self.add_or_modify_requirement, style="TButton").grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Draw Tree", command=self.draw_tree, style="TButton").grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Save to File", command=self.save_to_file, style="TButton").grid(row=0, column=2, padx=(0, 10))
        ttk.Button(button_frame, text="Open Database", command=self.open_database, style="TButton").grid(row=0, column=3)

        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Indication", "Content", "Parent"), show="headings", style="Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Indication", text="Indication")
        self.tree.heading("Content", text="Content")
        self.tree.heading("Parent", text="Parent")
        
        self.tree.column("ID", width=100, anchor=tk.W)
        self.tree.column("Indication", width=100, anchor=tk.W)
        self.tree.column("Content", width=300, anchor=tk.W)
        self.tree.column("Parent", width=100, anchor=tk.W)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        tree_frame.columnconfigure(0, weight=1)
        tree_frame.rowconfigure(0, weight=1)

        self.tree.bind("<Double-1>", self.on_tree_double_click)

    def add_or_modify_requirement(self):
        req_id = self.req_id_entry.get()
        indication = self.indication_var.get()
        content = self.content_entry.get()
        parent_id = self.parent_var.get()

        if not req_id or not indication or not content:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        existing_req = next((req for req in self.requirements if req.req_id == req_id), None)
        parent = next((req for req in self.requirements if req.req_id == parent_id), None)

        if existing_req:
            # Modify existing requirement
            existing_req.indication = "Parent" if indication == "Master" else parent_id
            existing_req.content = content
            if existing_req.parent:
                existing_req.parent.children.remove(existing_req)
            existing_req.parent = parent
            if parent:
                parent.add_child(existing_req)
        else:
            # Add new requirement
            new_req = Requirement(req_id, "Parent" if indication == "Master" else parent_id, content, parent)
            self.requirements.append(new_req)
            if parent:
                parent.add_child(new_req)

        self.update_treeview()
        self.update_parent_combobox()
        self.clear_entries()
        self.save_database()

    def update_treeview(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for req in self.requirements:
            indication_display = self.get_indication_display(req)
            self.tree.insert("", "end", values=(req.req_id, indication_display, req.content, req.parent.req_id if req.parent else ""))

    def get_indication_display(self, req):
        if req.indication == "Parent" or req.indication == "Master":
            return "Master"
        else:
            return req.indication

    def update_parent_combobox(self):
        parent_ids = [req.req_id for req in self.requirements]
        self.parent_combobox['values'] = parent_ids

    def clear_entries(self):
        self.req_id_entry.delete(0, tk.END)
        self.indication_var.set("")
        self.content_entry.delete(0, tk.END)
        self.parent_var.set("")

    def on_tree_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        
        # Clear previous data
        self.req_id_entry.delete(0, tk.END)
        self.indication_var.set("")
        self.content_entry.delete(0, tk.END)
        self.parent_var.set("")
        
        # Populate with new data
        self.req_id_entry.insert(0, values[0])
        self.indication_var.set("Parent" if values[1] == "Master" else "Child")
        self.content_entry.insert(0, values[2])
        self.parent_var.set(values[3] if values[3] != "None" else "")

    def draw_tree(self):
        if not self.requirements:
            messagebox.showinfo("Info", "No requirements to draw")
            return

        root = Node("Requirements")
        node_dict = {"Requirements": root}

        for req in self.requirements:
            parent_node = node_dict.get(req.parent.req_id if req.parent else "Requirements")
            node = Node(req.req_id, parent=parent_node)
            node_dict[req.req_id] = node

        dot_exporter = DotExporter(root, 
                                   options=["rankdir=TB", "splines=curved"],
                                   nodeattrfunc=lambda node: "shape=box")
        dot_exporter.to_dotfile("requirement_tree.dot")
        messagebox.showinfo("Success", "Tree saved as 'requirement_tree.dot'. Use Graphviz to visualize.")

    def save_to_file(self):
        if not self.requirements:
            messagebox.showinfo("Info", "No requirements to save")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if not file_path:
            return

        with open(file_path, 'w') as f:
            for req in self.requirements:
                parent = req.parent.req_id if req.parent else "None"
                children = ", ".join([child.req_id for child in req.children]) or "None"
                indication = self.get_indication_display(req)
                f.write(f"Requirement ID: {req.req_id}\n")
                f.write(f"Indication: {indication}\n")
                f.write(f"Content: {req.content}\n")
                f.write(f"Parent: {parent}\n")
                f.write(f"Children: {children}\n\n")

        messagebox.showinfo("Success", f"Requirements saved to {file_path}")

    def save_database(self):
        try:
            with open(self.db_file, 'w') as f:
                for req in self.requirements:
                    f.write(f"Requirement ID: {req.req_id}\n")
                    f.write(f"Indication: {self.get_indication_display(req)}\n")
                    f.write(f"Content: {req.content}\n")
                    f.write(f"Parent: {req.parent.req_id if req.parent else 'None'}\n")
                    children = ', '.join([child.req_id for child in req.children]) if req.children else 'None'
                    f.write(f"Children: {children}\n\n")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while saving the database: {str(e)}")

    def open_database(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if file_path:
            self.db_file = file_path
            self.requirements.clear()
            self.load_database()
            self.update_treeview()
            self.update_parent_combobox()
            messagebox.showinfo("Success", f"Database loaded from {self.db_file}")

    def load_database(self):
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r') as f:
                    lines = f.readlines()

                current_req = None
                for line in lines:
                    line = line.strip()
                    if line.startswith("Requirement ID:"):
                        if current_req:
                            self.requirements.append(current_req)
                        req_id = line.split(":")[1].strip()
                        current_req = Requirement(req_id, "", "")
                    elif line.startswith("Indication:"):
                        current_req.indication = line.split(":")[1].strip()
                    elif line.startswith("Content:"):
                        current_req.content = line.split(":")[1].strip()
                    elif line.startswith("Parent:"):
                        parent_id = line.split(":")[1].strip()
                        if parent_id != "None":
                            parent = next((r for r in self.requirements if r.req_id == parent_id), None)
                            if parent:
                                current_req.parent = parent
                                parent.children.append(current_req)
                    elif line.startswith("Children:"):
                        children_ids = line.split(":")[1].strip()
                        if children_ids != "None":
                            for child_id in children_ids.split(", "):
                                child = next((r for r in self.requirements if r.req_id == child_id), None)
                                if child:
                                    current_req.children.append(child)

                if current_req:
                    self.requirements.append(current_req)

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred while loading the database: {str(e)}")
        else:
            messagebox.showinfo("Info", "No existing database found. Starting with an empty database.")

if __name__ == "__main__":
    root = tk.Tk()
    app = RequirementManager(root)
    root.mainloop()