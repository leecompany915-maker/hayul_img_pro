import sqlite3
from flask import Flask,redirect,render_template,url_for,request,flash,session,send_file
from io import BytesIO
from PIL import Image
import os
conn = sqlite3.connect("hayul.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS hayul (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    scr TEXT,
    data BLOB
)
""")
# 4. 변경사항 저장 (Commit)
conn.commit()
conn.close()
app = Flask(__name__)
@app.route("/")
def index():
     return render_template("index.html")
@app.route('/upload')
def upload():
     return render_template("upload.html")
@app.route('/uplo', methods=['POST'])
def view():
    if 'image' not in request.files:
        return '파일이 없습니다.'

    file = request.files['image']
    if file.filename == '':
        return '선택된 파일이 없습니다.'

    title = request.form['title']
    script = request.form['script']
    
    # 이미지를 바이너리(BLOB)로 읽기
    image_bytes = file.read()

    # 데이터베이스 연결 및 저장
    conn = sqlite3.connect("hayul.db")
    cur = conn.cursor()
    
    sql = 'INSERT INTO hayul (title, scr, data) VALUES (?, ?, ?)'
    cur.execute(sql, (title, script, image_bytes))
    conn.commit()
    
    # 방금 삽입된 데이터의 id 가져오기
    last_id = cur.lastrowid

    # 최신 데이터 또는 방금 넣은 데이터 조회
    cur.execute("SELECT data FROM hayul WHERE id = ?", (last_id,))
    row = cur.fetchone()

    fl_name = f"hayul_{last_id}"
    
    # Render 환경에서도 안전한 static 폴더 경로 설정 (상대 경로 활용)
    static_folder = os.path.join(app.root_path, 'static')
    os.makedirs(static_folder, exist_ok=True) # 폴더가 없으면 자동 생성
    
    save_path = os.path.join(static_folder, fl_name + ".png")

    if row:
        blob_data = row[0]
        try:
            # Pillow를 이용해 이미지 검증 및 저장
            image = Image.open(BytesIO(blob_data))
            with open(save_path, "wb") as output_file:
                output_file.write(blob_data)
        except Exception as e:
            print(f"이미지 처리 중 오류 발생: {e}")

    conn.close()

    return render_template('view.html', script=script, img_name=fl_name + ".png", title=title)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)