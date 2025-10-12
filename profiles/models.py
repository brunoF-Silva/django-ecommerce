import re
from utils.validacpf import valida_cpf

from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError


class UserProfile(models.Model):
    '''Model to store user profile information.'''
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birthdate = models.DateField()
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    address = models.CharField(max_length=50)
    number = models.CharField(max_length=5)
    complement = models.CharField(max_length=30)
    neighborhood = models.CharField(max_length=30)
    zip_code = models.CharField(max_length=8)
    city = models.CharField(max_length=30)
    state = models.CharField(
        max_length=2,
        default = 'SP',
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),   
        )
    )
    
    def __str__(self):
        return f"{self.user}"
    
    def clean(self):
        error_messages = {}
        
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Invalid Brazilian CPF number.'
        
        if re.search(r'[^0-9]', self.zip_code) or len(self.zip_code) < 8:
            error_messages['zip_code'] = 'Brazilian ZIP code must contain 8 numbers.'
            
        if error_messages:
            raise ValidationError(error_messages)
    
    class Meta:
        ''' Meta class for UserProfile model. '''
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'