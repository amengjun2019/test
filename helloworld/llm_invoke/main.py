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

if __name__=='__main__':
    msg=[
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "content": 'who are you?'},
            ]
    llm_invoke('0','qwen-plus',msg)