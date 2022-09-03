from django.db import models
from django.shortcuts import reverse

# Create your models here.


class Logs(models.Model):
    file_path = models.CharField(
        max_length=500, verbose_name="File Path")
    event_type = models.CharField(max_length=100, verbose_name="Event Type")
    created_date = models.DateTimeField(
        verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return self.event_type

    def get_update_url(self):
        return reverse('dlp:update_log', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('dlp:delete_log', kwargs={'id': self.id})


class Rule(models.Model):
    PERMISSION = [
        ('N', 'No Access'),
        ('F', 'Full Accsess'),
        ('M', 'Modify access'),
        ('RX', 'Read and execute access'),
        ('R', 'Read-only access'),
        ('W', 'Write-only access'),
    ]

    ACCSESS = [
        ('grant', 'grant'),
        ('deny', 'deny'),
        ('remove', 'remove'),
        ('setintegritylevel', 'setintegritylevel'),
    ]

    name = models.CharField(max_length=50, verbose_name="Rule Name")
    permission = models.CharField(
        default="F", choices=PERMISSION, max_length=50)
    accsess = models.CharField(default="grant", choices=ACCSESS, max_length=50)
    created_date = models.DateTimeField(
        verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ---> {self.permission} ---> {self.accsess}"

    def get_update_url(self):
        return reverse('dlp:update_rule', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('dlp:delete_rule', kwargs={'id': self.id})


class Policy(models.Model):
    name = models.CharField(
        max_length=500, verbose_name="Policy Name")
    logs = models.ManyToManyField(
        Logs, related_name="policy_logs", blank=True)
    rule = models.OneToOneField(Rule, on_delete=models.CASCADE)
    created_date = models.DateTimeField(
        verbose_name="Created Date", auto_now_add=True)

    def __str__(self):
        return f"{self.name} ---> {self.rule}"

    def get_update_url(self):
        return reverse('dlp:update_policy', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('dlp:delete_policy', kwargs={'id': self.id})
