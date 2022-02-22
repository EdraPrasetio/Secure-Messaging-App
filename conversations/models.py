from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Conversation(models.Model):
	from_account = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
	to_account = models.ForeignKey(User, related_name='+', on_delete=models.CASCADE)
	text = models.TextField(max_length=512)
	created_at = models.DateTimeField(auto_now_add=True)