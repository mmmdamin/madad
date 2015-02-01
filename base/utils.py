from django.utils.crypto import get_random_string


def make_random_password(length=10,
                         allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                       'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                       '23456789'):
    """
    Generates a random password with the given length and given
    allowed_chars. Note that the default value of allowed_chars does not
    have "I" or "O" or letters and digits that look similar -- just to
    avoid confusion.
    """
    return get_random_string(length, allowed_chars)


def save_file(in_memory_file):
    import os
    from django.core.files.storage import default_storage
    from django.core.files.base import ContentFile
    from django.conf import settings

    path = default_storage.save('data_file/' + str(in_memory_file), ContentFile(in_memory_file.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, path)
    return tmp_file

