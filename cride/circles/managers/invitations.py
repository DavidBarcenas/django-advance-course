from django.db import models
from string import ascii_uppercase, digits
import random

class InvitationManager(models.Manager):
    """Invitation manager
    
    Used to handle code creation.
    """

    CODE_LENGTH = 10

    def create(self, **kwargs):
        pool = ascii_uppercase + digits + '.-'
        code = kwargs.get('code', ''.join(random.choices(pool, k=self.CODE_LENGTH)))

        while self.filter(code=code).exists():
            code = ''.join(random.choices(pool, k=self.CODE_LENGTH))

        kwargs['code'] = code

        return super(InvitationManager, self).create(**kwargs)