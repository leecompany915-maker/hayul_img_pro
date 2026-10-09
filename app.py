import sqlite3
from flask import Flask,redirect,render_template,url_for,request,flash,session,send_file
import PIL			
from PIL import Image
import io	

conn = sqlite3.connect("hayul.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    mime_type TEXT,
    data BLOB
)
""")
app = Flask(__name__)
@app.route("/")
def index():
     return render_template("index.html")
@app.route("/view")
def view_image():
     return render_template("view.html")
# @app.route("/download")
# def download_file():
#     # 파일이 저장된 디렉토리 경로 지정
# #     directory = './files'
# #     file_path = os.path.join(directory, filename
#     try:
#         conn = sqlite3.connect("images.db")
#         cur = conn.cursor()

#         cur.execute("SELECT data FROM images WHERE id = ?", (1,))
#         row = cur.fetchone()
#         conn.close()
#      #    row="PNG_transparency_demonstration_1.png"
#         print(row)
#         data_io = io.BytesIO(row[0])
#         image=Image.open(data_io)
#         image.save("output_image.png")
#         return send_file("output_image.png", as_attachment=True)
#     except Exception as e:
#         return str("fuck")

if __name__ == "__main__":
     app.run(host="0.0.0.0",debug=True)