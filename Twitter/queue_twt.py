import pika
from rauth import OAuth1Service
from requests_oauthlib import OAuth1Session

host_server = 'localhost'

connection = pika.BlockingConnection(pika.ConnectionParameters(host=host_server))
channel = connection.channel()

channel.queue_declare(queue='twt')

def callback(ch, method, properties, body):
	channel1 = connection.channel()
	channel1.queue_declare(queue='to_server', durable=True)
	message = body.decode('utf-8')
	l = message.split('ÿ', 2)
	print("Received msg splitted ",l)

	flag = 'ÿ'
	msg = l[0]
	if (l[1] == 'upload_post'):
	
		# msg_id ÿ 'upload_post' ÿ access_token ÿ access_tok_secret ÿ text ÿ photo (binary)
		f = 0
		consumer_key = 'VyP9pdp6VC1M0qkfS4m14oxqM'
		consumer_secret = 'udtYapVuIU3vFalBjRmHWIVPPE6yA9BK4Zwzj6XB1kRcg8ekQq'
		l = message.split('ÿ', 5)
		access_token = l[2]
		access_token_secret = l[3]
		text = l[4]
		photo = l[5]
		print(text)
		flag_photo = false
		
		oauth = OAuth1Session(consumer_key, client_secret = consumer_secret,resource_owner_key = access_token,resource_owner_secret = access_token_secret)
		if len(photo) > 0:
			media_info = oauth.post('https://upload.twitter.com/1.1/media/upload.json', media=photo, json=None)
			if (!('200' in str(media_info))):
				# messaggio d'errore non hai caricato un ciufulo
			flag_photo = true
			pass
		print('AAAAAAAAAAAAAAAAAAAAAAAA')
		
		if (flag_photo):
			media_id = media_info['media_id']
			params = {'status': 'testo','media_id'= 'media_id'}
			params['media_id'] = media_id
		else:
			params = {'status': 'testo'}
		
		params['status']=text
		r = oauth.post('https://api.twitter.com/1.1/statuses/update.json', data = params,json=None)
		risposta = 1
		if ('200' in str(r)):
			risposta = 0
	
		if not risposta:
			stringa_invio =msg+flag+'twtÿupload_postÿ'+str(risposta)
			channel1.basic_publish(exchange='',routing_key = 'to_server',body=stringa_invio)
		else: 
			stringa_invio =msg+flag+'twtÿupload_postÿ'+'exception_occurred'
			channel1.basic_publish(exchange='',routing_key = 'to_server',body=stringa_invio)
	else:
		#send error message to server 'comand not verified'
	

channel.basic_consume(callback,
                      queue='twt',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
