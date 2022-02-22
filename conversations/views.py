import re

from Crypto.Cipher import AES
import base64

from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist, BadRequest
from django.http import HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q

from conversations.models import Conversation

alphanumeric = re.compile(r'^\w+$')

# Create your views here.
@login_required
def index(request):

	all_users = User.objects.distinct().order_by('username')
	return render(request, 'conversations/index.html', {
			'user_list': all_users
		}
	)

@login_required
def conversation(request):
	to_username = request.GET.get("to_username")

	# Precondition: the correspondant's username is a valid username format.
	if not alphanumeric.match(to_username):
		raise BadRequest("Not a valid username.")

	# Precondition: the user exists.
	if to_username and not User.objects.filter(username=to_username).exists():
		raise ObjectDoesNotExist("User not found.")

	to_user_pk = User.objects.get(username=to_username).pk

	message_query = Conversation.objects.filter(
		((Q(from_account=request.user.pk) & Q(to_account=to_user_pk)) |
		(Q(from_account=to_user_pk) & Q(to_account=request.user.pk)))
	).distinct().order_by('created_at')

	messages = []
	for msg in list(message_query):
		
		# Decryption
		message = base64.b64decode(msg.text)
		decryption_suite = AES.new('This is a key123'.encode("utf8"), AES.MODE_CFB, 'This is an IV456'.encode("utf8"))
		plain_text = decryption_suite.decrypt(message).decode('utf-8')
		msg.text = plain_text
		messages.append(msg)

	return render(request,
		'conversations/conversation.html', {
			'from_username': request.user.username,
			'to_username': to_username,
			'message_list': messages
		}
	)

@login_required
def send_to_conversation(request):
	if request.method == 'POST':
		to_username = request.POST.get("to_username")
		
		# Precondition: the correspondant's username is a valid username format.
		if not alphanumeric.match(to_username):
			raise BadRequest("Not a valid username.")

		# Precondition: the user exists.
		if to_username and not User.objects.filter(username=to_username).exists():
			raise ObjectDoesNotExist("User not found.")

		to_user = User.objects.get(username=to_username)

		conversation = Conversation.objects.create(
			from_account=request.user,
			to_account=to_user,
			text=encrypt(request.POST.get("text")),
		)
		conversation.save()

		return redirect(f'/conversation?to_username={to_username}')
	else:
		raise HttpResponseNotAllowed("Unuspported method.")

def encrypt(msg):
	# Encryption
	encryption_suite = AES.new('This is a key123'.encode("utf8"), AES.MODE_CFB, 'This is an IV456'.encode("utf8"))
	cipher_text = (encryption_suite.encrypt(str(msg).encode("utf8")))
	
	return base64.b64encode(cipher_text).decode("utf-8")



	
	