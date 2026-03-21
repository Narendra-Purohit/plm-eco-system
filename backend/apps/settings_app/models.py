from django.db import models


class ECOStage(models.Model):
    name            = models.CharField(max_length=100)
    sequence        = models.IntegerField()
    is_default_new  = models.BooleanField(default=False)
    is_default_done = models.BooleanField(default=False)

    class Meta:
        ordering = ['sequence']

    def __str__(self):
        tag = ''
        if self.is_default_new: tag = ' [NEW]'
        if self.is_default_done: tag = ' [DONE]'
        return f'{self.sequence}. {self.name}{tag}'
