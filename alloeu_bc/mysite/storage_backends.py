import os
from django.core.files.storage import Storage
from django.core.files.base import ContentFile
from supabase import create_client, Client

class SupabaseStorage(Storage):
    def __init__(self):
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")  # clé admin
        self.bucket = os.getenv("SUPABASE_BUCKET", "media")  # nom du bucket
        self.client: Client = create_client(self.supabase_url, self.supabase_key)

    def _save(self, name, content):
        # lecture en bytes
        if hasattr(content, 'read'):
            file_bytes = content.read()
        else:
            file_bytes = content

        # upload vers supabase
        self.client.storage.from_(self.bucket).upload(name, file_bytes, {
            "content-type": getattr(content, "content_type", "application/octet-stream")
        })
        return name

    def url(self, name):
        # URL publique
        return f"{self.supabase_url}/storage/v1/object/public/{self.bucket}/{name}"

    def exists(self, name):
        # vérifier si le fichier existe
        try:
            res = self.client.storage.from_(self.bucket).list(path=name)
            return len(res) > 0
        except Exception:
            return False
