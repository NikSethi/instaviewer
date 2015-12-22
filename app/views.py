from flask import Flask, request, render_template
from instagram.client import InstagramAPI
from instagram import client, subscriptions
from app import app

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
    access_token, user_info = unauthenticated_api.exchange_code_for_access_token(code)
    if not access_token:
        return 'Could not get access token'
    api = client.InstagramAPI(access_token=access_token, client_secret=client_secret)

    print user_info
    # request.session['access_token'] = access_token
    # return render_template('index.html', title='Auth Successful', user='Auth')

    userID = user_info['id']

    recent_media, next_ = api.user_recent_media(user_id=userID, count=20)

    recent_media.sort(key=lambda x: x.like_count, reverse=True)

    return render_template('index.html',
                               title='Home',
                               user=user_info,
                               media=recent_media)