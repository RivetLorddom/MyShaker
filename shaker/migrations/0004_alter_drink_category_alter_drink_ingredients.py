# Generated by Django 4.0.4 on 2022-08-16 05:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shaker', '0003_alter_category_options_alter_glass_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='drink',
            name='category',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_listings', to='shaker.category'),
        ),
        migrations.AlterField(
            model_name='drink',
            name='ingredients',
            field=models.ManyToManyField(blank=True, default=None, related_name='used_for', to='shaker.ingredient'),
        ),
    ]