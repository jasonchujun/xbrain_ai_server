import json
import traceback

from io import BytesIO
from django.http import HttpResponse
from django.http import JsonResponse
from elasticsearch import Elasticsearch
from extract.tools.common import *
from extract.tools.embedding import *
from extract.tools.extract_document import BaseDocxExtract

es_ctrl = Elasticsearch([{'host': 'localhost', 'port': 9200}])
name_vecs, catalog_vecs, content_vecs, images_vecs = load_vecs(es_ctrl)

text_embedding_ins = BaseSentenceEmbedding('paraphrase-distilroberta-base-v1')


