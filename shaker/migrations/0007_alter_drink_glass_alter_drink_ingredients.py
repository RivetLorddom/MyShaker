# Generated by Django 4.0.4 on 2022-08-16 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shaker', '0006_alter_drink_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drink',
            name='glass',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='used_for', to='shaker.glass'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='ingredients',
            field=models.ManyToManyField(blank=True, null=True, related_name='used_for', to='shaker.ingredient'),
        ),
    ]
