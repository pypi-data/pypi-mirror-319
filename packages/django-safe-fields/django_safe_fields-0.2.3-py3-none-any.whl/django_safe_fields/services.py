from django.apps import apps
from django_safe_fields.fields import SafeFieldMixinBase
from zenutils.cipherutils import MappingCipher

__all__ = [
    "get_all_mapping_cipher_field_seeds",
]


def get_all_mapping_cipher_field_seeds():
    infos = {}
    for app_label, models in apps.all_models.items():
        for model_name, model in models.items():
            for field in model._meta.fields:
                if isinstance(field, SafeFieldMixinBase):
                    cipher = getattr(field, "cipher")
                    if cipher and isinstance(cipher, MappingCipher):
                        cipher_seeds = cipher.dumps()
                        infos[str(field)] = cipher_seeds
    return infos
