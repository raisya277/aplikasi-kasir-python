import mysql.connector
from tkinter import *
from tkinter import messagebox

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",  # Ganti dengan password MySQL kamu
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

# GUI
root = Tk()
root.title("Aplikasi Kasir")
root.geometry("600x500")

frame_input = Frame(root)
frame_input.pack(pady=10)

Label(frame_input, text="Nama Barang:").grid(row=0, column=0, sticky=W)
entry_nama = Entry(frame_input)
entry_nama.grid(row=0, column=1)

Label(frame_input, text="Harga:").grid(row=1, column=0, sticky=W)
entry_harga = Entry(frame_input)
entry_harga.grid(row=1, column=1)

btn_tambah = Button(frame_input, text="Tambah Barang", command=tambah_barang)
btn_tambah.grid(row=2, column=0, columnspan=2, pady=10)

frame_list = Frame(root)
frame_list.pack(pady=10)

listbox_barang = Listbox(frame_list, width=70)
listbox_barang.pack()

Label(root, text="Transaksi Penjualan", font=('Arial', 12, 'bold')).pack(pady=10)

frame_transaksi = Frame(root)
frame_transaksi.pack()

Label(frame_transaksi, text="ID Barang:").grid(row=0, column=0)
entry_id_barang = Entry(frame_transaksi)
entry_id_barang.grid(row=0, column=1)

Label(frame_transaksi, text="Jumlah:").grid(row=1, column=0)
entry_jumlah = Entry(frame_transaksi)
entry_jumlah.grid(row=1, column=1)

btn_transaksi = Button(frame_transaksi, text="Tambah Transaksi", command=tambah_transaksi)
btn_transaksi.grid(row=2, column=0, columnspan=2, pady=10)

lihat_barang()

root.mainloop()

