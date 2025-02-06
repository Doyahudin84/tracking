import streamlit as st
import pandas as pd
import datetime
import os

# Fungsi untuk menyimpan dan membaca data pekerjaan
def load_data():
    if os.path.exists('work_tracking.csv'):
        df = pd.read_csv('work_tracking.csv')
        
        # Mengkonversi kolom tanggal menjadi tipe datetime, dengan penanganan error
        df['Start Date'] = pd.to_datetime(df['Start Date'], errors='coerce')
        df['End Date'] = pd.to_datetime(df['End Date'], errors='coerce')
    else:
        # Jika file CSV tidak ada, buat DataFrame kosong dengan kolom yang sesuai
        df = pd.DataFrame(columns=['Task', 'Start Date', 'End Date', 'Duration (Days)', 'Status'])
    return df

def save_data(df):
    df.to_csv('work_tracking.csv', index=False)

# Judul Aplikasi
st.title("Aplikasi Tracking Pekerjaan")

# Menampilkan data pekerjaan dengan responsif
st.header("Daftar Pekerjaan")
df = load_data()
st.dataframe(df, use_container_width=True)

# Formulir untuk menambahkan pekerjaan baru
st.header("Tambah Pekerjaan Baru")
task = st.text_input("Nama Pekerjaan")

# Menggunakan date_input dengan tanggal default sebagai tanggal saat ini
start_date = st.date_input("Tanggal Mulai", min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2025, 12, 31), key="start_date")
end_date = st.date_input("Tanggal Selesai", min_value=start_date, max_value=datetime.date(2025, 12, 31), key="end_date")

status = st.selectbox("Status Pekerjaan", ['Belum Selesai', 'Selesai'])

if st.button("Simpan Pekerjaan"):
    if task and start_date and end_date:
        duration = (end_date - start_date).days  # durasi dalam hari
        new_task = {
            'Task': task,
            'Start Date': start_date.strftime('%Y-%m-%d'),
            'End Date': end_date.strftime('%Y-%m-%d'),
            'Duration (Days)': duration,
            'Status': status
        }
        new_task_df = pd.DataFrame([new_task])
        df = pd.concat([df, new_task_df], ignore_index=True)
        save_data(df)
        st.success("Pekerjaan berhasil ditambahkan!")
    else:
        st.error("Harap isi semua kolom!")

# Fungsi untuk mengedit pekerjaan
st.header("Edit Pekerjaan")
edit_task = st.selectbox("Pilih Pekerjaan untuk Edit", df['Task'].tolist())

if edit_task:
    selected_task = df[df['Task'] == edit_task].iloc[0]
    new_status = st.selectbox("Pilih Status Baru", ['Belum Selesai', 'Selesai'], index=['Belum Selesai', 'Selesai'].index(selected_task['Status']))

    # Pastikan new_start_date dan new_end_date valid
    new_start_date = selected_task['Start Date'] if pd.notna(selected_task['Start Date']) else datetime.date.today()
    new_end_date = selected_task['End Date'] if pd.notna(selected_task['End Date']) else datetime.date.today()

    new_start_date = st.date_input("Edit Tanggal Mulai", value=new_start_date, min_value=datetime.date(2020, 1, 1), max_value=datetime.date(2025, 12, 31))
    new_end_date = st.date_input("Edit Tanggal Selesai", value=new_end_date, min_value=new_start_date, max_value=datetime.date(2025, 12, 31))

    if st.button("Update Status dan Tanggal"):
        duration = (new_end_date - new_start_date).days
        df.loc[df['Task'] == edit_task, ['Status', 'Start Date', 'End Date', 'Duration (Days)']] = [new_status, new_start_date.strftime('%Y-%m-%d'), new_end_date.strftime('%Y-%m-%d'), duration]
        save_data(df)
        st.success("Status dan Tanggal pekerjaan telah diperbarui!")

    # Menambahkan Fitur untuk menghapus pekerjaan
    if st.button("Hapus Pekerjaan"):
        df = df[df['Task'] != edit_task]  # Menghapus task yang dipilih
        save_data(df)
        st.success("Pekerjaan telah dihapus!")

# Menambahkan Fitur untuk menampilkan pekerjaan yang masih berjalan
st.header("Pekerjaan yang Belum Selesai")
unfinished_tasks = df[df['Status'] == 'Belum Selesai']
st.dataframe(unfinished_tasks, use_container_width=True)
