from transformers import AutoTokenizer, AutoModel
#THUDM少了个模型
def ask(query):
    tokenizer = AutoTokenizer.from_pretrained("THUDM/chatglm2-6b-int4", trust_remote_code=True)
    # model = AutoModel.from_pretrained("THUDM/chatglm2-6b-int4", trust_remote_code=True, device='cpu')
    model = AutoModel.from_pretrained("THUDM/chatglm2-6b-int4", trust_remote_code=True, device='cpu').float()
    model = model.eval()
    print("运行中...")
    response, history = model.chat(tokenizer, query, history=[])
    return response
