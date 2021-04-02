from django.urls import path

from .views import views

urlpatterns = [
    path('', views.index, name='index'),
    path('text_embedding', views.text_embedding),
    path('extract_docx', views.extract_docx),
    path('semantic_search_file_name', views.semantic_search_file_name),
    path('semantic_search_file_dir', views.semantic_search_file_dir),
    path('semantic_search_file_content', views.semantic_search_file_content),
    path('semantic_search_image_desc', views.semantic_search_image_desc),
    path('semantic_search_image_content', views.semantic_search_image_content),
    path('get_pdf_html', views.get_pdf_html),
]
