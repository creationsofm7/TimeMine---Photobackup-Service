from django.urls import path
from .views import (
    FolderListView, 
    FolderDetailView, 
    FileListView, 
    FileDetailView, 
    ImageFileListView, 
    ImageFileDetailView, VideoFileListView, VideoFileDetailView,
    get_folder_files
)

urlpatterns = [
    path('folders/', FolderListView.as_view(), name='folder-list'),
    path('folders/<int:pk>/', FolderDetailView.as_view(), name='folder-detail'),
    path('files/', FileListView.as_view(), name='file-list'),
    path('files/<int:pk>/', FileDetailView.as_view(), name='file-detail'),
    path('images/', ImageFileListView.as_view(), name='image-list'),
    path('images/<int:pk>/', ImageFileDetailView.as_view(), name='image-detail'),
    path('folders/<int:pk>/files/', get_folder_files, name='folder-files'),
    path('videos/', VideoFileListView.as_view(), name='video-list'),
    path('videos/<int:pk>/', VideoFileDetailView.as_view(), name='video-detail'),
    
    # New URL patterns for filtering files and images by folder
    path('folders/<int:folder_id>/files/', FileListView.as_view(), name='folder-file-list'),
    path('folders/<int:folder_id>/images/', ImageFileListView.as_view(), name='folder-image-list'),
    path('folders/<int:folder_id>/videos/', VideoFileListView.as_view(), name='folder-video-list'),
]