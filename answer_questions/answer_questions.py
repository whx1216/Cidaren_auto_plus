import random
import re
import time
import requests as rq
from api.main_api import query_word, submit_result, next_exam
from log.log import Log
from publicInfo.publicInfo import PublicInfo
from util.basic_util import delete_other_char
from util.select_mean import select_mean, handle_query_word_mean, filler_option, select_match_word, word_examples, \
    is_word_exist
from util.word_revert import word_revert
from view.error import showError
import json

query_answer = Log('query_answer')


# submit
def submit(public_info: PublicInfo, option: int or str or dict):
    """
    提交答案
    :param public_info:
    :param option: 选项索引或单词
    :return: None
    """
    public_info.topic_code = public_info.exam['topic_code']
    # submit result
    if type(option) == dict:
        # resolve mode == 31
        for answer_index in option.values():
            submit_result(public_info, answer_index)
    else:
        submit_result(public_info, option)
    #
    time.sleep(random.randint(1, 2))
    # get next exam
    next_exam(public_info)


# skip read word
def jump_read(public_info):
    time.sleep(random.randint(1, 3))
    query_answer.logger.info("跳过阅读单词卡片")
    next_exam(public_info)
    public_info.topic_code = public_info.exam['topic_code']


# mean form word
def select_word(public_info) -> int or str or None:
    word_mean = public_info.exam['stem']['remark']
    query_answer.logger.info("汉译英:" + word_mean)
    # option word
    options = filler_option(public_info)
    for option in options:
        # word is exist word_list
        if is_word_exist(public_info, option):
            # two response types
            if public_info.word_query_result.get('means'):
                query_result = public_info.word_query_result['means']
                for means in query_result:
                    for usage in means['usages']:
                        phrases_infos = usage['phrases_infos']
                        if phrases_infos:
                            for phrases_info in phrases_infos:
                                # match same mean
                                if phrases_info['sen_mean_cn'] == word_mean:
                                    return delete_other_char(phrases_info['sen_content'])

            else:
                query_result = public_info.word_query_result['options']
                for content in query_result:
                    for usage_info in content['content']['usage_infos']:
                        if usage_info['sen_mean_cn'] == word_mean:
                            return delete_other_char(usage_info['sen_content'])
    query_answer.logger.info("查询失败,准备跳过")
    return None


def word_form_mean(public_info: PublicInfo) -> int:
    """
    英译汉
    :param public_info:
    :return:
    """
    query_answer.logger.info("英译汉")
    # is listen
    exam = public_info.exam['stem']['content'].replace(' ', "")
    # 题干格式xxx{word}xxx
    query_answer.logger.info(f"从{exam}提取单词")
    word = re.findall("{(.*?)}", exam)
    query_answer.logger.info(f"提取到{word}")
    word = word[0] if word else exam
    # 判断单词是否在单词列表中
    if word not in public_info.word_list:
        if word.endswith("ed") and word[:-2] in public_info.word_list:
            word = word[:-2]
        elif word.endswith("ing") and word[:-3] in public_info.word_list:
            word = word[:-3]
        else:
            query_answer.logger.info(f"将{word}转原型")
            # 单词转原型
            word = word_revert(word)
    # 请求单词释义
    query_word(public_info, word)
    # 提取释义
    handle_query_word_mean(public_info)
    query_answer.logger.info('选择意思')
    # 选择正确释义
    return select_mean(public_info)


# mean to word
def mean_to_word(public_info):
    # mode 17
    word_mean = public_info.exam['stem']['content']
    # match answer
    return select_match_word(public_info, word_mean)


# select together word
def together_word(public_info) -> dict:
    query_answer.logger.info("意思相似单词")
    # exam options
    options = filler_option(public_info)
    # answer
    result_word = {word['relation']: options.index(word['relation']) for word in public_info.exam['stem']['remark']}
    query_answer.logger.info(f"选项{options}")
    query_answer.logger.info(f"答案{result_word}")
    return result_word


# complete a sentence
def full_sentence(public_info) -> int or str:
    query_answer.logger.info("选择最合适的单词完成句子")
    options = filler_option(public_info)
    # word in examples sentence
    word = word_examples(public_info, options)
    # extract answer tag
    for option in public_info.exam['options']:
        # match answer
        option_word = option['answer_tag']
        if type(option_word) == str:
            if option['sub_options']:
                for sub_option in option['sub_options']:
                    if sub_option['content'] == word:
                        return option_word + str(sub_option['answer_tag'])
            # no need to  match  tenses
            if option['content'] == word:
                return option_word + '0'
        else:
            if option['content'] == word:
                return option_word
    query_answer.logger.info("补全句子失败,猜第3个选项")
    # submit 1#0,0#2 or 1 应该分开写提升正确率
    return public_info.exam['options'][2]['answer_tag']


