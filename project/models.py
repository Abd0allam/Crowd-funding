from django.db import models
from user_profile.models import *
from django.db.models import Avg,Sum
from datetime import datetime



# Create your models here.
# from django.db import models
# from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=50, primary_key=True ,default="helpDesoky")
    def __str__(self) -> str:
        return self.name

class Projects(models.Model):
    #id,title,details,category,target,start_date,end_date,owener_email,total_rate,repor_count
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255,unique=True)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    target = models.IntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    owner_id = models.ForeignKey(MyUser, on_delete=models.CASCADE ,null=True)  #### owner_email
    total_rate = models.DecimalField(max_digits=3, decimal_places=2,default=0)
    report_count = models.IntegerField(default=0) ###  report_count
    created_at = models.DateField(default=datetime.now)


    def calculate_total_rating(self):
        ratings = Rating.objects.filter(project=self)
        if ratings.exists():
            self.total_rate = ratings.aggregate(Avg('rate'))['rate__avg']
        else:
            self.total_rate = 0
    
    def calculate_total_report(self):
        reports = Report.objects.filter(project=self)
        if reports.exists():
            self.report_count = reports.aggregate(Sum('report_state'))['report_state__sum']
        else:
            self.report_count = 0

class Adminproject(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)

class Tag(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    tag_name = models.CharField(max_length=50)

class Image(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='static/project_pictures')
    # def __str__(self):
    #     return str(self.picture)
    
class Donation(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    donate_amount = models.IntegerField()

class Comment(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    comment_body = models.TextField()
    report_comment = models.BooleanField(default=False)
    # user_report = models.CharField()

class Report(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    report_state=models.IntegerField()

    def save(self, *args, **kwargs):
        super(Report, self).save(*args, **kwargs)
        self.project.calculate_total_report()
        self.project.save()

class Rating(models.Model):
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    user_id = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    rate = models.IntegerField()
    
    def save(self, *args, **kwargs):
        super(Rating, self).save(*args, **kwargs)
        self.project.calculate_total_rating()
        self.project.save()

