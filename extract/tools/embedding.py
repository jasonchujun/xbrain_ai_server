from extract.tools import *


class BaseSentenceEmbedding(object):

    def __init__(self, model):
        self.model = SentenceTransformer(model, device='cuda')

    def encode(self, text):
        return self.model.encode([text])

    def cal_cos_sim(self, vectors_array, embeddings, topk):
        cos_scores = util.pytorch_cos_sim(embeddings, vectors_array)[0]
        top_results = torch.topk(cos_scores, k=topk)
        return top_results

