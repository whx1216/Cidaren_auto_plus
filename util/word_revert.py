from api.llm_api import get_llm_suggestion
from publicInfo.publicInfo import PublicInfo
from get_path import get_application_path
from api.basic_api import use_api_get_prototype
import logging

# Configure logger
logger = logging.getLogger(__name__)

def word_revert(word: str, public_info=None) -> str:
    """
    使用LLM将单词还原为原形

    :param word: 需要还原的单词
    :param public_info: 包含API配置信息的对象，如果为None则只尝试Ollama
    :param ollama_model: 指定使用的Ollama模型名称
    :return: 单词的原形
    """
    # 优化后的提示词，更明确要求只返回一个单词
    prompt = (
        f"任务：将单词还原为原形(lemma)。\n\n"
        f"规则：\n"
        f"1. 只返回一个单词作为结果\n"
        f"2. 不要包含任何解释或标点\n"
        f"3. 不要重复原始单词\n"
        f"4. 不要包含'原形是'或类似的短语\n\n"
        f"示例：\n"
        f"- 输入：'used'，输出：'use'\n"
        f"- 输入：'running'，输出：'run'\n"
        f"- 输入：'better'，输出：'good'\n\n"
        f"现在请处理以下单词：{word}\n\n"
        f"返回格式：仅返回一个单词，没有其他内容。"
    )

    # 使用统一的LLM接口，指定为单词处理模式
    result = get_llm_suggestion(prompt, public_info, mode="word")
    if result:
        logger.info(f"LLM处理结果: '{result}' (原单词: '{word}')")
        return result

    # 2. 如果LLM接口都失败，尝试使用备用API方法
    try:
        logger.info(f"使用备用API方法处理单词: '{word}'")
        api_result = use_api_get_prototype(word)

        # 验证API返回的结果是否有效
        if api_result and isinstance(api_result, str):
            logger.info(f"API结果: '{api_result}' (原单词: '{word}')")
            return api_result
    except Exception as e:
        logger.error(f"备用API处理失败: {str(e)}")

    # 最终备用方案：如果所有API都失败，返回原单词
    logger.warning(f"所有方法都失败，返回原单词: '{word}'")
    return word

if __name__ == '__main__':
    # 需要创建一个包含API配置信息的对象
    path = get_application_path()
    public_info = PublicInfo(path)
    print(word_revert('installed', public_info))
