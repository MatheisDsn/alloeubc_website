from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("annonces", "0002_alter_annonce_price"),
    ]

    operations = [
        migrations.RunSQL(
            sql=
            """
            ALTER TABLE annonces_annonce
            ADD COLUMN IF NOT EXISTS price numeric(8,2) NOT NULL DEFAULT 0.00;
            """,
            reverse_sql=
            """
            ALTER TABLE annonces_annonce
            DROP COLUMN IF EXISTS price;
            """,
        ),
    ]
