from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Store 5-letter words
class Word(models.Model):
    word = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return self.word

# Each play session (user + chosen word)
class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    attempts_used = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    won = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.word.word} - {self.date}"

# Each individual guess attempt
class Guess(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='guesses')
    guess_word = models.CharField(max_length=5)
    attempt_number = models.IntegerField()
    result = models.CharField(max_length=100)  # stores "green,grey,orange,..." etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.game} - {self.guess_word} ({self.attempt_number})"