# full word
# def complete_sentence(public_info):
#     '''
#     {'task_id': 120381820, 'task_type': 1, 'topic_mode': 51, 'stem': {'content': '{}  to  norms', 'remark': '遵守规范', 'ph_us_url': None, 'ph_en_url': None, 'au_addr': None}, 'options': [], 'sound_mark': '', 'ph_en': '', 'ph_us': '', 'answer_num': 1, 'chance_num': 1, 'topic_done_num': 93, 'topic_total': 98, 'w_lens': [7], 'w_len': 7, 'w_tip': 'con', 'tips': '', 'word_type': 1, 'enable_i': 2, 'enable_i_i': 2, 'enable_i_o': 2, 'topic_code': 'lFh3eYdsktiTVlyHeHuLbJevZJeTa1liWpmopJvU1qNWjZhqYHCYb2xgj1WbotDHo6LSV5Njk5VlY2STZGhtbGdrbG6cmWxqk5xlj5SOcmlgbWtkbJiVaGOdaGJoZGlrYmuaaW9oaGJqbmWelG9mkpZlZm6YcWxnaV9okA==', 'answer_state': 1, 'show_card_type': 1}
# <class 'dict'>
#     :param public_info:
#     :return:
#     '''
#     query_answer.logger.info("补全单词")
#     word_len = public_info.exam['w_lens'][0]
#     # submit not  case sensitive
#     word_start_with = public_info.exam['w_tip'].lower()
#     # iterate over all word in the unit
#     for word in public_info.word_list:
#         if word.startswith(word_start_with):
#             query_answer.logger.info(public_info)
#             print(public_info.exam)
#             print(type(public_info.exam))
#             query_answer.logger.info(f'word_start_with：{word_start_with,word.startswith(word_start_with)}')
#             if len(word) == word_len:
#                 return word
#             elif len(word) + 1 == word_len:
#                 return word + 's'
#             else:
#                 result = word_examples(public_info, [word])
#                 if result:
#                     return result
#     query_answer.logger.info(f"找不到答案,提交{word}")
#     return word
#
#
# import requests  # 用于发送 HTTP 请求

def complete_sentence(public_info):
    '''
    根据 public_info 中的信息补全句子，结合第三方代理调用 ChatGPT API 进行语义匹配。

    :param public_info: 包含任务信息的字典，包括单词长度、起始字母、remark、content 和单词列表。
    :return: 最合适的单词。
    '''
    query_answer.logger.info("补全单词")

    # 提取任务信息
    word_len = public_info.exam['w_lens'][0]  # 目标单词长度
    word_start_with = public_info.exam['w_tip'].lower()  # 目标单词起始字母（小写）
    remark = public_info.exam['stem']['remark']  # 任务备注（例如“遵守规范”）
    content = public_info.exam['stem']['content']  # 句子模板（例如“{} to norms”）
    word_list = public_info.word_list  # 候选单词列表

    # 筛选出符合起始字母和长度的单词
    candidate_words = [
        word for word in word_list
        if word.startswith(word_start_with) and len(word) <= word_len + 2
    ]

    # 如果没有候选单词，直接返回最后一个单词
    if not candidate_words:
        query_answer.logger.info("没有符合条件的候选单词")
        return word_list[-1] if word_list else ""

    # 调用第三方代理的 ChatGPT API
    def get_chatgpt_suggestion(prompt,public_info):
        '''
        通过第三方代理调用 ChatGPT API 获取建议。
        '''
        try:
            # 获取 proxy_url 和 openai_key
            proxy_url = public_info.proxy_url
            openai_key = public_info.openai_key
            model = public_info.model

            if not proxy_url or not openai_key:
                raise ValueError("配置文件中缺少 proxy_url 或 openai_key")

            # 第三方代理 API 的 URL 和参数
            headers = {
                "Authorization": openai_key,
                "Content-Type": "application/json"
            }
            data = {
                "model": model,  # 使用的模型
                "messages": [
                    {"role": "system", "content": "你是一个语言助手，帮助用户选择最合适的单词。"},
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
            query_answer.logger.error(f"调用第三方代理 API 失败: {e}")
            return None

    # 构建 ChatGPT 的提示词
    prompt = (
        f"通过中文提示补全句子，请根据以下信息选择一个最合适的单词：\n"
        f"- 句子模板: '{content}'\n"
        f"- 中文意思: '{remark}'\n"
        f"- 候选单词: {', '.join(candidate_words)}\n"
        f"重要！请直接返回最合适的单词或选择的单词的形态变体，不要添加其他内容。输出内容应当只有一个单词。"
    )
    # print(prompt)
    # 获取 ChatGPT 的建议
    suggested_word = get_chatgpt_suggestion(prompt,public_info).strip("'").strip('"')
    # print(suggested_word)
    # 如果 ChatGPT 返回了建议，优先使用
    if suggested_word and suggested_word in candidate_words:
        query_answer.logger.info(f"ChatGPT 推荐单词: {suggested_word}")
        return suggested_word

    # 如果 ChatGPT 没有返回有效建议，返回第一个符合条件的候选单词
    query_answer.logger.info("ChatGPT 未返回有效建议，返回第一个候选单词")
    return candidate_words[0]

def answer(public_info, mode):
    if mode == 11:
        option = word_form_mean(public_info)
    elif mode == 13:
        # guess option 没思路
        option = 3
    elif mode == 15 or mode == 16 or mode == 21 or mode == 22:
        option = word_form_mean(public_info)
        # 英译汉
    elif mode == 17 or mode == 18:
        option = mean_to_word(public_info)
    elif mode == 31:
        option = together_word(public_info)
    elif mode == 32:
        option = select_word(public_info)
        query_answer.logger.info(f'翻译结果{option}')
    elif mode == 41 or mode == 42 or mode == 43 or mode == 44:
        option = full_sentence(public_info)
        query_answer.logger.info(f'提交选项{option}')
    # mode == 43  "content":"Reading  is  of  {}  importance  in  language  learning.","remark":"阅读在语言学习中至关重要。" 选时态
    elif mode == 51 or mode == 52 or mode == 53 or mode == 54:
        option = complete_sentence(public_info)
        query_answer.logger.info(f'补全单词结果{option}')
    else:
        option = 0
        query_answer.logger.info(public_info.exam)
        query_answer.logger.info("其他题型,程序退出")
        showError()
        exit(-1)
    return option


