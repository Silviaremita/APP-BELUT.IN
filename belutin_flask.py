from flask import Flask, render_template_string, request, redirect, url_for, session, flash
import random
import smtplib, ssl
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = "belutin_secret_key"  # penting untuk session

# Template HTML langsung di dalam kode (biar 1 file aja)
login_page = """
<!DOCTYPE html>
<html>
<head>
    <title>BELUT.IN - Login</title>
    <style>
        body {
            font-family: Arial;
            background-color: #f0fff0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .box {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 320px;
            text-align: center;
        }
        h1 { color: green; }
        input {
            width: 90%;
            padding: 10px;
            margin: 8px 0;
            border: 1px solid #ccc;
            border-radius: 8px;
        }
        button {
            background: green;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
        }
        .msg { color: red; font-size: 14px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🐍 BELUT.IN</h1>
        <p>Sistem Informasi Akuntansi Budidaya Belut</p>
        {% if not session.get('otp_sent') %}
            <form method="POST" action="/send_otp">
                <input type="email" name="email" placeholder="Masukkan Email" required><br>
                <button type="submit">Kirim OTP</button>
            </form>
        {% else %}
            <form method="POST" action="/verify_otp">
                <input type="text" name="otp" placeholder="Masukkan OTP" required><br>
                <button type="submit">Verifikasi OTP</button>
            </form>
            <p><a href="/">Kirim ulang OTP</a></p>
        {% endif %}
        {% if message %}
            <p class="msg">{{ message }}</p>
        {% endif %}
    </div>
</body>
</html>
"""

dashboard_page = """
<!DOCTYPE html>
<html>
<head>
    <title>BELUT.IN - Dashboard</title>
    <style>
        body {
            font-family: Arial;
            background-color: #f9fff9;
            text-align: center;
            padding-top: 100px;
        }
        h1 { color: green; }
        button {
            background: darkgreen;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 8px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Halo, {{ email }} 👋</h1>
    <p>Selamat datang di Dashboard BELUT.IN!</p>
    <form method="POST" action="/logout">
        <button type="submit">Logout</button>
    </form>
</body>
</html>
"""

# ------------------------
# Fungsi kirim OTP via Email (simulasi)
# ------------------------
def send_otp_email(email):
    otp = random.randint(100000, 999999)
    session["otp"] = str(otp)
    session["email"] = email
    session["otp_sent"] = True
    print(f"[SIMULASI] OTP untuk {email}: {otp}")  # tampil di console aja
    # kalau mau beneran kirim email, nanti bisa tambahkan smtplib di sini
    return otp

# ------------------------
# Routing
# ------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template_string(login_page, message=None)

@app.route("/send_otp", methods=["POST"])
def send_otp():
    email = request.form["email"]
    otp = send_otp_email(email)
    return render_template_string(login_page, message=f"OTP telah dikirim ke {email} (cek console).")

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    otp_input = request.form["otp"]
    if otp_input == session.get("otp"):
        session["logged_in"] = True
        return redirect(url_for("dashboard"))
    else:
        return render_template_string(login_page, message="OTP salah, coba lagi.")

@app.route("/dashboard", methods=["GET"])
def dashboard():
    if not session.get("logged_in"):
        return redirect(url_for("home"))
    return render_template_string(dashboard_page, email=session["email"])

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("home"))

# ------------------------
# Jalankan aplikasi
# ------------------------
if __name__ == "__main__":
    app.run(debug=True)
