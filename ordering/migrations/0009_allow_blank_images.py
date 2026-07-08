from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordering', '0008_alter_order_invoice_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='foods/',
            ),
        ),
        migrations.AlterField(
            model_name='offer',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='offers/',
            ),
        ),
    ]
