from flask import Flask, request, render_template, session
from instagram.client import InstagramAPI
from instagram import client, subscriptions
from app import app

app.secret_key = '\xc7\x8ds|\xfe\x0f\x91\x1d\x83\t\xe7$\xd2\x1e\x91\xf0\xc4c e\x17j\xe3\x8f'

@app.route('/')
@app.route('/index.html')
def index():
    code = request.args.get('code')
    client_id = '6b64bcfaa3be4735acc0a509e2bd130d'
    client_secret = 'f37f135de06942edb1d7931e7cf410f3'
    redirect_uri = 'http://127.0.0.1:5000/'
    unauthenticated_api = client.InstagramAPI(client_id=client_id,
                                              client_secret=client_secret,
                                              redirect_uri=redirect_uri)
    user = {'nickname':'pal'}
    if not code:
        return render_template('index.html', user=user)
    if not 'user' in session.keys():
        try:
            access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
            session['token'] = access_token
            session['user'] = user_info

        except Exception as e:
            return render_template('index.html', user=user)

    api = client.InstagramAPI(access_token=session['token'], client_secret=client_secret)

    user = session['user']
    userID = user['id']

    recent_media, next_ = api.user_recent_media(user_id=userID, count=20)

    recent_media.sort(key=lambda x: x.like_count, reverse=True)

    return render_template('index.html',
                               title='Home',
                               user=session['user'],
                               media=recent_media)