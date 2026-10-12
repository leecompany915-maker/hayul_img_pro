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

    # 요청마다 DB 연결 및 종료 처리
    conn = sqlite3.connect("hayul.db")
    cur = conn.cursor()
    
    # 테이블 이름을 hayul로 일치시킴
    sql = 'INSERT INTO hayul (title, scr, data) VALUES (?, ?, ?)'
    user_data = (title, script, image_bytes)

    cur.execute(sql, user_data)
    conn.commit()
    cur.execute("SELECT data FROM hayul WHERE id = 1")
    row = cur.fetchone()

    if row:
        blob_data = row[0]

        # 3-A. Pillow(PIL)를 이용해 이미지 객체로 변환하여 확인
        image = Image.open(BytesIO(blob_data))# 이미지Viewer로 표시

        # 3-B. 혹은 새로운 이미지 파일로 다시 저장하기
        fl_name="hayul1"
        save_path = os.path.join('/home/lee/hayul/static', fl_name+".png")
        with open(save_path, "wb") as output_file:
            output_file.write(blob_data)

    conn.close()

    # 필요시 서버 폴더에 파일 저장
    # if file:
    #     file.seek(0) # 읽어들인 포인터 초기화
    #     filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    #     file.save(filepath)

    return render_template('view.html', script=script, img_name=fl_name+".png", title=title)


if __name__ == "__main__":
     app.run(host="0.0.0.0",debug=True)