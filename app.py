from flask import Flask, render_template
from serial import Serial
import sys, json, subprocess

# Variabel untuk proses awal masukkan nama port Arduino
status = True # buat mengakhiri proses input nama port di perulangannya
input_val = "" # ini buat ketika pengguna mau lanjut atau keluar dari program ini

# Setting port arduino
while status:

  # bagian ini buat menentukan; lanjut atau keluar dari program ini
  if input_val == 'no' or input_val == 'n':
    print("Mengakhiri sistem, Bye!")
    sys.exit()

  nama_port = input("Masukkan nama port serial Arduino: ")
  nama_port = nama_port.upper()

  try:
    arduino = Serial(port=nama_port, baudrate=57600, timeout=1)
    status = False
  except:
    print("Mohon cek kembali serial port koneksi Arduino.")

    input_val = input("Retry? Y | N: \n")
    input_val = input_val.lower()

# Akan muncul teks ini jika berhasil masukkan port serial arduino
print("Aplikasi sudah tersambung dengan alat")
print("Buka browser dan ketikkan info URL di bawah ini")

# Memulai server bekerja
app = Flask(__name__, 
          static_url_path='',
          static_folder='static/src')

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/read')
def readData():
  # Read data
  data_bytes = arduino.readline().decode("utf-8").strip().split()
  data_bytes[0] = data_bytes[0].split(':')[1]
  data_bytes[1] = data_bytes[1].split(':')[1]
  data_bytes[2] = data_bytes[2].split(':')[1]
  data_bytes[3] = data_bytes[3].split(':')[1]

  # Untuk keterangan
  if data_bytes[4] == "AMAN":
    data_bytes[4] = "Semua Aman"
  elif data_bytes[4] == "ABBB":
    data_bytes[4] = "Bocor A dan B"
  elif data_bytes[4] == "ABBC":
    data_bytes[4] = "CL A dan B Bocor"
  elif data_bytes[4] == "ABBD":
    data_bytes[4] = "A Bocor B Digunakan"
  elif data_bytes[4] == "ADBB":
    data_bytes[4] = "A Digunakan B Bocor"
  elif data_bytes[4] == "ADBD":
    data_bytes[4] = "Tabung A dan B Digunakan"
  elif data_bytes[4] == "ADGN":
    data_bytes[4] = "Tabung A Digunakan"
  elif data_bytes[4] == "BBCR":
    data_bytes[4] = "Tabung B Bocor"
  elif data_bytes[4] == "BCBC":
    data_bytes[4] = "Tabung B dan Tabung C Bocor"
  elif data_bytes[4] == "BCRA":
    data_bytes[4] = "Tabung A Bocor"
  elif data_bytes[4] == "BDGN":
    data_bytes[4] = "Tabung B Digunakan"
  elif data_bytes[4] == "CABB":
    data_bytes[4] = "CL A Digunakan B Bocor"
  elif data_bytes[4] == "CABD":
    data_bytes[4] = "CL A dan B Digunakan"
  elif data_bytes[4] == "CBAB":
    data_bytes[4] = "CL B Digunakan A Bocor"
  elif data_bytes[4] == "CBCR":
    data_bytes[4] = "Tabung C Bocor"
  elif data_bytes[4] == "CBDG":
    data_bytes[4] = "CL B Digunakan"
  elif data_bytes[4] == "CLBA":
    data_bytes[4] = "CL Bocor A"

  # Untuk keterangan switch
  if data_bytes[5] == "SA1":
    data_bytes[5] = "A on"
  else:
    data_bytes[5] = "A off"

  if data_bytes[6] == "SB1":
    data_bytes[6] = "B on"
  else:
    data_bytes[6] = "B off"

  data = {
    "status": "success",
    "data": data_bytes
  }

  # return json.dumps({"data": "test"})
  return json.dumps(data)

port = 5000
if __name__ == '__main__':
  result = subprocess.call("start firefox -private -url localhost:5000", shell=True)
  app.run(port=port)