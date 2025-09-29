from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')
    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name

class MovieRequest(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_requested = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.id) + ' - ' + self.name + ' by ' + self.user.username

class Petition(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    movie_title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.movie_title} by {self.created_by.username}"

    def yes_votes_count(self):
        return self.petitionvote_set.filter(vote=True).count()

    def no_votes_count(self):
        return self.petitionvote_set.filter(vote=False).count()

    def user_has_voted(self, user):
        return self.petitionvote_set.filter(user=user).exists()

    def get_user_vote(self, user):
        try:
            return self.petitionvote_set.get(user=user)
        except PetitionVote.DoesNotExist:
            return None

class PetitionVote(models.Model):
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vote = models.BooleanField()
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('petition', 'user')

    def __str__(self):
        vote_text = "Yes" if self.vote else "No"
        return f"{self.user.username} voted {vote_text} on {self.petition.movie_title}"