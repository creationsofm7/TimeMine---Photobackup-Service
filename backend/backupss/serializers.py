from rest_framework import serializers
from rest_framework.fields import HiddenField
from .models import Folder, File, ImageFile, VideoFile
from django.contrib.auth import get_user_model

class FileSerializer(serializers.ModelSerializer):
    user = HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = File
        fields = '__all__'
        
class ImageFileSerializer(serializers.ModelSerializer):
    user = HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = ImageFile
        fields = '__all__'

class VideoFileSerializer(serializers.ModelSerializer):
    user = HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = VideoFile
        fields = '__all__'

class FolderSerializer(serializers.ModelSerializer):
    user = HiddenField(default=serializers.CurrentUserDefault())
    files = FileSerializer(many=True, read_only=True)
    images = ImageFileSerializer(many=True, read_only=True)
    videos = VideoFileSerializer(many=True, read_only=True)
    shared_with = serializers.PrimaryKeyRelatedField(many=True, queryset=get_user_model().objects.all(), required=False)

    subfolders = serializers.SerializerMethodField()
    
    class Meta:
        model = Folder
        fields = [
            'id',
            'name',
            'user',
            'parent_folder',
            'subfolders',
            'description',
            'created_at',
            'updated_at',
            'size',
            'is_public',
            'is_shared',
            'shared_with',
            'shared_at',
            'is_trashed',
            'trashed_at',
            'is_deleted',
            'deleted_at',
            'is_starred',
            'starred_at',
            'is_encrypted',
            'encrypted_at',
            'is_locked',
            'locked_at',
            'is_fav',
            'is_protected',
            'protected_at',
            'files',
            'images',
            'videos',
        ]

    def get_subfolders(self, instance):
        # Recursively serialize subfolders
        serializer = FolderSerializer(instance.subfolders.all(), many=True)
        return serializer.data
    
    
    
    def create(self, validated_data):
        shared_with = validated_data.pop('shared_with', [])
        files_data = self.context.get('request').data.get('files', [])
        images_data = self.context.get('request').data.get('images', [])
        videosdata = self.context.get('request').data.get('videos', [])
        
        folder = Folder.objects.create(**validated_data)
        folder.shared_with.set(shared_with)
        
        for file_data in files_data:
            File.objects.create(folder=folder, **file_data)
        
        for image_data in images_data:
            ImageFile.objects.create(folder=folder, **image_data)
        
        for video_data in videosdata:
            VideoFile.objects.create(folder=folder, **video_data)
        
        return folder

    def update(self, instance, validated_data):
        shared_with = validated_data.pop('shared_with', None)
        files_data = self.context.get('request').data.get('files', [])
        images_data = self.context.get('request').data.get('images', [])
        videos_data = self.context.get('request').data.get('videos', [])
        
        instance = super().update(instance, validated_data)
        
        if shared_with is not None:
            instance.shared_with.set(shared_with)
        
        for file_data in files_data:
            file_id = file_data.get('id')
            if file_id:
                file = File.objects.get(id=file_id, folder=instance)
                for key, value in file_data.items():
                    setattr(file, key, value)
                file.save()
            else:
                File.objects.create(folder=instance, **file_data)
        
        for image_data in images_data:
            image_id = image_data.get('id')
            if image_id:
                image = ImageFile.objects.get(id=image_id, folder=instance)
                for key, value in image_data.items():
                    setattr(image, key, value)
                image.save()
            else:
                ImageFile.objects.create(folder=instance, **image_data)
            
        for video_data in videos_data:
            video_id = video_data.get('id')
            if video_id:
                video = VideoFile.objects.get(id=video_id, folder=instance)
                for key, value in video_data.items():
                    setattr(video, key, value)
                video.save()
            else:
                VideoFile.objects.create(folder=instance, **video_data)
        
        return instance