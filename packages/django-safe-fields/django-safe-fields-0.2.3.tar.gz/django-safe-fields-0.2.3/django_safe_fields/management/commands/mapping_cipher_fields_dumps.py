import json
from django.core.management.base import BaseCommand
from django_safe_fields.services import get_all_mapping_cipher_field_seeds


class Command(BaseCommand):
    help = "Dump All Mapping Cipher Fields"

    def add_arguments(self, parser):
        parser.add_argument(
            "-n", "--name", help="Dump mapping cipher fields to the variable..."
        )

    def handle(self, *args, **options):
        name = options.get("name", None)
        infos = get_all_mapping_cipher_field_seeds()
        text = json.dumps(infos, indent=4, ensure_ascii=True, sort_keys=True)
        if name:
            print(name, "=", text)
        else:
            print(text)
