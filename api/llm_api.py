import requests as rq
import logging
import re
import json

# Configure logger
logger = logging.getLogger(__name__)

def get_ollama_models():
    """
    获取Ollama上所有可用的模型列表

    :return: 可用模型列表，如果请求失败则返回空列表
    """
    try:
        response = rq.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        models_data = response.json()
        # 从返回数据中提取模型名称
        models = [model["name"] for model in models_data.get("models", [])]
        return models
    except Exception as e:
        logger.error(f"获取Ollama模型失败: {str(e)}")
        return []

def select_best_model(preferred_model=None):
    """
    选择最适合的Ollama模型

    :param preferred_model: 用户首选的模型名称
    :return: 选择的模型名称，如果没有可用模型则返回None
    """
    available_models = get_ollama_models()

    if not available_models:
        logger.info("没有发现可用的Ollama模型")
        return None

    print(available_models)

    # 如果用户指定了模型且该模型可用，直接返回
    if preferred_model and preferred_model in available_models:
        logger.info(f"使用指定模型: {preferred_model}")
        return preferred_model

    # 扩展的模型优先级，按类别和能力组织
    model_families = {
        "优先级高": ["claude", "gpt4", "phi3", "phi4", "gemma2", "llama3", "mistral-large", "mixtral-8x22b"],
        "优先级中": ["gemma", "phi2", "mixtral", "mistral", "llama2", "qwen"],
        "优先级低": ["vicuna", "orca", "neural-chat", "stable-beluga"]
    }

    # 按优先级选择模型
    for priority, models in model_families.items():
        for model_base in models:
            matching_models = [m for m in available_models if model_base.lower() in m.lower()]
            if matching_models:
                # 优先选择更大/更新的版本（通常名称更长）
                matching_models.sort(key=len, reverse=True)
                logger.info(f"自动选择模型: {matching_models[0]}")
                return matching_models[0]

    # 如果没有匹配到已知模型，返回第一个可用模型
    logger.info(f"使用默认可用模型: {available_models[0]}")
    return available_models[0]

def call_ollama(prompt: str, model: str = None) -> str:
    """
    调用本地Ollama模型获取回复

    :param prompt: 提示词
    :param model: 要使用的模型名称，如果为None则自动选择
    :return: 模型的回复文本，失败时返回None
    """
    # 如果没有指定模型，自动选择最佳模型
    if model is None:
        model = select_best_model()
        if model is None:
            return None  # 没有可用模型

    try:
        logger.info(f"正在使用Ollama模型: {model}")
        response = rq.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=10
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response", "").strip()
    except Exception as e:
        logger.error(f"Ollama调用失败: {str(e)}")
        return None

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


def clean_llm_result(result: str, mode: str = "word") -> str:
    """
    根据不同模式清理LLM返回的结果

    :param result: LLM返回的原始结果
    :param mode: 清理模式，可以是"word"(单词清理)、"number"(提取数字)或"raw"(原始结果)
    :return: 根据指定模式清理后的结果
    """
    if not result:
        return ""

    if mode == "raw":
        return result.strip()

    elif mode == "number":
        # 提取数字，适用于选项索引等场景
        match = re.search(r'\d+', result)
        if match:
            return match.group()  # 返回匹配到的第一个数字
        return ""

    elif mode == "word":
        # 移除常见的回答格式词组
        patterns_to_remove = [
            r"^原形[是为为:：]?\s*",
            r"^lemma[是为:：]?\s*",
            r"^the lemma is\s*",
            r"^[原基]词[是为:：]?\s*",
            r"^不定式[是为:：]?\s*",
            r"^answer[是为:：]?\s*",
            r"^word[是为:：]?\s*",
            r"^\"|\"$",  # 移除引号
            r"^\s*'|'\s*$"  # 移除单引号
        ]

        clean_result = result.strip().lower()
        for pattern in patterns_to_remove:
            clean_result = re.sub(pattern, '', clean_result, flags=re.IGNORECASE)

        # 如果包含"/"或"-"，取前面部分（常见于模型给出"lemma/原单词"格式）
        if "/" in clean_result:
            clean_result = clean_result.split("/")[0].strip()
        if "-" in clean_result:
            clean_result = clean_result.split("-")[0].strip()

        # 如果返回多个单词，只取第一个（更严格处理空格分隔）
        clean_result = re.split(r'[\s,，.。:：]', clean_result)[0]

        # 移除所有非单词字符
        clean_result = re.sub(r'[^\w]', '', clean_result)

        return clean_result

    else:
        logger.warning(f"未知的清理模式: {mode}，返回原始结果")
        return result.strip()

def get_llm_suggestion(prompt, public_info=None, ollama_model=None, mode="word" , llm_type_advance=""):
    """
    综合LLM接口，优先使用本地Ollama模型，失败后尝试ChatGPT API

    :param prompt: 提示文本
    :param public_info: 包含API配置信息的对象，如果为None则只尝试Ollama
    :param ollama_model: 指定使用的Ollama模型名称，None表示自动选择
    :param mode: 结果清理模式，可以是"word"(单词清理)、"number"(提取数字)或"raw"(原始结果)
    :return: LLM返回的处理结果，清理后的文本，失败则返回None
    """
    # 1. 首先尝试使用本地Ollama模型
    ollama_result = call_ollama(prompt, ollama_model)
    logger.info(f"\nprompt: '{prompt}'\n")
    if ollama_result:
        clean_result = clean_llm_result(ollama_result, mode)
        logger.info(f"\nOllama原始结果: '{ollama_result}'")
        logger.info(f"Ollama清理结果({mode}模式): '{clean_result}'")

    # 2. 如果Ollama失败且提供了public_info，尝试调用ChatGPT
    if public_info:
        try:
            result = get_chatgpt_suggestion(prompt, public_info)
            logger.info(f"\nprompt: '{prompt}'\n")
            if result:
                clean_result = clean_llm_result(result, mode)
                logger.info(f"\nChatGPT原始结果: '{result}'")
                logger.info(f"ChatGPT清理结果({mode}模式): '{clean_result}'")
                return clean_result
        except Exception as e:
            logger.error(f"ChatGPT处理失败: {str(e)}")

    # 如果所有方法都失败
    logger.warning("所有LLM接口调用失败")
    return None


