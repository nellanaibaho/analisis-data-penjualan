import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Memuat Data
sales_data = pd.read_csv('sales_data.csv')
customer_reference = pd.read_csv('customer_reference.csv')

# Tampilkan 5 baris pertama dari masing-masing dataset
print("Data Penjualan:")
print(sales_data.head())

print("\nData Referensi Pelanggan:")
print(customer_reference.head())

# Tampilkan informasi mengenai dataset penjualan dan referensi pelanggan
print("\nInformasi Data Penjualan:")
print(sales_data.info())

print("\nInformasi Data Referensi Pelanggan:")
print(customer_reference.info())
# 2. Mengidentifikasi Kode Pelanggan yang Salah
invalid_customers = ~sales_data['CustomerID'].isin(customer_reference['CustomerID'])
invalid_sales = sales_data[invalid_customers]
print("\nTransaksi dengan Kode Pelanggan yang Salah:")
print(invalid_sales)
# 3. Membersihkan Data Penjualan
sales_data['CustomerValid'] = sales_data['CustomerID'].isin(customer_reference['CustomerID'])
sales_data.loc[~sales_data['CustomerValid'], 'CustomerID'] = np.nan
print("\nData Penjualan Setelah Pembersihan:")
print(sales_data)

# 4. Transformasi Data
sales_data['Total Sales'] = sales_data['Quantity'] * sales_data['Price']
sales_data['Date'] = pd.to_datetime(sales_data['Date'])
sales_data['Order Month'] = sales_data['Date'].dt.to_period('M')
# 5. Visualisasi Data
# Histogram dari 'Total Sales'
plt.figure(figsize=(10, 6))
plt.hist(sales_data['Total Sales'], bins=20, color='skyblue', edgecolor='black')
plt.title('Distribusi Total Penjualan')
plt.xlabel('Total Penjualan')
plt.ylabel('Frekuensi')
plt.grid(True)
plt.show()
# Grafik batang dari 'Region'
plt.figure(figsize=(10, 6))
sales_data['Region'].value_counts().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Distribusi Penjualan per Region')
plt.xlabel('Region')
plt.ylabel('Jumlah Penjualan')
plt.grid(True)
plt.show()
# Grafik batang dari penjualan per produk
plt.figure(figsize=(10, 6))
sales_data.groupby('Product')['Total Sales'].sum().plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Total Penjualan per Produk')
plt.xlabel('Produk')
plt.ylabel('Total Penjualan')
plt.grid(True)
plt.show()

# Menambah Kolom "customervalid"
sales_data['CustomerValid'] = sales_data['CustomerID'].isin(customer_reference['CustomerID'])
# 4. Menganalisis Dampak Kode Pelanggan yang Salah
invalid_sales_total = invalid_sales['Quantity'] * invalid_sales['Price']
print("\nTotal Penjualan yang Terkait dengan Kode Pelanggan yang Salah:", invalid_sales_total.sum())
# Grafik batang jumlah transaksi dan total penjualan untuk kode pelanggan yang valid dan tidak valid
valid_invalid_counts = sales_data['CustomerValid'].value_counts()
valid_invalid_sales = sales_data.groupby('CustomerValid')['Total Sales'].sum()

plt.figure(figsize=(12, 6))
# Jumlah transaksi
plt.subplot(1, 2, 1)
valid_invalid_counts.plot(kind='bar', color=['green', 'red'])
plt.title('Jumlah Transaksi: Valid vs Tidak Valid')
plt.xlabel('Validitas Pelanggan')
plt.ylabel('Jumlah Transaksi')
# Total penjualan
plt.subplot(1, 2, 2)
valid_invalid_sales.plot(kind='bar', color=['green', 'red'])
plt.title('Total Penjualan: Valid vs Tidak Valid')
plt.xlabel('Validitas Pelanggan')
plt.ylabel('Total Penjualan')

plt.tight_layout()
plt.show()

# 5. Pelaporan Temuan
temuan = {
    "Jumlah Transaksi dengan Kode Pelanggan Salah": len(invalid_sales),
    "Total Penjualan Terkait dengan Kode Pelanggan Salah": invalid_sales_total.sum(),
    "Rekomendasi": "Periksa dan koreksi kode pelanggan dalam transaksi yang tidak valid."
}

print("\nLaporan Temuan:")
for k, v in temuan.items():
    print(f"{k}: {v}")



