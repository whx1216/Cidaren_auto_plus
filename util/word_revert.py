from api.llm_api import get_chatgpt_suggestion
from publicInfo.publicInfo import PublicInfo
from get_path import get_application_path
from api.basic_api import use_api_get_prototype

def word_revert(word: str, public_info) -> str:
    """
    使用LLM将单词还原为原形

    :param word: 需要还原的单词
    :param public_info: 包含API配置信息的对象
    :return: 单词的原形
    """

    # 构建提示词
    prompt = (
        f"请将以下单词还原为其原形(lemma)或不定式形式。只返回原形单词，不要包含任何解释、标点或额外文本。\n"
        f"单词: {word}\n"
        f"例如：\n"
        f"- 如果输入是'used'，则返回'use'\n"
        f"- 如果输入是'running'，则返回'run'\n"
        f"- 如果输入是'better'，则返回'good'\n"
        f"- 如果输入已经是原形，则返回原单词\n"
        f"请只返回一个单词作为回答。"
    )

    # 调用LLM获取原形
    result = get_chatgpt_suggestion(prompt, public_info)

    # 处理结果
    if result:
        # 清理可能的额外内容，只保留单词
        clean_result = result.strip().lower()
        # 如果返回多个单词，只取第一个
        if ' ' in clean_result:
            clean_result = clean_result.split()[0]
        # 移除可能的标点
        import re
        clean_result = re.sub(r'[^\w]', '', clean_result)

        print(f"{clean_result}  /  {word}")
        return clean_result

    # 如果LLM调用失败或结果无效，使用备用API方法
    try:
        print(f"使用备用API方法处理单词: {word}")
        api_result = use_api_get_prototype(word)

        # 验证API返回的结果是否有效
        if api_result and isinstance(api_result, str):
            print(f"API结果: {api_result}  /  原单词: {word}")
            return api_result
    except Exception as e:
        print(f"备用API处理失败: {str(e)}")

    # 最终备用方案：如果所有API都失败，返回原单词
    print(f"所有API方法失败，返回原单词: {word}")
    return word
# 使用示例
if __name__ == '__main__':
    # 需要创建一个包含API配置信息的对象
    path = get_application_path()
    public_info = PublicInfo(path)
    print(word_revert('installed', public_info))
