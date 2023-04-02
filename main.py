from wxauto import *
import requests
import time

def chat(prompt,name):
    # wx.SendMsg("进入OpenAI主程序，正在请求OpenAI接口respond")
    data = {
        "messages": prompt,
        "model":"gpt-3.5-turbo",
        "max_tokens": 3000,
        "temperature": 0.5,
        "top_p": 1,
        "n": 1
    }
    response = requests.post(ENDPOINT, headers=headers, json=data)

    response_text = response.json()['choices'][0]['message']['content']
    return response_text

if __name__=='__main__':
    OPENAI_API_KEY = ""    #此处填写你的OpenAI API Key
    ENDPOINT = "https://api.openai.com/v1/chat/completions"  
    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    who = 'ChatGPT测试' #此处填写你的ChatGPT Robot所在群聊名称
    nickname='@Robot'  # 此处填写你的ChatGPT Robot的微信名，需要识别出是在和ChatGPT对话即可
    MDannotation = '@md'    #用于识别输出为md格式
    isMD = False

    wx=WeChat()
    wx.ChatWith(who)
    messages=[{"role": "system", "content": "你是一个有用的助手"}]
    num = 1
    while True:
        if len(messages) > 10:
            messages=[{"role": "system", "content": "你是一个有用的助手"}]
            num = 1
        msgobject1 = wx.GetLastMessage
        speaker1, msgcontent1, speakerid1= msgobject1
        time.sleep(1)
        msgobject2=wx.GetLastMessage
        speaker2, msgcontent2, speakerid2 = msgobject2
        if msgcontent1 != msgcontent2 and (nickname in msgcontent2):
            msgcontent2=msgcontent2.replace(nickname,'')

            #判断是否需要转为Markdown格式
            if MDannotation in msgcontent2:
                msgcontent2=msgcontent2.replace(MDannotation,'')
                isMD = True
            else:
                isMD = False
    
            #wx.SendMsg("Reply the Question："+msgcontent2)
            messages.append({"role": "user", "content":msgcontent2})
            ret = chat(messages,speaker2)
            print(num)

            #转换为Markdown格式
            if isMD:
                strnum=str(num)
                filename=strnum+".md"
                f = open(filename, "w",encoding='utf-8') 
                f.write(ret)
                f.close()
                filedir="C:\\Example"+filename  #此处填写main.py所在的路径
                # print(filedir)
                wx.SendFiles(filedir)
                ret=speaker2+"，结果已经转为Markdown文件发送给你了"
            WxUtils.SetClipboard(ret)
            wx.SendClipboard()
            num=num+1