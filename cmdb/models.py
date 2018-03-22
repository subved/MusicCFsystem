from django.db import models

# Create your models here.

class song_sim_matrix(models.Model):
    song1 = models.CharField(max_length=32,null = True)
    song2 = models.CharField(max_length=32,null = True)
    song3 = models.CharField(max_length=32,null = True)
    song4 = models.CharField(max_length=32,null = True)
    song5 = models.CharField(max_length=32,null = True)
    song6 = models.CharField(max_length=32,null = True)
    song7 = models.CharField(max_length=32,null = True)
    song8 = models.CharField(max_length=32,null = True)
    song9 = models.CharField(max_length=32,null = True)
    song10 = models.CharField(max_length=32,null = True)