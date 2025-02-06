import streamlit as st
import pandas as pd
import datetime
import os

# Fungsi untuk menyimpan dan membaca data pekerjaan
def load_data():
    if os.path.exists('work_tracking.csv'):
        df = pd.read_csv('work_tracking.csv')
        
        # Mengkonversi kolom tanggal menjadi tipe datetime, dengan penanganan error
        df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')  # Menggunakan 'coerce' untuk menangani nilai yang salah
        df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')  # Sama untuk End Date
    else:
        # Jika file CSV tidak ada, buat DataFrame kosong dengan kolom yang sesuai
        df = pd.DataFrame(columns=['Task', 'Start Date', 'End Date', 'Duration (Days)', 'Status'])
    return df

def save_data(df):
    # Pastikan file disimpan di direktori yang benar
    df.to_csv('work_tracking.csv', index=False)
    
# Judul Aplikasi
st.title("Aplikasi Tracking Pekerjaan")

# Menampilkan data pekerjaan dengan menggunakan `use_container_width`
st.header("Daftar Pekerjaan")
df = load_data()

# Menampilkan DataFrame dengan opsi responsif
st.dataframe(df, use_container_width=True)

# Formulir untuk menambahkan pekerjaan baru
st.header("Tambah Pekerjaan Baru")
task = st.text_input("Nama Pekerjaan")

# Menggunakan date_input dengan tanggal default sebagai tanggal saat ini
start_date = st.date_input("Tanggal Mulai", min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2025, 12, 31), key="start_date")

# Setelah start_date dipilih, tampilkan end_date dengan rentang yang sesuai
end_date = st.date_input("Tanggal Selesai", min_value=start_date, max_value=datetime.date(2025, 12, 31))
