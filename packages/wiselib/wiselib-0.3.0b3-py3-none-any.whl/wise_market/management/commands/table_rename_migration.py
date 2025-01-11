import importlib
import os

from django.conf import settings
from django.core.management import BaseCommand, call_command
from django.db import migrations


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "app_label",
            type=str,
            help="The app for which to create the migration.",
            default="market",
        )

    def handle(self, *args, **options):
        app_label = options["app_label"]

        call_command(
            "makemigrations", app_label, "--empty", "--name", "wise_rename_tables"
        )

        migrations_dir = os.path.join(settings.BASE_DIR, app_label, "migrations")
        migration_files = sorted(
            f
            for f in os.listdir(migrations_dir)
            if f.endswith(".py") and f.startswith("0")
        )

        if not migration_files:
            self.stderr.write("No migration files found!")
            return

        migration_file = os.path.join(migrations_dir, migration_files[-1])
        self.stdout.write(f"Located migration file: {migration_file}")

        spec = importlib.util.spec_from_file_location(
            "migration_module", migration_file
        )
        migration_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(migration_module)

        migration = migration_module.Migration

        migration.operations.append(
            migrations.SeparateDatabaseAndState(
                database_operations=[
                    *(
                        migrations.AlterModelTable(
                            model, f"wise_market_{model.lower()}"
                        )
                        for model in _models
                    )
                ]
            )
        )
