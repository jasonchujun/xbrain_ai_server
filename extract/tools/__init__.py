import re
import os
import torch
import base64
import win32com
import platform
from sentence_transformers import SentenceTransformer, util
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
from pptx import Presentation
import pandas as pd
from io import BytesIO
from PIL import Image
from docx.shared import Pt
import numpy as np
import docx