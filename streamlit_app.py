import streamlit as st
import pandas as pd
import datetime

# Fungsi untuk menyimpan dan membaca data pekerjaan
def load_data():
    try:
        df = pd.read_csv('work_tracking.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Task', 'Start Date', 'End Date', 'Duration (Hours)', 'Status'])
    return df

def save_data(df):
    df.to_csv('work_tracking.csv', index=False)

# Judul Aplikasi
st.title("Aplikasi Tracking Pekerjaan")

# Menampilkan data pekerjaan
st.header("Daftar Pekerjaan")
df = load_data()
st.dataframe(df)

# Formulir untuk menambahkan pekerjaan baru
st.header("Tambah Pekerjaan Baru")
task = st.text_input("Nama Pekerjaan")
start_date = st.date_input("Tanggal Mulai", datetime.date.today())
end_date = st.date_input("Tanggal Selesai", datetime.date.today())
status = st.selectbox("Status Pekerjaan", ['Belum Selesai', 'Selesai'])

if st.button("Simpan Pekerjaan"):
    if task and start_date and start_time and end_date and end_time:
        # Menghitung durasi pekerjaan
        start_datetime = datetime.datetime.combine(start_date, start_time)
        end_datetime = datetime.datetime.combine(end_date, end_time)
        duration = (end_datetime - start_datetime).total_seconds() / 3600  # dalam jam

        # Menambahkan data pekerjaan baru
        new_task = {
            'Task': task,
            'Start Date': start_datetime.strftime('%Y-%m-%d %H:%M'),
            'End Date': end_datetime.strftime('%Y-%m-%d %H:%M'),
            'Duration (Hours)': round(duration, 2),
            'Status': status
        }

        df = df.append(new_task, ignore_index=True)
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
    if st.button("Update Status"):
        df.loc[df['Task'] == edit_task, 'Status'] = new_status
        save_data(df)
        st.success("Status pekerjaan telah diperbarui!")

# Menambahkan Fitur untuk menampilkan pekerjaan yang masih berjalan
st.header("Pekerjaan yang Belum Selesai")
unfinished_tasks = df[df['Status'] == 'Belum Selesai']
st.dataframe(unfinished_tasks)
