from django.db import models
from django.conf import settings

  
  
class Entrys(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    json = models.CharField(max_length=100)
    project = models.ForeignKey(
        'Project',
        related_name='entries',
        on_delete=models.CASCADE
    )
    

class Project(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.name

# class Documentation(models.Model):
#     name = models.CharField(max_length=100)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE
#     )
#     title = models.CharField(max_length=100)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title

