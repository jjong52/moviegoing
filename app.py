from flask import Flask, render_template, request, jsonify
import random
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://sparta:test@cluster0.32ylit8.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

import requests
from bs4 import BeautifulSoup

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/movie", methods=["POST"])
def movie_post():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    star_receive = request.form['star_give']

    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive,headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    ogtitle = soup.select_one('meta[property="og:title"]')['content']
    ogimage = soup.select_one('meta[property="og:image"]')['content']
    ogdesc = soup.select_one('meta[property="og:description"]')['content']

    # 사용자가 입력한 url에서 movie_id 뽑기
    movieid = int(url_receive[-5:])

    print(movieid)
    
    doc = { 
        'title':ogtitle,
        'desc':ogdesc,
        'image':ogimage, 
        'comment':comment_receive,
        'star':star_receive,
        'id':movieid
    }
    db.movies.insert_one(doc)

    return jsonify({'msg':'저장완료!'})

@app.route("/movie", methods=["GET"])
def movie_get(): 
    all_movies = list(db.movies.find({},{'_id':False}))
    return jsonify({'result':all_movies})



#글쓰기 페이지
@app.route('/create/')
def create():
    return '글쓰기 페이지'


#상세 페이지
@app.route('/read/<id>/')
def read(id):
    return 'Read '+id

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)



