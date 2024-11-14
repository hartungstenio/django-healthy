from django.db import models


class Test(models.Model):
    summary = models.CharField(max_length=256)

    def __str__(self) -> str:
        return f"{self.pk}: {self.summary}"
