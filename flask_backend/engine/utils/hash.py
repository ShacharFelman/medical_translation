import hashlib


def create_file_hash_id(file):
    """Create a cache key for a file using its content."""
    hasher = hashlib.sha256()
    with open(file, 'rb') as f:
        file_content = f.read()
        hasher.update(file_content)
    cache_key = hasher.hexdigest()
    return cache_key


def create_file_hash_id_from_key(file_key:str):
    """Create a cache key for a file using its content."""
    hasher = hashlib.sha256()
    file_key_encoding = file_key.encode("utf-8")
    hasher.update(file_key_encoding)
    cache_key = hasher.hexdigest()
    return cache_key


def create_string_hash(content: str):
    """Calculate a hash for the given string content."""
    hasher = hashlib.sha256()
    content_encoding = content.encode("utf-8")
    hasher.update(content_encoding)
    return hasher.hexdigest()