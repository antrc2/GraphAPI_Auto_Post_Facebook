import requests
from openai import OpenAI
import pandas as pd
import time
import datetime

BASE_URL = "http://26.203.51.178:5555/v1"
API_KEY = "YOUR API KEY"
PAGE_ACCESS_TOKEN = "ACCESS_TOKEN"
PAGE_ID="PAGE_ID"
MODEL_NAME = "qwen2.5-1.5b-instruct"
EXCEL_PATH = "Aleotron.xlsx"
client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)



def getListPromptFromExcelPath(excel_path):
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
        prompts = df['prompt'].tolist()
    except:
        print("Không tìm thấy cột 'prompt'")
        prompts = []
    return prompts

def getFirstPromptFromExcelPath(excel_path):
    try:
        df = pd.read_excel(excel_path, engine='openpyxl')
        prompts = df['prompt'].tolist()

        if len(prompts) > 0:
            first_prompt = prompts[0]
            # Xóa dòng đầu tiên
            df = df.iloc[1:].reset_index(drop=True)

            # (Tuỳ chọn) Cập nhật file Excel nếu muốn:
            df.to_excel(excel_path, index=False)

            return first_prompt, df  # trả về cả prompt đầu tiên và phần còn lại nếu cần
        else:
            return "", df
    except:
        print("Không tìm thấy cột 'prompt' hoặc lỗi đọc file")
        return "", pd.DataFrame()
def postToFacebook(message):
    response = requests.post(f"https://graph.facebook.com/v22.0/{PAGE_ID}/feed",json={
        "message": message,
        "published": True,
        "access_token": PAGE_ACCESS_TOKEN
    })

    if (response.status_code == 200):
        return True
    else:
        return False
def chat_with_gemini(messages):
    response = client.chat.completions.create(
        messages=messages,
        temperature=0.7,
        stream=False,
        max_tokens=8196,
        model=MODEL_NAME
    )
    return response.choices[0].message.content

while True:
    now = datetime.datetime.now()
    # hour = now.hour
    minute = now.minute
    # minute = 0
    if minute == 0:
        prompt, df = getFirstPromptFromExcelPath(EXCEL_PATH)
        firstTask =  prompt
        if (firstTask):
            messages = [
                {
                    "role": "system",
                    "content": "Bạn là một trợ lí ảo của Nguyễn Ngọc An. Tên của bạn là Aleotron. Trong đó Aleotron: A: là AnTrc2, Leo: là linh vật sư tử. Tron: Mang nghĩa người máy"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            message = chat_with_gemini(messages)
            postToFacebook(message)
            print(f"Đăng bài về '{prompt}' thành công")
            time.sleep(61)
            
        else :
            pass
        

