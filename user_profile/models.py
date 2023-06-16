from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class MyUser(models.Model):

    id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=20)
    last_name=models.CharField(max_length=20)
    email=models.EmailField(max_length=75,db_column='email',
        validators=[
            RegexValidator(
                r'[^@]+@[^@]+\.[^@]+',
                'Enter a valid email.'
            )
        ])
    password=models.CharField(max_length=20)
    phone_number = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                r'^01[0125][0-9]{8}$',
                'Enter a valid Egyption phone number.'
            )
        ]
    )
    image = models.ImageField(upload_to='static/profile_pictures')
    
    birth_date= models.DateField(default='1990-12-12')
    facebook_profile= models.CharField(default='https://www.facebook.com')
    country= models.CharField(default='Egypt')

    def __str__(self) -> str:
        return self.first_name+" "+self.last_name