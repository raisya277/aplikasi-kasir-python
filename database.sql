CREATE DATABASE IF NOT EXISTS kasir;
USE kasir;

CREATE TABLE barang (
    id_barang INT AUTO_INCREMENT PRIMARY KEY,
    nama_barang VARCHAR(100) NOT NULL,
    harga DECIMAL(12,2) NOT NULL
);

CREATE TABLE gudang (
    id_gudang INT AUTO_INCREMENT PRIMARY KEY,
    lokasi VARCHAR(100) NOT NULL
);

CREATE TABLE stok (
    id_stok INT AUTO_INCREMENT PRIMARY KEY,
    id_barang INT NOT NULL,
    id_gudang INT NOT NULL,
    jumlah INT NOT NULL DEFAULT 0,
    UNIQUE KEY unique_stok (id_barang, id_gudang),
    FOREIGN KEY (id_barang) REFERENCES barang(id_barang),
    FOREIGN KEY (id_gudang) REFERENCES gudang(id_gudang)
);

CREATE TABLE transaksi (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    tanggal TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE detail_transaksi (
    id_detail INT AUTO_INCREMENT PRIMARY KEY,
    id_transaksi INT NOT NULL,
    id_barang INT NOT NULL,
    jumlah INT NOT NULL,
    subtotal DECIMAL(12,2) NOT NULL,
    FOREIGN KEY (id_transaksi) REFERENCES transaksi(id_transaksi),
    FOREIGN KEY (id_barang) REFERENCES barang(id_barang)
);
