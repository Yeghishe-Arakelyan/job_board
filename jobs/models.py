from django.db import models
from accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.urls import reverse
from django.template.defaultfilters import slugify



class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jobs:job_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

class Job(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='jobs',default='job.jpeg')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,null=True, related_name='category')
    company = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    contact_email = models.EmailField()
    contact_phone = PhoneNumberField()
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_by')
    date_created = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    class Meta:
        ordering = ('-date_created',)

    def __str__(self):
        return self.slug
        
    def get_absolute_url(self):
        return reverse('jobs:job_detail', kwargs={'slug':self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)