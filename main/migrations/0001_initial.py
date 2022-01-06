# Generated by Django 3.2.9 on 2022-01-05 18:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('MR', 'Mirrorless'), ('DSLR', 'DSRL'), ('CC', 'Compacta')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Marca',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(choices=[('Canon', 'Canon'), ('Nikon', 'Nikon'), ('Sony', 'Sony')], max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Camara',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField()),
                ('sensor', models.TextField()),
                ('iso', models.TextField()),
                ('procesador', models.TextField()),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6)),
                ('marca', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.marca')),
                ('tipo', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.categoria')),
            ],
        ),
    ]
