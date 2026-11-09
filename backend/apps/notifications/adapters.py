from django.core.mail import send_mail
from django.conf import settings

class SMTPEmailAdapter:
    @staticmethod
    def enviar_correo(destinatario_email, asunto, mensaje):
        try:
            send_mail(
                subject=asunto,
                message=mensaje,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[destinatario_email],
                fail_silently=False,
            )
            return True
        except Exception as e:
            raise Exception(f"Error SMTP: {str(e)}")