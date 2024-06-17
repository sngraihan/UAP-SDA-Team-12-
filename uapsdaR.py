#Sistem Manajemen Buku Tamu Pesta

#Dikerjakan Oleh Raihan Andi Saungnaga
import csv
from tkinter import *
from tkinter import filedialog, messagebox, ttk

class Tamu:
    def __init__(self, id, nama, waktu_kedatangan, status_undangan, kategori):
        self.id = id
        self.nama = nama
        self.waktu_kedatangan = waktu_kedatangan
        self.status_undangan = status_undangan
        self.kategori = kategori

    def __str__(self):
        return f"ID: {self.id}, Nama: {self.nama}, Waktu Kedatangan: {self.waktu_kedatangan}, Status Undangan: {self.status_undangan}, Kategori: {self.kategori}"

class SistemManajemenTamu:
    def __init__(self, root):
        self.tamu = []
        self.root = root
        self.root.title("Sistem Manajemen Tamu Pesta")
        self.root.geometry("1500x800")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=("Helvetica", 10, "bold"), padding=10, background="pink")
        style.configure("TLabel", font=("Helvetica", 12), background="#FFFDD0") 
        style.configure("Treeview.Heading", font=("Helvetica", 12, "bold"), background="pink")

        self.frame = Frame(self.root, bg="#FFFDD0") 
        self.frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        self.button_frame = Frame(self.frame, bg="#FFFDD0")  
        self.button_frame.pack(pady=10)
        self.btn_tambah = ttk.Button(self.button_frame, text="Tambah Tamu", command=self.tambah_tamu)
        self.btn_tambah.grid(row=0, column=0, padx=10)
        self.btn_perbarui = ttk.Button(self.button_frame, text="Perbarui Tamu", command=self.perbarui_tamu)
        self.btn_perbarui.grid(row=0, column=2, padx=10)
        self.btn_hapus = ttk.Button(self.button_frame, text="Hapus Tamu", command=self.hapus_tamu)
        self.btn_hapus.grid(row=0, column=3, padx=10)
        self.btn_urutkan = ttk.Button(self.button_frame, text="Urutkan Tamu", command=self.urutkan_tamu)
        self.btn_urutkan.grid(row=0, column=4, padx=10)
        self.btn_cari = ttk.Button(self.button_frame, text="Cari Tamu", command=self.cari_tamu)
        self.btn_cari.grid(row=0, column=5, padx=10)
        self.btn_impor = ttk.Button(self.button_frame, text="Impor Tamu dari CSV", command=self.impor_tamu)
        self.btn_impor.grid(row=0, column=6, padx=10)
        self.btn_ekspor = ttk.Button(self.button_frame, text="Ekspor Tamu ke CSV", command=self.ekspor_tamu)
        self.btn_ekspor.grid(row=0, column=7, padx=10)

        self.tree_frame = Frame(self.frame)
        self.tree_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)
        self.tree = ttk.Treeview(self.tree_frame, columns=("ID", "Nama", "Waktu Kedatangan", "Status Undangan", "Kategori"), show='headings', selectmode='browse')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nama", text="Nama")
        self.tree.heading("Waktu Kedatangan", text="Waktu Kedatangan")
        self.tree.heading("Status Undangan", text="Status Undangan")
        self.tree.heading("Kategori", text="Kategori")
        self.tree.column("ID", anchor=CENTER)
        self.tree.column("Nama", anchor=CENTER)
        self.tree.column("Waktu Kedatangan", anchor=CENTER)
        self.tree.column("Status Undangan", anchor=CENTER)
        self.tree.column("Kategori", anchor=CENTER)
        self.tree.pack(fill=BOTH, expand=True)
        self.tree_scroll = ttk.Scrollbar(self.tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree_scroll.pack(side=RIGHT, fill=Y)
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

#Dikerjakan Oleh Maura Hellena    
    
    def tambah_tamu(self):
        self.edit_tamu_window("Tambah Tamu", self.simpan_tamu_baru)

    def simpan_tamu_baru(self, id, nama, waktu_kedatangan, status_undangan, kategori):
        tamu = Tamu(id, nama, waktu_kedatangan, status_undangan, kategori)
        self.tamu.append(tamu)
        self.update_treeview()
        messagebox.showinfo("Sukses", "Tamu berhasil ditambahkan!")

    def lihat_tamu(self):
        self.update_treeview()

    def perbarui_tamu(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Silakan pilih tamu yang ingin diperbarui.")
            return

        item = self.tree.item(selected_item)
        tamu_data = item['values']
        self.edit_tamu_window("Perbarui Tamu", self.simpan_tamu_diperbarui, *tamu_data)

    def simpan_tamu_diperbarui(self, id, nama, waktu_kedatangan, status_undangan, kategori):
        for tamu in self.tamu:
            if tamu.id == id:
                tamu.nama = nama
                tamu.waktu_kedatangan = waktu_kedatangan
                tamu.status_undangan = status_undangan
                tamu.kategori = kategori
                self.update_treeview()
                messagebox.showinfo("Sukses", "Tamu berhasil diperbarui!")
                return

    def hapus_tamu(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Silakan pilih tamu yang ingin dihapus.")
            return

        item = self.tree.item(selected_item)
        tamu_id = item['values'][0]

        self.tamu = [tamu for tamu in self.tamu if tamu.id != tamu_id]
        self.tree.delete(selected_item)
        messagebox.showinfo("Sukses", "Tamu berhasil dihapus!")

    def urutkan_tamu(self):
        sort_window = Toplevel(self.root)
        sort_window.title("Urutkan Tamu")
        Label(sort_window, text="Urutkan berdasarkan:", font=("Helvetica", 12), background="#FFFDD0").pack(pady=10)
        criteria = StringVar()
        criteria.set("nama")
        OptionMenu(sort_window, criteria, "nama", "waktu_kedatangan", "status_undangan", "kategori").pack(pady=10)
        Button(sort_window, text="Urutkan", command=lambda: self.lakukan_pengurutan(criteria.get())).pack(pady=10)

    def lakukan_pengurutan(self, criteria):
        if criteria == "nama":
            self.tamu.sort(key=lambda tamu: tamu.nama)
        elif criteria == "waktu_kedatangan":
            self.tamu.sort(key=lambda tamu: tamu.waktu_kedatangan)
        elif criteria == "status_undangan":
            self.tamu.sort(key=lambda tamu: tamu.status_undangan)
        elif criteria == "kategori":
            self.tamu.sort(key=lambda tamu: tamu.kategori)
        else:
            messagebox.showerror("Kesalahan", "Kriteria tidak valid")
            return
        self.update_treeview()
        messagebox.showinfo("Sukses", "Tamu berhasil diurutkan!")
