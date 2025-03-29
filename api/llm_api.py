import requests as rq
import logging

# Configure logger
logger = logging.getLogger(__name__)

def get_chatgpt_suggestion(prompt, public_info):
    '''
    通过第三方代理调用 ChatGPT API 获取建议。
    从 public_info 中获取 proxy_url 和 openai_key。

    :param prompt: 发送给 ChatGPT 的提示文本
    :param public_info: 包含配置信息的对象
    :return: ChatGPT 返回的建议或 None（如果调用失败）
    '''
    try:
        # 获取 proxy_url 和 openai_key
        proxy_url = public_info.proxy_url
        openai_key = public_info.openai_key
        model = public_info.model

        if not proxy_url or not openai_key:
            raise ValueError("配置文件中缺少 proxy_url 或 openai_key")

        # 设置请求头和请求体
        headers = {
            "Authorization": openai_key,
            "Content-Type": "application/json"
        }
        data = {
            "model": model,  # 使用的模型
            "messages": [
                {"role": "system", "content": "你是一个内置的语言助手api，按照要求输出内容。"},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 500
        }

        # 发送 POST 请求
        response = rq.post(proxy_url, headers=headers, json=data)
        response.raise_for_status()  # 检查请求是否成功
        result = response.json()

        # 解析返回的结果
        return result['choices'][0]['message']['content'].strip()
    except Exception as e:
        logger.error(f"调用第三方代理 API 失败: {e}")
        return None