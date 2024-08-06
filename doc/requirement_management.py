import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
import os

class Requirement:
    def __init__(self, req_id, indication, content, parent=None, status="Pending"):
        self.req_id = req_id
        self.indication = indication
        self.content = content
        self.parent = parent
        self.children = []
        self.status = status

    def add_child(self, child):
        self.children.append(child)

    def to_dict(self):
        return {
            'req_id': self.req_id,
            'indication': self.indication,
            'content': self.content,
            'parent': self.parent.req_id if self.parent else None,
            'children': [child.req_id for child in self.children],
            'status': self.status
        }

class RequirementManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Requirement Manager")
        self.master.geometry("1000x700")
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

        # ttk.Label(input_frame, text="Parent/Child:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        # self.indication_var = tk.StringVar()
        # ttk.Combobox(input_frame, textvariable=self.indication_var, values=["Parent", "Child"], width=18).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Parent:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.indication_var = tk.StringVar()
        ttk.Combobox(input_frame, textvariable=self.indication_var, values=["Parent", "Child"], width=18).grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Content:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.content_entry = ttk.Entry(input_frame, width=60)
        self.content_entry.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Parent ID:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.parent_var = tk.StringVar()
        self.parent_combobox = ttk.Combobox(input_frame, textvariable=self.parent_var, width=18)
        self.parent_combobox.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

        ttk.Label(input_frame, text="Status:").grid(row=2, column=2, padx=5, pady=5, sticky=tk.W)
        self.status_var = tk.StringVar()
        ttk.Combobox(input_frame, textvariable=self.status_var, values=["Pending", "In progress", "Completed"], width=18).grid(row=2, column=3, padx=5, pady=5, sticky=tk.W)

        # Button Frame
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20), sticky=tk.W)

        ttk.Button(button_frame, text="Add/Modify Requirement", command=self.add_or_modify_requirement, style="TButton").grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Delete Requirement", command=self.delete_requirement, style="TButton").grid(row=0, column=1, padx=(0, 10))
        ttk.Button(button_frame, text="Draw Tree", command=self.draw_tree, style="TButton").grid(row=0, column=2, padx=(0, 10))
        ttk.Button(button_frame, text="Save to File", command=self.save_to_file, style="TButton").grid(row=0, column=3, padx=(0, 10))
        ttk.Button(button_frame, text="Open Database", command=self.open_database, style="TButton").grid(row=0, column=4)

        # Search and Filter Frame
        search_frame = ttk.Frame(main_frame)
        search_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20), sticky=(tk.W, tk.E))

        ttk.Label(search_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        ttk.Button(search_frame, text="Search", command=self.search_requirements, style="TButton").grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(search_frame, text="Filter by ID:").grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        self.filter_entry = ttk.Entry(search_frame, width=20)
        self.filter_entry.grid(row=0, column=4, padx=5, pady=5, sticky=tk.W)
        ttk.Button(search_frame, text="Apply Filter", command=self.filter_requirements, style="TButton").grid(row=0, column=5, padx=5, pady=5)
        ttk.Button(search_frame, text="Clear Filter", command=self.clear_filter, style="TButton").grid(row=0, column=6, padx=5, pady=5)

        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)

        # self.tree = ttk.Treeview(tree_frame, columns=("ID", "Indication", "Content", "Parent", "Status"), show="headings", style="Treeview")
        self.tree = ttk.Treeview(tree_frame, columns=("ID", "Parent", "Content", "Status"), show="headings", style="Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Parent", text="Parent")
        self.tree.heading("Content", text="Content")
        # self.tree.heading("Parent", text="Parent")
        self.tree.heading("Status", text="Status")
        
        self.tree.column("ID", width=100, anchor=tk.W)
        self.tree.column("Parent", width=100, anchor=tk.W)
        self.tree.column("Content", width=300, anchor=tk.W)
        # self.tree.column("Parent", width=100, anchor=tk.W)
        self.tree.column("Status", width=100, anchor=tk.W)

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
        status = self.status_var.get()

        if not req_id or not indication or not content or not status:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        existing_req = next((req for req in self.requirements if req.req_id == req_id), None)
        parent = next((req for req in self.requirements if req.req_id == parent_id), None)

        if existing_req:
            # Modify existing requirement
            existing_req.indication = "Parent" if indication == "Master" else parent_id
            existing_req.content = content
            existing_req.status = status
            if existing_req.parent:
                existing_req.parent.children.remove(existing_req)
            existing_req.parent = parent
            if parent:
                parent.add_child(existing_req)
        else:
            # Add new requirement
            new_req = Requirement(req_id, "Parent" if indication == "Master" else parent_id, content, parent, status)
            self.requirements.append(new_req)
            if parent:
                parent.add_child(new_req)

        self.update_treeview()
        self.update_parent_combobox()
        self.clear_entries()
        self.save_database()

    def delete_requirement(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Warning", "Please select a requirement to delete")
            return

        req_id = self.tree.item(selected_items[0])['values'][0]
        req_to_delete = next((req for req in self.requirements if req.req_id == req_id), None)

        if req_to_delete:
            if req_to_delete.children:
                confirm = messagebox.askyesno("Warning", f"Requirement {req_id} has children. Deleting it will also delete all its children. Are you sure you want to proceed?")
                if not confirm:
                    return

            self.delete_req_recursive(req_to_delete)
            if req_to_delete.parent:
                req_to_delete.parent.children.remove(req_to_delete)
            self.requirements.remove(req_to_delete)

            self.update_treeview()
            self.update_parent_combobox()
            self.save_database()
            messagebox.showinfo("Success", f"Requirement {req_id} and its children have been deleted")
        else:
            messagebox.showerror("Error", f"Requirement {req_id} not found")

    def delete_req_recursive(self, req):
        for child in req.children:
            self.delete_req_recursive(child)
            self.requirements.remove(child)

    def search_requirements(self):
        search_term = self.search_entry.get().lower()
        if not search_term:
            self.update_treeview()
            return

        filtered_reqs = [req for req in self.requirements if 
                         search_term in req.req_id.lower() or 
                         search_term in req.content.lower() or 
                         search_term in req.status.lower()]
        self.update_treeview(filtered_reqs)

    def filter_requirements(self):
        filter_term = self.filter_entry.get().lower()
        if not filter_term:
            self.update_treeview()
            return

        filtered_reqs = [req for req in self.requirements if filter_term in req.req_id.lower()]
        self.update_treeview(filtered_reqs)

    def clear_filter(self):
        self.filter_entry.delete(0, tk.END)
        self.search_entry.delete(0, tk.END)
        self.update_treeview()

    def update_treeview(self, requirements=None):
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            if requirements is None:
                requirements = self.requirements

            for req in requirements:
                parent_id = req.parent.req_id if req.parent else ""
                self.tree.insert("", "end", values=(req.req_id, parent_id, req.content, req.status))

    def get_indication_display(self, req):
        if req.parent:
            return req.parent.req_id
        else:
            return "Parent"

    def update_parent_combobox(self):
        parent_ids = [req.req_id for req in self.requirements]
        self.parent_combobox['values'] = parent_ids

    def clear_entries(self):
        self.req_id_entry.delete(0, tk.END)
        self.indication_var.set("")
        self.content_entry.delete(0, tk.END)
        self.parent_var.set("")
        self.status_var.set("")

    def on_tree_double_click(self, event):
        item = self.tree.selection()[0]
        values = self.tree.item(item, "values")
        
        self.clear_entries()
        
        self.req_id_entry.insert(0, values[0])
        self.indication_var.set("Parent" if values[1] == "Master" else "Child")
        self.content_entry.insert(0, values[2])
        self.parent_var.set(values[3] if values[3] != "" else "")
        self.status_var.set(values[4])

    def draw_tree(self):
        if not self.requirements:
            messagebox.showinfo("Info", "No requirements to draw")
            return

        root = Node("Requirements")
        node_dict = {"Requirements": root}

        for req in self.requirements:
            parent_node = node_dict.get(req.parent.req_id if req.parent else "Requirements")
            node_label = f"{req.req_id}\nStatus: {req.status}"
            node = Node(node_label, parent=parent_node)
            node_dict[req.req_id] = node

        dot_exporter = DotExporter(root, 
                                options=["rankdir=TB", "splines=curved", "overlap=false"],
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
                f.write(f"Children: {children}\n")
                f.write(f"Status: {req.status}\n\n")

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
                    f.write(f"Children: {children}\n")
                    f.write(f"Status: {req.status}\n\n")
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
                    elif line.startswith("Status:"):
                        current_req.status = line.split(":")[1].strip()

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