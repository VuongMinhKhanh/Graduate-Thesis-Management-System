# Generated by Django 5.0.4 on 2024-04-09 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graduatethesis', '0004_alter_tieuchi_id_kltn'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hoidongbvkl',
            name='tinh_trang',
        ),
        migrations.RemoveField(
            model_name='lop',
            name='tinh_trang_lop',
        ),
        migrations.RemoveField(
            model_name='nghanhhoc',
            name='tinh_trang',
        ),
        migrations.AddField(
            model_name='hoidongbvkl',
            name='trang_thai',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lop',
            name='trang_thai',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='nghanhhoc',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='nghanhhoc',
            name='trang_thai',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='nghanhhoc',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='diem',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='diem',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='giangvien',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='giangvien',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='giaovu',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='giaovu',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='hoidongbvkl',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='hoidongbvkl',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='khoaluantotnghiep',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='khoaluantotnghiep',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='kltngvhuongdan',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='kltngvhuongdan',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='lop',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='lop',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='lophocnghanhhoc',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='lophocnghanhhoc',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='sinhvien',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='sinhvien',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='tieuchi',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='tieuchi',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='vaitro',
            name='created_date',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='vaitro',
            name='updated_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
