from rest_framework import generics
from .models import Folder, File, ImageFile, VideoFile
from .serializers import FolderSerializer, FileSerializer, ImageFileSerializer, VideoFileSerializer
from .permissons import IsOwnerOrShared
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
    

class VideoFileListView(generics.ListAPIView):
    serializer_class = VideoFileSerializer

    def get_queryset(self):
        folder_id = self.kwargs.get('folder_id')
        if folder_id:
            return VideoFile.objects.filter(Folder_id=folder_id, is_trashed=False)
        return VideoFile.objects.filter(is_trashed=False)
    
class VideoFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrShared]
    serializer_class =  VideoFileSerializer

    def get_queryset(self):
        return VideoFile.objects.filter(Q(user=self.request.user) | Q(folder__is_shared=True, folder__shared_with=self.request.user))
    

class FolderListView(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrShared]
    serializer_class = FolderSerializer

    def get_queryset(self):
        return Folder.objects.filter(Q(user=self.request.user) | Q(is_shared=True, shared_with=self.request.user))

class FolderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrShared]
    serializer_class = FolderSerializer

    def get_queryset(self):
        return Folder.objects.filter(Q(user=self.request.user) | Q(is_shared=True, shared_with=self.request.user))

class FileListView(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrShared]
    serializer_class = FileSerializer

    def get_queryset(self):
        folder_id = self.request.query_params.get('folder', None)
        queryset = File.objects.filter(Q(user=self.request.user) | Q(folder__is_shared=True, folder__shared_with=self.request.user))
        if folder_id:
            queryset = queryset.filter(folder_id=folder_id)
        return queryset

class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrShared]
    serializer_class = FileSerializer

    def get_queryset(self):
        return File.objects.filter(Q(user=self.request.user) | Q(folder__is_shared=True, folder__shared_with=self.request.user))

class ImageFileListView(generics.ListCreateAPIView):
    permission_classes = [IsOwnerOrShared]
    serializer_class = ImageFileSerializer

    def get_queryset(self):
        folder_id = self.request.query_params.get('folder', None)
        queryset = ImageFile.objects.filter(Q(user=self.request.user) | Q(folder__is_shared=True, folder__shared_with=self.request.user))
        if folder_id:
            queryset = queryset.filter(folder_id=folder_id)
        return queryset

class ImageFileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrShared]
    serializer_class = ImageFileSerializer

    def get_queryset(self):
        return ImageFile.objects.filter(Q(user=self.request.user) | Q(folder__is_shared=True, folder__shared_with=self.request.user))

def get_folder_files(request, pk):
    folder = get_object_or_404(Folder, pk=pk)
    files = folder.files.all()
    images = folder.images.all()

    files_data = [
        {
            'id': file.id,
            'name': file.name,
            'description': file.description,
            'created_at': file.created_at,
            'updated_at': file.updated_at,
            'size': file.size,
            'is_public': file.is_public,
            'is_shared': file.is_shared,
            'shared_at': file.shared_at,
            'is_trashed': file.is_trashed,
            'trashed_at': file.trashed_at,
            'is_deleted': file.is_deleted,
            'deleted_at': file.deleted_at,
            'is_starred': file.is_starred,
            'starred_at': file.starred_at,
            'is_encrypted': file.is_encrypted,
            'encrypted_at': file.encrypted_at,
            'is_locked': file.is_locked,
            'locked_at': file.locked_at,
            'is_protected': file.is_protected,
            'protected_at': file.protected_at,
            'file': file.file.url,
        }
        for file in files
    ]

    images_data = [
        {
            'id': image.id,
            'name': image.name,
            'is_trashed': image.is_trashed,
            'trashed_at': image.trashed_at,
            'is_deleted': image.is_deleted,
            'deleted_at': image.deleted_at,
            'is_starred': image.is_starred,
            'starred_at': image.starred_at,
            'is_encrypted': image.is_encrypted,
            'encrypted_at': image.encrypted_at,
            'is_locked': image.is_locked,
            'locked_at': image.locked_at,
            'is_protected': image.is_protected,
            'protected_at': image.protected_at,
            'is_archived': image.is_archived,
            'is_shared': image.is_shared,
            'image': image.image.url,
        }
        for image in images
    ]

    return JsonResponse({'files': files_data, 'images': images_data})



