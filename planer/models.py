from django.db import models
from django.shortcuts import reverse


class Documents(models.Model):
    PERIOD = (
        (1, 'Неделя'),
        (2, 'Месяц'),
        (3, 'Квартал'),
        (4, 'Год'),
    )
    document_name = models.CharField(max_length=256,
                                     db_index=True,
                                     blank=False,
                                     verbose_name='Название документа')
    period = models.PositiveSmallIntegerField(choices=PERIOD,
                                              verbose_name='Период')
    description = models.TextField(blank=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['id']

    def __str__(self):
        return f'{self.document_name}'

    def get_absolute_url(self):
        return reverse('document_detail', kwargs={'pk': self.id})
