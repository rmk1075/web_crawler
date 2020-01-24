# main site by flask

from flask import Flask, render_template, request, url_for
from login import login_check

app = Flask(__name__, static_url_path='/static')

# '/'
# index.html
@app.route('/')
def main_get(num=None):
    return render_template('index.html', num=num)


# '/login'
# check by hisnet_id, hisnet_pwd
@app.route('/login', methods=['POST', 'GET'])
def login(num=None):
    
    if request.method == 'GET':
        ## 넘겨받은 id&pwd
        id = request.args.get('id')
        pwd = request.args.get('pwd')

        ## 넘겨받은 값을 원래 페이지로 리다이렉트
        if login_check(request.args.get('id'), request.args.get('pwd')):
            return render_template('output.html', id = id, pwd = pwd, status = 'logged in')
            # return 'success'
        else:
            return render_template('output.html', id = id, pwd = pwd, status = 'log in fail')
            # return 'fail'
        
        # return render_template('login_test.html', id=temp, pwd=temp1)
    ## else 로 하지 않은 것은 POST, GET 이외에 다른 method로 넘어왔을 때를 구분하기 위함

# '/table/'+hisnet_id # is it possible?
# prints out the information from hisnet by the table

if __name__ == '__main__':
    # threaded=True 로 넘기면 multiple plot이 가능해짐
  app.run(debug=True, threaded=True)
