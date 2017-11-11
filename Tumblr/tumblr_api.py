from rauth import OAuth1Service
import webbrowser
import json


 
try:
    read_input = raw_input
except NameError:
    read_input = input
 
with open('./tumblr_info.json' , 'r') as json_data_file:
    app_info = json.load(json_data_file)
 
tumblr = OAuth1Service(name='tumblr',
                       consumer_key = app_info['tumblr']['consumer_key'],
                       consumer_secret= app_info['tumblr']['consumer_secret'],
                       request_token_url='https://www.tumblr.com/oauth/request_token',
                       access_token_url='https://www.tumblr.com/oauth/access_token',
                       authorize_url='https://www.tumblr.com/oauth/authorize')
 

request_token, request_token_secret = tumblr.get_request_token(method='POST')

authorize_url = tumblr.get_authorize_url(request_token)

print('Visit this URL in your browser: ' + authorize_url)
webbrowser.open(authorize_url)

s = read_input('Enter the url u were redirect here: ')
s = s.split('&oauth_verifier=')
code = s[1]

session = tumblr.get_auth_session(request_token,request_token_secret,method='POST',data={'oauth_verifier': code})

#print(session.consumer_key)
#print(session.consumer_secret)
#print(session.access_token)
#print(session.access_token_secret)
#print(session.signature)

#exit(0)
r = session.get('http://api.tumblr.com/v2/user/info').json()
name = r['response']['user']['name']
stringa = 'http://api.tumblr.com/v2/blog/'+name+'/post'

params = {'title': 'title','body':'text'}

while(True):
	titolo = read_input("Inserisci il titolo del post che vuoi creare(Ctrl+c per terminare):\n")
	corpo = read_input("Inserisci il corpo del post che vuoi creare(Ctrl+c per terminare):\n")
	params['title']=str(titolo)
	params['body'] = str(corpo)
	r = session.post(stringa, data = params,json=None).json()
	print(r)