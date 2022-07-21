from django.core.mail import EmailMessage
from django.utils import timezone
from django_cron import CronJobBase, Schedule


class EnviarEmails(CronJobBase):
    """Envia os e-mails cadastrados no banco de dados, verificando atualizações a cada 1 minuto.

    (Revisar)
    """

    tempo = 1
    schedule = Schedule(run_every_mins=tempo)
    code = "principal.views.EnviarEmails"

    def do(self):
        consultorias = Consultoria.objects.filter(
            enviado=False, dataHoraEnvio__lte=timezone.now()
        )

        for consultoria in consultorias:
            email = EmailMessage(
                subject=consultoria.empresa,
                body=consultoria.mensagem,
                from_email='"Julyanna Veras" <administracao@mazzollisistemas.com.br>',
                to=[consultoria.email],
                bcc=["mazzolli@mazzollisistemas.com.br"],
                reply_to=["administracao@mazzollisistemas.com.br"],
                headers={},
            )
            email.content_subtype = "html"
            email.send()

            consultoria.enviado = True
            consultoria.save()
