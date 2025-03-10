# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv() 

# client = OpenAI(
#     # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
#     api_key=os.getenv("ALIBABA_APIKEY"), 
#     base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
# )
# completion = client.chat.completions.create(
#     model="qwen-plus", # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
#     messages=[
#         {'role': 'system', 'content': 'You are a helpful assistant.'},
#         {'role': 'user', 'content': '你是谁？'}],
#     )
    
# print(completion.model_dump_json())



# # Please install OpenAI SDK first: `pip3 install openai`

# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("DEEPSEEK_APIKEY"), base_url="https://api.deepseek.com")

# response = client.chat.completions.create(
#     model="deepseek-chat",
#     messages=[
#         {"role": "system", "content": "You are a helpful assistant"},
#         {"role": "user", "content": "Hello"},
#     ],
#     stream=False
# )

# print(response.choices[0].message.content)


from openai import OpenAI
import os
from dotenv import load_dotenv
from custommodel.models import Message

model_dict={'0':'ALIBABA','1':'DEEPSEEK'

}

urls_dict={
    '0':"https://dashscope.aliyuncs.com/compatible-mode/v1",
    '1':"https://api.deepseek.com"

}
load_dotenv()

def llm_invoke(modeltype,modelname,usermsg):
    '''
        modeltype: 0/1/2...,
        modelname: model='deepseek-chat' model='deepseek-reasoner' 与官网modelname一致
    '''
    try:
        client=OpenAI(api_key=os.getenv(model_dict.get(modeltype)+'_APIKEY'),base_url=urls_dict.get(modeltype))

        response = client.chat.completions.create(
            model=modelname,
            messages=usermsg,
            # messages=[
            #     {"role": "system", "content": "You are a helpful assistant"},
            #     {"role": "user", "content": usermsg},
            # ],
            stream=False
        )
        
        # print(response.choices[0].message.content)
        return response.choices[0].message.content
    except:
        return '服务器无响应，请稍后再试！'
    
import requests
import sys

def stream_llm_response(modeltype,modelname,usermsg):
    try:
        client=OpenAI(api_key=os.getenv(model_dict.get(modeltype)+'_APIKEY'),base_url=urls_dict.get(modeltype))
        response = client.chat.completions.create(
            model=modelname,
            # prompt='who are you?',
            max_tokens=500,
            messages=usermsg,
            stream=True
        )
        for chunk in response:
            # if "choices" in chunk:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content)
                yield chunk.choices[0].delta.content
                # sys.stdout.flush()  # 刷新缓冲区
        # yield ""
        # for chunk in response.iter_content(chunk_size=None):
        #     if chunk:
        #         res=chunk.decode("utf-8")
        #         yield res
    except Exception as e:
        return '服务器无响应，请稍后再试！'


def stream_llm_response_record(modeltype,modelname,usermsg,uuid):
    try:
        client=OpenAI(api_key=os.getenv(model_dict.get(modeltype)+'_APIKEY'),base_url=urls_dict.get(modeltype))
        response = client.chat.completions.create(
            model=modelname,
            # prompt='who are you?',
            max_tokens=200,
            messages=usermsg,
            stream=True
        )
        complete_output = ""
        for chunk in response: 
            # if "choices" in chunk:
            if chunk.choices[0].delta.content:
                complete_output+=chunk.choices[0].delta.content
                # print(chunk.choices[0].delta.content)
                yield chunk.choices[0].delta.content
        
        mes = Message.objects.filter(message_id=uuid,content='').first()
        mes.content = complete_output 
        mes.save()

    except Exception as e:
        return '服务器无响应，请稍后再试！'

    # # 调用LLM服务（以OpenAI API为例）
    # api_url =urls_dict.get(modeltype)
    # headers = {
    #     "Authorization": os.getenv(model_dict.get(modeltype)+'_APIKEY'),
    #     "Content-Type": "application/json",
    # }
    # data = {
    #     "model":modelname,  # 或其他模型
    #     "prompt": prompt,
    #     "max_tokens": 100,
    #     "stream": True,  # 启用流式返回
    # }

    # # 发送请求并流式读取响应
    # response = requests.post(api_url, headers=headers, json=data, stream=True)



if __name__=='__main__':
    msg=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": 'who are you?'},
            ]
    llm_invoke('0','qwen-plus',msg)