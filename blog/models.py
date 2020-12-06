from django.db import models

class BlogPost(models.Model):
    post_id = models.AutoField(primary_key=True)
    post_type = models.CharField(max_length=50, default='')
    title = models.CharField(max_length=100)
    lead_author = models.CharField(max_length=50, null=True, blank=True)
    heading_0 = models.CharField(max_length=200, default='')
    cheading_0 = models.CharField(max_length=5000, default='')
    heading_1 = models.CharField(max_length=200, default='')
    cheading_1 = models.CharField(max_length=5000, default='')
    heading_2 = models.CharField(max_length=200, default='')
    cheading_2 = models.CharField(max_length=5000, default='')
    thumbnail = models.ImageField(upload_to='blog/post/', null=True, blank=True)
    pub_date = models.DateField()
    created_by = models.CharField(max_length=50, null=True, blank=True)
    creation_time = models.DateTimeField(auto_now=False, auto_now_add=True,null=True)

    def __str__(self):
        return self.title
