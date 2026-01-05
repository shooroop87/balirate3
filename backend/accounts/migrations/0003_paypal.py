from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_user_documents_verified_user_onboarding_completed_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="paypal_payer_id",
            field=models.CharField(blank=True, max_length=100, verbose_name="PayPal Payer ID"),
        ),
    ]