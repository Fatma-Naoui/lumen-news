from django.db import models
from django.contrib.postgres.fields import ArrayField
from pgvector.django import VectorField  # new


class Article(models.Model):
    """
    Model to store scraped news articles.
    """
    title = models.CharField(max_length=1024)
    text = models.TextField(blank=True)
    url = models.URLField(max_length=1000,unique=True, blank=False)
  # URL is now unique to prevent duplicates
    source = models.CharField(max_length=256, blank=True)
    summary = models.TextField(blank=True, null=True)

    category = models.CharField(max_length=256, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    # Optional: BERT embedding stored as array of floats
    embedding = VectorField(dimensions=384, null=True, blank=True)
    # Status for processing pipeline
    status = models.CharField(max_length=32, default="pending")

    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title[:50]} ({self.source})"
