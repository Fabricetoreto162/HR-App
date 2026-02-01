from django.db import models
from datetime import time
import uuid
from io import BytesIO
import qrcode
from django.core.files.base import ContentFile

class Employee(models.Model):
    full_name = models.CharField(max_length=150)
    position = models.CharField(max_length=100)
    work_start_time = models.TimeField()
    work_end_time = models.TimeField()
    is_active = models.BooleanField(default=True)

    # Identification unique + QR code
    unique_code = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        # Sauvegarder d'abord pour obtenir un ID si nouveau
        if not self.id:
            super().save(*args, **kwargs)

        # Générer le QR code si non existant
        if not self.qr_code:
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=4
            )
            qr.add_data(str(self.unique_code))
            qr.make(fit=True)
            img = qr.make_image(fill_color='black', back_color='white')

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            # On utilise l'ID pour éviter None et caractères spéciaux
            file_name = f"{self.full_name.replace(' ', '_')}_{self.id}.png"
            self.qr_code.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)

    def str(self):
        return self.full_name