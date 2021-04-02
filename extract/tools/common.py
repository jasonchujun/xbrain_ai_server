import os
import pandas as pd


def walk_file(file):
    res = []
    for root, dirs, files in os.walk(file):

        # root 表示当前正在访问的文件夹路径
        # dirs 表示该文件夹下的子目录名list
        # files 表示该文件夹下的文件list

        # 遍历文件
        for f in files:
            if os.path.join(root, f).split('.')[1] in ['docx']:
                res.append(os.path.join(root, f))

        # 遍历所有的文件夹
    #         for d in dirs:
    #             print(os.path.join(root, d))
    return res


def query_with(kv):
    doc = {
        "query": {
            "bool": {
                "must": []
            }
        }
    }
    for k, v in kv:
        doc["query"]["bool"]["must"].append({"term": {k: v}})
    return doc


def load_vecs(es_ctrl):
    name_vecs = pd.DataFrame([], columns=['path', 'name', 'name_embedding'])
    catalog_vecs = pd.DataFrame([], columns=['path', 'chapter', 'title', 'path_content'])
    content_vecs = pd.DataFrame([], columns=['path', 'index', 'content', 'embedding'])
    images_vecs = pd.DataFrame([],
                               columns=['path', 'index', 'desc', 'content', 'desc_embeddings', 'content_embeddings'])

    data = []
    for i in range(0, 5):
        data.extend(es_ctrl.search(index='hunter-sharepoint-text-embedding', from_=i * 100, size=100)['hits']['hits'])
    for i, res in enumerate(data):
        #     res = es_ctrl.search(index='hunter-sharepoint-text-embedding', body=query_with([['path', elm]]))['hits']['hits']
        if len(res) > 0:
            name_vecs.loc[i, ['path', 'name', 'name_embedding']] = [res['_source']['path'], res['_source']['name'],
                                                                    res['_source']['name_embedding']]

            tmp = pd.DataFrame(res['_source']['content_embedding'])
            tmp['path'] = res['_source']['path']
            content_vecs = content_vecs.append(tmp).reset_index(drop=True)

            if len(res['_source']['content_embedding']) > 0:
                tmp = pd.DataFrame(res['_source']['catalog_embedding'])
                tmp['path'] = res['_source']['path']
                catalog_vecs = catalog_vecs.append(tmp).reset_index(drop=True)

            if len(res['_source']['images_embedding']) > 0:
                tmp = pd.DataFrame(res['_source']['images_embedding'])
                tmp['path'] = res['_source']['path']
                images_vecs = images_vecs.append(tmp).reset_index(drop=True)

    name_vecs = name_vecs.reset_index(drop=True)
    return name_vecs, catalog_vecs, content_vecs, images_vecs
