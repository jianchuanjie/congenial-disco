## generate wordcloud by python


## back
back is the backend for the APIs with [Flask](http://flask.pocoo.org)

---

## 部署

* 首先用python的virtualenv创建一个新的虚拟环境, 并激活

    `virtualenv -p python3 py3`
    `source py3/bin/activate`

* 再根据requirements.txt装上需要的第三方包
    `pip install -r requirements.txt`

* 创建文件夹 instance, 再在文件夹下创建 config.py文件
    ```python
    import os

    DEBUG = False
    SECRET_KEY = b'you_secret_key'
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = 'database:///DATABASE_URI'

    UPLOADED_PHOTOS_DEST = os.path.join(os.getcwd(), 'pic')
    UPLOADED_DOCS_DEST = os.path.join(os.getcwd(), 'doc')
    ```

* 第一次运行时先创建数据库
    `python create_db.py`

* 测试环境启动:
    `python manage.py runserver`

    生产环境启动:
    `nohup gunicorn -w 3 manage:app -b 127.0.0.1:5001  >> wc.out 2>&1 &`

