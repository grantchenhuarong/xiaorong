#！/bin/bash
# 功能：
# 1、比较下不同的embedding方法，所产生出来的vector
# 2、比较下不同的embedding方法，余弦相似度计算的近似程度
# 3、范围： text2vec-large-chinese/moka-ai-m3e/Ali-Qwen-7B


from transformers import AutoTokenizer, AutoModel, AutoModelForCausalLM
import torch
import numpy as np

# 定义词嵌入模型的相关信息
embedding_models = {
    "text2vec": "/data/ftp/models/embeddings/text2vec-large-chinese",
    "m3e": "/data/ftp/models/embeddings/moka-ai/m3e-base",
    "Baichuan-13B-Chat": "/data/ftp/models/baichuan/13B-Chat",
    "ChatGLM2-6B": "/data/ftp/models/tsinghua/chatglm2/chatglm2-6b",
    "Ali-Qwen-7B": "/data/ftp/models/Ali/Qwen-7B",
}

#  定义比较相似度的语句对
similarity_sentences = [
    ("张三在讲话", "李四在发言"),
    ("请问你的手机号码？", "请问你的联系电话？"),
    ("这家商场的老板是罗丝。", "罗丝是这家商场的主人。"),
    ("Driven by an insatiable thirst for knowledge, she stayed late every night, her eyes dancing across the pages of books as if they were starry skies.",
     "Isn't it unusual, that she, prompted by an unquenchable intellectual curiosity, burns the midnight oil, pouring over pages as though navigating constellations?"),
]


def load_tokenizer(model_name, model_type):
    tokenizer = AutoTokenizer.from_pretrained(
        model_name,
        trust_remote_code=True,
        # llama不支持fast
        use_fast=False if model_type == 'llama' else True
    )
    # QWenTokenizer比较特殊，pad_token_id、bos_token_id、eos_token_id均为None。eod_id对应的token为<|endoftext|>
    if tokenizer.__class__.__name__ == 'QWenTokenizer':
        tokenizer.pad_token_id = tokenizer.eod_id
        tokenizer.bos_token_id = tokenizer.eod_id
        tokenizer.eos_token_id = tokenizer.eod_id

    return tokenizer


def embedding_text(text):
    input_ids = tokenizer(text, return_tensors="pt", add_special_tokens=False).input_ids
    return input_ids


# 加载模型和分词器
def get_model(model_name_or_path, device, model_type):
    model = None, None
    try:
        if model_type in ("text2vec", "m3e"):
            model = AutoModel.from_pretrained(model_name_or_path)
        else:
            model = AutoModelForCausalLM.from_pretrained(
                model_name_or_path,
                trust_remote_code=True,
                low_cpu_mem_usage=True,
                torch_dtype=torch.float16,
                device_map=device
            ).to(device).eval()
    except Exception as e:
        print("cal_similarity.get_model ===", str(e))
    finally:
        return model


# 定义计算相似度的函数
def calc_similarity_bert(model, tokenizer, s1, s2):
    # 对句子进行分词，并添加特殊标记
    input_ids = tokenizer([s1, s2], return_tensors='pt', padding=True, truncation=True, max_length=1024)
    # print(s1)

    # 将输入传递给BERT模型，并获取输出
    with torch.no_grad():
        outputs = model(**input_ids)
        embeddings = outputs.last_hidden_state[:, :, :].cpu().numpy()

    # 计算余弦相似度，并返回结果
    print(type(embeddings[0]))
    print(embeddings[0].shape)
    print(embeddings[0])

    sim = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
    return sim


# 定义计算相似度的函数
def calc_similarity_llm(model, tokenizer, s1, s2, model_type, device = 'cuda'):
    if model_type == 'ChatGLM2-6B':
        # s1 = '[Round 1]\n\n问：{}\n\n答：'.format(s1)
        # s2 = '[Round 1]\n\n问：{}\n\n答：'.format(s2)
        input_id1 = tokenizer(s1, return_tensors="pt", add_special_tokens=False).input_ids.to(device)
        input_id2 = tokenizer(s2, return_tensors="pt", add_special_tokens=False).input_ids.to(device)
        print(type(input_id1))
        print(input_id1.shape)
    else:
        input_id1 = tokenizer(s1, return_tensors="pt", add_special_tokens=False).input_ids.to(device)
        bos_token_id = torch.tensor([[tokenizer.bos_token_id]], dtype=torch.long).to(device)
        eos_token_id = torch.tensor([[tokenizer.eos_token_id]], dtype=torch.long).to(device)
        input_id1 = torch.concat([bos_token_id, input_id1, eos_token_id], dim=1)

        input_id2 = tokenizer(s2, return_tensors="pt", add_special_tokens=False).input_ids.to(device)
        bos_token_id = torch.tensor([[tokenizer.bos_token_id]], dtype=torch.long).to(device)
        eos_token_id = torch.tensor([[tokenizer.eos_token_id]], dtype=torch.long).to(device)
        input_id2 = torch.concat([bos_token_id, input_id2, eos_token_id], dim=1)

    embeddings = ()
    torch.cuda.empty_cache()
    with torch.no_grad():
        if model_type == 'ChatGLM2-6B':
            output1 = model.embedding(input_id1)
            print("input_id1-output1:", input_id1, "===", output1)
            output2 = model.embedding(input_id2)
            print("input_id2-output2:", input_id2, "===", output2)
        else:
            output1 = model.model.embed_tokens(input_id1)
            print("input_id1-output1:", input_id1, "===", output1)
            output2 = model.model.embed_tokens(input_id2)
            print("input_id2-output2:", input_id2, "===", output2)
        print(type(output1))
        print(output1.shape)
        embeddings = (output1[0, :, :].cpu().numpy(), output2[0, :, :].cpu().numpy())

    # 计算余弦相似度，并返回结果
    print(type(embeddings[0]))
    print(embeddings[0].shape)
    print(embeddings[0])

    # 计算余弦相似度，并返回结果
    sim = np.dot(embeddings[0], embeddings[1]) / (np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1]))
    return sim


if __name__ == "__main__":
    ## 循环处理每对比较的语句
    ## 利用GPU计算字符串嵌入编码的向量
    for model_type, embedding_model in embedding_models.items():
        print("embedding_model:==", model_type)
        ## 加载词表模型
        tokenizer = load_tokenizer(embedding_model, model_type)
        ## 加载模型
        model = get_model(embedding_model, "cuda", model_type)

        for text_pair in similarity_sentences:
            ## 计算字符串对的嵌入式编码
            s1, s2 = text_pair[0], text_pair[1]

            ## 计算其余弦相似度
            similarity_cos = 0.0
            if model_type in ("text2vec", "m3e"):
                similarity_cos = calc_similarity_bert(model, tokenizer, s1, s2)
            else:
                # input_ids1, input_ids2 = embedding_text(s1), embedding_text(s2)
                # print(input_ids1, "---", input_ids2)
                similarity_cos = calc_similarity_llm(model, tokenizer, s1, s2, model_type)
                pass
            print(s1,"--", s2, " 余弦相似度===", str(similarity_cos))
        print("\n")
