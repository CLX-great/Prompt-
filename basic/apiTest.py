import requests
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

url = "http://localhost:8000/v1/chat/completions"

headers = {
    "Content-Type": "application/json"
}
# 非流式输出
stream_flag = False

#input_text = "有没有土豪套餐"
#input_text = "请给我推荐一个套餐"
#input_text = "我平时不怎么用流量，请给我推荐一个套餐"
input_text = "但我流量使用可能会比现在你推荐的高一点"
payload = {
    "messages": [{"role": "user", "content": input_text}],
    "stream": stream_flag,
    "userId": "123",
    "conversationId": "123"
}


def safe_parse_response(response):
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    try:
        result = response.json()
    except json.JSONDecodeError:
        print("返回内容不是合法 JSON")
        return None

    if response.status_code != 200:
        print("请求失败：", result)
        return None

    if "choices" not in result:
        print("返回结果中没有 choices：", result)
        return None

    try:
        return result["choices"][0]["message"]["content"]
    except (KeyError, IndexError, TypeError) as e:
        print("解析 choices 失败：", e)
        print("完整返回：", result)
        return None


if stream_flag:
    try:
        with requests.post(
            url,
            headers=headers,
            json=payload,
            stream=True,
            timeout=60
        ) as response:

            print("Status Code:", response.status_code)

            if response.status_code != 200:
                print("请求失败：", response.text)
            else:
                for line in response.iter_lines():
                    if not line:
                        continue

                    line_text = line.decode("utf-8").strip()

                    if line_text.startswith("data:"):
                        line_text = line_text[5:].strip()

                    if line_text == "[DONE]":
                        logger.info("流式输出结束")
                        break

                    try:
                        chunk = json.loads(line_text)
                    except json.JSONDecodeError:
                        print("无法解析的流式内容：", line_text)
                        continue

                    try:
                        choice = chunk["choices"][0]
                        finish_reason = choice.get("finish_reason")

                        if finish_reason == "stop":
                            logger.info("接收JSON数据结束")
                            break

                        delta = choice.get("delta", {})
                        content = delta.get("content")

                        if content:
                            print(content, end="", flush=True)

                    except (KeyError, IndexError, TypeError) as e:
                        print("流式数据结构异常：", e)
                        print("完整 chunk：", chunk)

    except requests.exceptions.RequestException as e:
        print("请求发生网络错误：", e)

else:
    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=60
        )

        content = safe_parse_response(response)

        if content:
            print(content)
            logger.info(f"非流式输出，响应内容是: {content}")

    except requests.exceptions.RequestException as e:
        print("请求发生网络错误：", e)