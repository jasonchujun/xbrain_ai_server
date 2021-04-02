from extract.views import *
from django.shortcuts import render
from django.http import FileResponse
import PyPDF2
import markdown
import uuid


def index(request):
    return HttpResponse("Hello World!")


def text_embedding(request):
    try:
        if request.method == 'POST':
            text = request.POST.get('text')
            res = []
            for elm in json.loads(text):
                # print(text_embedding_ins.get_last_hidden_states(elm['content']))
                elm['embedding'] = text_embedding_ins.encode(elm['content']).tolist()
                res.append(elm)
            return JsonResponse({'content': res})
        return HttpResponse(404)
    except Exception as e:
        traceback.print_exc()


def extract_docx(request):
    try:
        if request.method == 'POST':
            upload_file = BytesIO(request.FILES.get("upload_file").read())
            docx_extract = BaseDocxExtract(upload_file)
            return JsonResponse({'content': docx_extract.get_docx_structure()})
        return HttpResponse(404)
    except Exception as e:
        traceback.print_exc()


def semantic_search_file_name(request):
    try:
        if request.method == 'GET':
            text = request.GET.get("text")
            top_results = text_embedding_ins.cal_cos_sim(list(name_vecs.name_embedding.values), text_embedding_ins.encode(text), 20)
            return JsonResponse({'content': json.loads(name_vecs.loc[top_results[1].tolist(), ['path', 'name']].to_json(orient="records"))})
        return HttpResponse(404)
    except Exception as e:
        traceback.print_exc()


def semantic_search_file_dir(request):
    try:
        if request.method == 'GET':
            text = request.GET.get("text")
            top_results = text_embedding_ins.cal_cos_sim(list(catalog_vecs.embedding.values), text_embedding_ins.encode(text), 20)
            return JsonResponse({'content': json.loads(catalog_vecs.loc[top_results[1].tolist(), ['path', 'chapter', 'title', 'path_content']].to_json(orient="records"))})
        return HttpResponse(404)
    except Exception as e:
        traceback.print_exc()


def semantic_search_file_content(request):
    try:
        if request.method == 'GET':
            text = request.GET.get("text")
            top_results = text_embedding_ins.cal_cos_sim(list(content_vecs.embedding.values), text_embedding_ins.encode(text), 20)
            return JsonResponse({'content': json.loads(content_vecs.loc[top_results[1].tolist(), ['path', 'content']].to_json(orient="records"))})
        return HttpResponse(404)
    except Exception as e:
        traceback.print_exc()


def semantic_search_image_desc(request):
    try:
        if request.method == 'GET':
            text = request.GET.get("text")
            top_results = text_embedding_ins.cal_cos_sim(list(images_vecs.desc_embeddings.values), text_embedding_ins.encode(text), 20)
            return JsonResponse({'content': json.loads(images_vecs.loc[top_results[1].tolist(), ['path', 'desc']].to_json(orient="records"))})
        return HttpResponse(404)
    except Exception as e:
        traceback.print_exc()


def semantic_search_image_content(request):
    try:
        if request.method == 'GET':
            text = request.GET.get("text")
            top_results = text_embedding_ins.cal_cos_sim(list(images_vecs.content_embeddings.values), text_embedding_ins.encode(text), 20)
            return JsonResponse({'content': json.loads(images_vecs.loc[top_results[1].tolist(), ['path', 'content']].to_json(orient="records"))})
        return HttpResponse(404)
    except Exception as e:
        traceback.print_exc()


def get_content_html(request):
    index = request.GET.get("index")
    path = request.GET.get("path")
    doc = semantic_search_file_content()
    result = markdown.markdown("# Search Result! \r")
    count = 0
    image_num = 0
    for elm in doc:
        if elm['type'] == 'text':
            if 'Heading ' in elm['style']:
                level = ''.join(["#" for _ in range(0, int(elm['style'].split(' ')[1]) + 1)]) + ' '
                result = result + markdown.markdown(level + catalog['catalog'][count]['chapter'] + ' ' + elm['content'] + " \r")
                count += 1
            else:
                if 'List' in elm['style']:
                    result = result + markdown.markdown("* " + elm['content'] + " \r")
                else:
                    result = result + markdown.markdown(elm['content'] + " \r")

        if elm['type'] == 'image':
            img = Image.open(BytesIO(bytes(elm['content'])))
            img = img.resize((450, 300), Image.ANTIALIAS)
            img.save('assets/' + uuid.uuid4() + '.png')
            result = result + markdown.markdown("![test](get_image/?path=assets/" + uuid.uuid4() + ".png)" + " \r").replace(
                "src=\"", "src=\"http://localhost:8001/extract/"
            )

        if elm['type'] == 'table':
            table = elm['content'].to_markdown(index=False)
            result = result + markdown.markdown(table + " \r", extensions=['markdown.extensions.fenced_code',
                                              'markdown.extensions.tables']).replace('table',
                                                                                     'table border="1" cellspacing="0"')

    return render(request, './base.html', {'content': result})

# def get_doc_html(request):
#     try:
#         if request.method == 'GET':
#             path = request.GET.get("path")
#             with open(path, "rb") as docx_file:
#                 result = mammoth.convert_to_html(docx_file, convert_image=mammoth.images.img_element(convert_image))
#                 html = result.value  # The generated HTML
#             return render(request, './base.html', {'content': html})
#         return HttpResponse(404)
#     except Exception as e:
#         traceback.print_exc()


def get_pdf_html(request):
    # pdfWriter = PyPDF2.PdfFileWriter()
    # pdfFileObj = open(request.GET.get("path"), 'rb')
    # pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # pageObj = pdfReader.getPage(1)
    # pdfWriter.addPage(pageObj)
    # with open("page.pdf", "wb") as output:
    #     pdfWriter.write(output)
    return FileResponse(open(request.GET.get("path"), 'rb'), content_type='application/pdf')


def convert_image(image):
    with image.open() as image_bytes:
        encoded_src = base64.b64encode(image_bytes.read()).decode("ascii")

    return {
        "src": "data:{0};base64,{1}".format(image.content_type, encoded_src)
    }


def get_image(request):
    image_data = open(request.GET.get("path"), "rb").read()
    # image_data = base64.b64encode(image_data)
    return HttpResponse(image_data, content_type="image/jpeg")