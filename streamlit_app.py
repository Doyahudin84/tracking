import streamlit as st
import pandas as pd
import datetime
import os

# Fungsi untuk menyimpan dan membaca data pekerjaan
def load_data():
    if os.path.exists('work_tracking.csv'):
        df = pd.read_csv('work_tracking.csv')
        # Mengkonversi kolom tanggal menjadi tipe datetime
        df['Start Date'] = pd.to_datetime(df['Start Date'])
        df['End Date'] = pd.to_datetime(df['End Date'])
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
start_date = st.date_input("Tanggal Mulai", datetime.date.today())
end_date = st.date_input("Tanggal Selesai", datetime.date.today())
status = st.selectbox("Status Pekerjaan", ['Belum Selesai', 'Selesai'])

if st.button("Simpan Pekerjaan"):
    if task and start_date and end_date:
        # Menghitung durasi pekerjaan dalam hari
        duration = (end_date - start_date).days  # durasi dalam hari

        # Menambahkan data pekerjaan baru
        new_task = {
            'Task': task,
            'Start Date': start_date.strftime('%Y-%m-%d'),
            'End Date': end_date.strftime('%Y-%m-%d'),
            'Duration (Days)': duration,
            'Status': status
        }

        new_task_df = pd.DataFrame([new_task])  # Membuat DataFrame baru untuk task
        df = pd.concat([df, new_task_df], ignore_index=True)  # Menambahkan baris baru ke DataFrame
        save_data(df)  # Menyimpan data ke CSV
        st.success("Pekerjaan berhasil ditambahkan!")
    else:
        st.error("Harap isi semua kolom!")

# Fungsi untuk mengedit pekerjaan
st.header("Edit Pekerjaan")
edit_task = st.selectbox("Pilih Pekerjaan untuk Edit", df['Task'].tolist())
if edit_task:
    selected_task = df[df['Task'] == edit_task].iloc[0]
    new_status = st.selectbox("Pilih Status Baru", ['Belum Selesai', 'Selesai'], index=['Belum Selesai', 'Selesai'].index(selected_task['Status']))
    if st.button("Update Status"):
        df.loc[df['Task'] == edit_task, 'Status'] = new_status
        save_data(df)
        st.success("Status pekerjaan telah diperbarui!")

# Menambahkan Fitur untuk menampilkan pekerjaan yang masih berjalan
st.header("Pekerjaan yang Belum Selesai")
unfinished_tasks = df[df['Status'] == 'Belum Selesai']

# Menampilkan data pekerjaan yang belum selesai dengan responsif
st.dataframe(unfinished_tasks, use_container_width=True)
