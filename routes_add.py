'''
リスト関係の画面遷移
'''
from bottle import Bottle, jinja2_template as template,request, redirect
from bottle import response
import routes
from models import connection, Books
from utils.auth import Auth
import urllib.parse as urlpar
import psycopg2
import psycopg2.extras
import datetime
date1 = datetime.date.today()

#routesからappを読み込む
app  = routes.app
auth = Auth()


#DB接続情報
# DB接続情報
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'book_data'
DB_USER = 'book_user'
DB_PASS = 'kikikawaii'

def get_connection():
    '''
    DBの接続を行う
    '''
    dsn = 'host={host} port={port} dbname={dbname} user={user} password={password}'
    dsn = dsn.format(user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT, dbname=DB_NAME)
    return psycopg2.connect(dsn)

@app.route('/add', method=['GET', 'POST'])
def add():
    return template('add.html')

@app.route('/store', method=['GET', 'POST'])
def store():
    name = request.forms.decode().get('name')
    volume  = request.forms.decode().get('volume')
    author   = request.forms.decode().get('author')
    publisher = request.forms.decode().get('publisher')
    memo = request.forms.decode().get('memo')

    #sqlを記入する
    sql = """insert into books \
    (name, volume, author, publisher, memo, create_date, del) \
    values \
    (%(name)s, %(volume)s, %(author)s, %(publisher)s, %(memo)s, %(date1)s,false);"""
    #入力する値の辞書を設定する
    val = {'name':name, 'volume':volume,\
        'author':author, 'publisher':publisher,\
        'memo':memo ,'date1':date1 }
    with get_connection() as con:#DBの接続を取得
        with con.cursor() as cur:#カーソルを取得
            cur.execute(sql, val)
        con.commit()
    redirect('/list')

@app.route('/modi', method=['GET', 'POST'])
def modi():
    # リスト画面を表示する
    # DBから書籍リストの取得

    #認証確認
    auth.check_login()

    bookList = connection.query(Books.name,
                             Books.volume, Books.author,
                             Books.publisher, Books.memo,
                             Books.id_)\
            .filter(Books.delFlg == False).all()
    return template('modify.html', bookList=bookList)