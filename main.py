import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  
    database="kasir"
)
cursor = conn.cursor()

# Fungsi Barang

def tambah_barang():
    nama = entry_nama.get()
    harga = entry_harga.get()
    if nama and harga:
        cursor.execute("INSERT INTO barang (nama_barang, harga) VALUES (%s, %s)", (nama, harga))
        conn.commit()
        messagebox.showinfo("Sukses", "Barang ditambahkan.")
        entry_nama.delete(0, END)
        entry_harga.delete(0, END)
        lihat_barang()
    else:
        messagebox.showwarning("Peringatan", "Nama dan harga tidak boleh kosong.")

def lihat_barang():
    listbox_barang.delete(0, END)
    cursor.execute("SELECT * FROM barang")
    for row in cursor.fetchall():
        listbox_barang.insert(END, f"ID: {row[0]}, Nama: {row[1]}, Harga: {row[2]}")

# Fungsi Gudang dan Stok

def tambah_gudang():
    lokasi = entry_lokasi.get()
    if lokasi:
        cursor.execute("INSERT INTO gudang (lokasi) VALUES (%s)", (lokasi,))
        conn.commit()
        messagebox.showinfo("Sukses", "Gudang ditambahkan.")
        entry_lokasi.delete(0, END)
    else:
        messagebox.showwarning("Peringatan", "Lokasi tidak boleh kosong.")

def tambah_stok():
    try:
        id_barang = int(entry_stok_id_barang.get())
        id_gudang = int(entry_stok_id_gudang.get())
        jumlah = int(entry_stok_jumlah.get())
        cursor.execute("INSERT INTO stok (id_barang, id_gudang, jumlah) VALUES (%s, %s, %s) "
                       "ON DUPLICATE KEY UPDATE jumlah = jumlah + %s", (id_barang, id_gudang, jumlah, jumlah))
        conn.commit()
        messagebox.showinfo("Sukses", "Stok ditambahkan.")
    except ValueError:
        messagebox.showwarning("Peringatan", "Semua input stok harus berupa angka.")

# Fungsi Transaksi

def tambah_transaksi():
    try:
        id_barang = int(entry_id_barang.get())
        jumlah = int(entry_jumlah.get())
        cursor.execute("SELECT harga FROM barang WHERE id_barang = %s", (id_barang,))
        result = cursor.fetchone()
        if result:
            harga = result[0]
            subtotal = harga * jumlah
            cursor.execute("INSERT INTO transaksi () VALUES ()")
            id_transaksi = cursor.lastrowid
            cursor.execute("INSERT INTO detail_transaksi (id_transaksi, id_barang, jumlah, subtotal) VALUES (%s, %s, %s, %s)",
                           (id_transaksi, id_barang, jumlah, subtotal))
            conn.commit()
            messagebox.showinfo("Sukses", f"Transaksi ditambahkan. Total: Rp{subtotal:.2f}")
            entry_id_barang.delete(0, END)
            entry_jumlah.delete(0, END)
        else:
            messagebox.showerror("Error", "Barang tidak ditemukan.")
    except ValueError:
        messagebox.showwarning("Peringatan", "ID Barang dan Jumlah harus berupa angka.")

# Fungsi Laporan

def lihat_laporan():
    tree_laporan.delete(*tree_laporan.get_children())
    cursor.execute("SELECT t.id_transaksi, t.tanggal, b.nama_barang, d.jumlah, d.subtotal FROM transaksi t "
                   "JOIN detail_transaksi d ON t.id_transaksi = d.id_transaksi "
                   "JOIN barang b ON d.id_barang = b.id_barang")
    for row in cursor.fetchall():
        tree_laporan.insert('', END, values=row)

# GUI
root = Tk()
root.title("Aplikasi Kasir")
root.geometry("800x700")

# Frame Barang
Label(root, text="Data Barang", font=('Arial', 12, 'bold')).pack(pady=5)
frame_input = Frame(root)
frame_input.pack()
Label(frame_input, text="Nama Barang:").grid(row=0, column=0)
entry_nama = Entry(frame_input)
entry_nama.grid(row=0, column=1)
Label(frame_input, text="Harga:").grid(row=1, column=0)
entry_harga = Entry(frame_input)
entry_harga.grid(row=1, column=1)
Button(frame_input, text="Tambah Barang", command=tambah_barang).grid(row=2, column=0, columnspan=2, pady=5)
listbox_barang = Listbox(root, width=80)
listbox_barang.pack(pady=5)
lihat_barang()

# Frame Gudang
Label(root, text="Manajemen Gudang & Stok", font=('Arial', 12, 'bold')).pack(pady=5)
frame_gudang = Frame(root)
frame_gudang.pack()
Label(frame_gudang, text="Lokasi Gudang:").grid(row=0, column=0)
entry_lokasi = Entry(frame_gudang)
entry_lokasi.grid(row=0, column=1)
Button(frame_gudang, text="Tambah Gudang", command=tambah_gudang).grid(row=0, column=2, padx=5)
Label(frame_gudang, text="ID Barang:").grid(row=1, column=0)
entry_stok_id_barang = Entry(frame_gudang)
entry_stok_id_barang.grid(row=1, column=1)
Label(frame_gudang, text="ID Gudang:").grid(row=2, column=0)
entry_stok_id_gudang = Entry(frame_gudang)
entry_stok_id_gudang.grid(row=2, column=1)
Label(frame_gudang, text="Jumlah:").grid(row=3, column=0)
entry_stok_jumlah = Entry(frame_gudang)
entry_stok_jumlah.grid(row=3, column=1)
Button(frame_gudang, text="Tambah Stok", command=tambah_stok).grid(row=4, column=0, columnspan=2, pady=5)

# Frame Transaksi
Label(root, text="Transaksi Penjualan", font=('Arial', 12, 'bold')).pack(pady=5)
frame_transaksi = Frame(root)
frame_transaksi.pack()
Label(frame_transaksi, text="ID Barang:").grid(row=0, column=0)
entry_id_barang = Entry(frame_transaksi)
entry_id_barang.grid(row=0, column=1)
Label(frame_transaksi, text="Jumlah:").grid(row=1, column=0)
entry_jumlah = Entry(frame_transaksi)
entry_jumlah.grid(row=1, column=1)
Button(frame_transaksi, text="Tambah Transaksi", command=tambah_transaksi).grid(row=2, column=0, columnspan=2, pady=5)

# Frame Laporan
Label(root, text="Laporan Penjualan", font=('Arial', 12, 'bold')).pack(pady=5)
tree_laporan = ttk.Treeview(root, columns=("ID Transaksi", "Tanggal", "Barang", "Jumlah", "Subtotal"), show='headings')
for col in tree_laporan["columns"]:
    tree_laporan.heading(col, text=col)
    tree_laporan.column(col, width=150)
tree_laporan.pack(pady=5)
Button(root, text="Tampilkan Laporan", command=lihat_laporan).pack(pady=5)

root.mainloop()
