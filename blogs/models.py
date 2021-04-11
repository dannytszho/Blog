from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class BlogPost(models.Model):
	"""A blogpost the user is writing about."""
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
	public = models.BooleanField(default=False)

	def __str__(self):
		"""Return a string represtation of the model."""
		return self.text

class Entry(models.Model):
	"""Something specific about a blogpost."""
	blogpost = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
	text = models.TextField()
	date_added = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name_plural = 'Entries'

	def __str__(self):
		"""Return a string representation of the model."""
		if len(self.text) > 50:
			return f"{self.text[:50]}..."
		else:
			return self.text