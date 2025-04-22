from datetime import timezone
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from PIL import Image

# Utility functions to generate file paths
def user_directory_path(instance, filename):
    return 'files/{0}/{1}'.format(instance.user.id, filename)

def user_image_directory_path(instance, filename):
    return 'files/{0}/images/{1}'.format(instance.user.id, filename)

def user_video_directory_path(instance, filename):
    return 'files/{0}/videos/{1}'.format(instance.user.id, filename)

def user_thumbnail_directory_path(instance, filename):
    return 'files/{0}/videos/thumbnails/{1}'.format(instance.user.id, filename)

class Folder(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent_folder = models.ForeignKey('self', on_delete=models.CASCADE, related_name='subfolders', null=True, blank=True)
    name = models.CharField(max_length=50, default='new folder')
    description = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_fav = models.BooleanField(default=False  )
    size = models.FloatField(null=True, blank=True)
    is_public = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='shared_with', blank=True)
    shared_at = models.DateTimeField(auto_now_add=True)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_starred = models.BooleanField(default=False)
    starred_at = models.DateTimeField(null=True, blank=True)
    is_encrypted = models.BooleanField(default=False)
    encrypted_at = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)
    is_protected = models.BooleanField(default=False)
    protected_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_trashed and not self.trashed_at:
            self.trashed_at = timezone.now()
        if self.is_deleted and not self.deleted_at:
            self.deleted_at = timezone.now()
        if self.is_starred and not self.starred_at:
            self.starred_at = timezone.now()
        if self.is_encrypted and not self.encrypted_at:
            self.encrypted_at = timezone.now()
        if self.is_locked and not self.locked_at:
            self.locked_at = timezone.now()
        if self.is_protected and not self.protected_at:
            self.protected_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class File(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='files')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.FloatField(null=True, blank=True)
    file = models.FileField(upload_to=user_directory_path)
    is_public = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)
    shared_at = models.DateTimeField(auto_now_add=True)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_starred = models.BooleanField(default=False)
    starred_at = models.DateTimeField(null=True, blank=True)
    is_encrypted = models.BooleanField(default=False)
    encrypted_at = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)
    is_protected = models.BooleanField(default=False)
    protected_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_trashed and not self.trashed_at:
            self.trashed_at = timezone.now()
        if self.is_deleted and not self.deleted_at:
            self.deleted_at = timezone.now()
        if self.is_starred and not self.starred_at:
            self.starred_at = timezone.now()
        if self.is_encrypted and not self.encrypted_at:
            self.encrypted_at = timezone.now()
        if self.is_locked and not self.locked_at:
            self.locked_at = timezone.now()
        if self.is_protected and not self.protected_at:
            self.protected_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class ImageFile(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='images')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default='Image')
    image = models.ImageField(upload_to=user_image_directory_path)
    image_height = models.IntegerField(null=True, blank=True)
    image_width = models.IntegerField(null=True, blank=True)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)
    is_starred = models.BooleanField(default=False)
    starred_at = models.DateTimeField(null=True, blank=True)
    is_encrypted = models.BooleanField(default=False)
    encrypted_at = models.DateTimeField(null=True, blank=True)
    is_locked = models.BooleanField(default=False)
    locked_at = models.DateTimeField(null=True, blank=True)
    is_protected = models.BooleanField(default=False)
    protected_at = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    is_shared = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.is_trashed and not self.trashed_at:
            self.trashed_at = timezone.now()
        if self.is_deleted and not self.deleted_at:
            self.deleted_at = timezone.now()
        if self.is_starred and not self.starred_at:
            self.starred_at = timezone.now()
        if self.is_encrypted and not self.encrypted_at:
            self.encrypted_at = timezone.now()
        if self.is_locked and not self.locked_at:
            self.locked_at = timezone.now()
        if self.is_protected and not self.protected_at:
            self.protected_at = timezone.now()
        if not self.pk and (self.image_height is None or self.image_width is None):
        
            if hasattr(self.image, 'file') and self.image.file:
                img = Image.open(self.image)
                self.image_width, self.image_height = img.size

       
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class VideoFile(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='videos')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default='Video')
    video = models.FileField(
        upload_to=user_video_directory_path,
        validators=[FileExtensionValidator(allowed_extensions=['mp4', 'avi', 'mov', 'wmv'])]
    )
    video_description = models.TextField(max_length=100, null=True, blank=True)
    video_thumbnail = models.ImageField(upload_to=user_thumbnail_directory_path)
    is_trashed = models.BooleanField(default=False)
    trashed_at = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.is_trashed and not self.trashed_at:
            self.trashed_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def clean(self):
        if self.video and self.video.size > 1024 * 1024 * 1024 * 4:  # 4 GB limit
            raise ValidationError("Video file size cannot exceed 4 GB.")
