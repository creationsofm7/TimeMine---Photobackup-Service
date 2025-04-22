from django.contrib import admin
from .models import Folder, File, ImageFile, VideoFile

# Register your models here.
admin.site.register(Folder)
admin.site.register(File)
admin.site.register(ImageFile)
admin.site.register(VideoFile)