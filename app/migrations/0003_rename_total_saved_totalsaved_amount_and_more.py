# Generated by Django 4.1.7 on 2023-03-21 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_rename_savinggoals_savinggoal"),
    ]

    operations = [
        migrations.RenameField(
            model_name="totalsaved",
            old_name="total_saved",
            new_name="amount",
        ),
        migrations.RenameField(
            model_name="totalsaved",
            old_name="total_saved_currency",
            new_name="amount_currency",
        ),
    ]
