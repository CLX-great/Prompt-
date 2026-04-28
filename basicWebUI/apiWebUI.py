import gradio as gr
import requests
import json

BACKEND_URL = "http://localhost:8005/v1/chat/completions"
HEADERS = {"Content-Type": "application/json"}


def chat_with_bot(message, history):
    data = {
        "messages": [
            {"role": "user", "content": message}
        ],
        "stream": False
    }

    try:
        response = requests.post(
            BACKEND_URL,
            headers=HEADERS,
            data=json.dumps(data),
            timeout=60
        )

        print("状态码:", response.status_code)
        print("原始返回:", response.text)

        res_json = response.json()

        if "choices" in res_json:
            bot_reply = res_json["choices"][0]["message"]["content"]
        else:
            bot_reply = f"后端返回异常：{res_json}"

    except Exception as e:
        bot_reply = f"请求失败：{e}"

    return bot_reply


demo = gr.ChatInterface(
    fn=chat_with_bot,
    title="智能流量套餐推荐系统",
    description="请输入你的套餐需求，例如：有没有土豪套餐 / 有没有流量大的套餐 / 200元以下有什么套餐",
    textbox=gr.Textbox(
        placeholder="请输入你的问题...",
        scale=7
    )
)


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860
    )