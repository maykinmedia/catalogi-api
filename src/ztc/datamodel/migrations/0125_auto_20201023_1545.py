# Generated by Django 2.2.4 on 2020-10-23 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('datamodel', '0124_auto_20201023_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eigenschap',
            name='zaaktype',
            field=models.ForeignKey(help_text='URL-referentie naar het ZAAKTYPE van de ZAAKen waarvoor deze EIGENSCHAP van belang is.', on_delete=django.db.models.deletion.CASCADE, to='datamodel.ZaakType', verbose_name='Zaaktype'),
        ),
        migrations.AlterField(
            model_name='informatieobjecttype',
            name='catalogus',
            field=models.ForeignKey(help_text='URL-referentie naar de CATALOGUS waartoe dit INFORMATIEOBJECTTYPE behoort.', on_delete=django.db.models.deletion.CASCADE, to='datamodel.Catalogus', verbose_name='Catalogus'),
        ),
        migrations.AlterField(
            model_name='roltype',
            name='zaaktype',
            field=models.ForeignKey(help_text='URL-referentie naar het ZAAKTYPE waar deze ROLTYPEn betrokken kunnen zijn.', on_delete=django.db.models.deletion.CASCADE, to='datamodel.ZaakType', verbose_name='Zaaktype'),
        ),
        migrations.AlterField(
            model_name='statustype',
            name='zaaktype',
            field=models.ForeignKey(help_text='URL-referentie naar het ZAAKTYPE van ZAAKen waarin STATUSsen van dit STATUSTYPE bereikt kunnen worden.', on_delete=django.db.models.deletion.CASCADE, related_name='statustypen', to='datamodel.ZaakType', verbose_name='Zaaktype'),
        ),
        migrations.AlterField(
            model_name='zaaktype',
            name='catalogus',
            field=models.ForeignKey(help_text='URL-referentie naar de CATALOGUS waartoe dit ZAAKTYPE behoort.', on_delete=django.db.models.deletion.CASCADE, to='datamodel.Catalogus', verbose_name='Catalogus'),
        ),
    ]
