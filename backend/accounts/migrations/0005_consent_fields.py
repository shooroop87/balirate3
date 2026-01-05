from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0004_user_stripe_customer_id_consentlog"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="privacy_accepted",
            field=models.BooleanField(default=False, verbose_name="Datenschutz akzeptiert"),
        ),
        migrations.AddField(
            model_name="user",
            name="privacy_accepted_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Datenschutz akzeptiert am"),
        ),
        migrations.AddField(
            model_name="user",
            name="medical_data_consent",
            field=models.BooleanField(default=False, verbose_name="Einwilligung Gesundheitsdaten"),
        ),
        migrations.AddField(
            model_name="user",
            name="medical_data_consent_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Einwilligung Gesundheitsdaten am"),
        ),
        migrations.AddField(
            model_name="user",
            name="marketing_consent_at",
            field=models.DateTimeField(blank=True, null=True, verbose_name="Marketing-Einwilligung am"),
        ),
    ]