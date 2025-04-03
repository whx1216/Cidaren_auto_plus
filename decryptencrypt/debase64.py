import base64
import binascii
import json
import re


def debase64(data: dict or str):
    """
    base64解码和通用JSON解析
    :param data: 包含base64编码数据的字典或字符串
    :return: 解析后的JSON对象，失败时返回空字典
    """
    if isinstance(data, dict):
        data = data.get("data", "")

    try:
        bs64_str = base64.b64decode(data.encode("utf-8")).decode("utf-8", errors='ignore')
    except binascii.Error as e:
        # 英译汉 插入乱码处理
        char_list = list(data)
        indices_to_remove = [0, 1, 2, 4, 5, 36, 47, 48, 59, 96, 107]
        for index in sorted(indices_to_remove, reverse=True):
            if 0 <= index < len(char_list):
                del char_list[index]
        new_data = ''.join(char_list)
        try:
            bs64_str = base64.b64decode(new_data.encode("utf-8")).decode("utf-8", errors='ignore')
        except:
            print("Base64解码彻底失败")
            return

            # 查找所有可能的JSON对象起点
    json_starts = [i for i, char in enumerate(bs64_str) if char == '{']

    for start_pos in json_starts:
        # 使用括号平衡技术查找完整的JSON对象
        braces = 0
        in_string = False
        escape_next = False
        valid_json = None

        for i, char in enumerate(bs64_str[start_pos:]):
            if escape_next:
                escape_next = False
                continue

            if char == '"' and not escape_next:
                in_string = not in_string
            elif char == '\\' and in_string:
                escape_next = True
            elif not in_string:
                if char == '{':
                    braces += 1
                elif char == '}':
                    braces -= 1
                    if braces == 0:  # 找到了平衡的JSON对象
                        valid_json = bs64_str[start_pos:start_pos+i+1]
                        break

        if valid_json:
            try:
                # 尝试解析找到的JSON对象
                return json.loads(valid_json)
            except json.JSONDecodeError:
                # 如果解析失败，尝试下一个起点
                continue

    # 所有JSON起点都尝试失败，记录错误
    print(f"JSON解析失败，尝试所有可能的起点后仍未找到有效的JSON对象")
    print(f"解析失败的内容字符: \n\n\n 开始| \n\n{bs64_str}\n\n|结束 \n\n\n")

    # 最后尝试替换常见的非法字符并重新解析
    try:
        # 移除不可打印字符，保留基本ASCII和空白符
        clean_str = ''.join(c if (32 <= ord(c) <= 126) or c.isspace() else ' ' for c in bs64_str)
        # 查找第一个 { 和最后一个 }
        first_brace = clean_str.find('{')
        last_brace = clean_str.rfind('}')
        if first_brace >= 0 and last_brace > first_brace:
            potential_json = clean_str[first_brace:last_brace+1]
            return json.loads(potential_json)
    except:
        pass

    # 所有尝试都失败后返回空字典
    return {}


if __name__ == '__main__':
    print(debase64(
        "IUnsaHMPi61aUocCrfw16gE7IiRezjE9eyJ0YXNrX2lkIjo5ODM4ODc1OSwidGFza190eXBlIjoyLCJ0b3BpY19tb2RlIjoxNywic3RlbSI6eyJjb250ZW50IjoidmVyYiAg5byV6LW377yb5Lqn55SfIiwicmVtYXJrIjpudWxsLCJwaF91c191cmwiOm51bGwsInBoX2VuX3VybCI6bnVsbCwiYXVfYWRkciI6bnVsbH0sIm9wdGlvbnMiOlt7ImNvbnRlbnQiOiJjb25zaXN0IiwicmVtYXJrIjpudWxsLCJhbnN3ZXIiOm51bGwsImFuc3dlcl90YWciOjAsImNoZWNrX2NvZGUiOm51bGwsInN1Yl9vcHRpb25zIjpudWxsLCJwaF9pbmZvIjpudWxsfSx7ImNvbnRlbnQiOiJnZW5lcmF0ZSIsInJlbWFyayI6bnVsbCwiYW5zd2VyIjpudWxsLCJhbnN3ZXJfdGFnIjoxLCJjaGVja19jb2RlIjpudWxsLCJzdWJfb3B0aW9ucyI6bnVsbCwicGhfaW5mbyI6bnVsbH0seyJjb250ZW50IjoiaW5xdWlyZSIsInJlbWFyayI6bnVsbCwiYW5zd2VyIjpudWxsLCJhbnN3ZXJfdGFnIjoyLCJjaGVja19jb2RlIjpudWxsLCJzdWJfb3B0aW9ucyI6bnVsbCwicGhfaW5mbyI6bnVsbH0seyJjb250ZW50IjoibG9jYXRlIiwicmVtYXJrIjpudWxsLCJhbnN3ZXIiOm51bGwsImFuc3dlcl90YWciOjMsImNoZWNrX2NvZGUiOm51bGwsInN1Yl9vcHRpb25zIjpudWxsLCJwaF9pbmZvIjpudWxsfV0sInNvdW5kX21hcmsiOiIiLCJwaF9lbiI6IiIsInBoX3VzIjoiIiwiYW5zd2VyX251bSI6MSwiY2hhbmNlX251bSI6MSwidG9waWNfZG9uZV9udW0iOjUsInRvcGljX3RvdGFsIjo0NCwid19sZW5zIjpbXSwid19sZW4iOjAsIndfdGlwIjoiIiwidGlwcyI6IiIsIndvcmRfdHlwZSI6MSwiZW5hYmxlX2kiOjIsImVuYWJsZV9pX2kiOjIsImVuYWJsZV9pX28iOjIsInRvcGljX2NvZGUiOiJrMU9EZkpWblY0NkRmbnJFWjVWb2wyaGJYbHJKbmFXYnFwZXRtMWVSbFcxZ2twbHZZSktUbFYyVWoySm1ZWk9OWldlV1oyWnBiR2xyWW1pWmEyT1JsV0p1WW1tWmtHNWxtcFZ2YVd5T2FsMXlhbWx0YlptV2JWeVdhVzVwYW10eFltK09hbWx0YUd4dmFtR1Z3UT09IiwiYW5zd2VyX3N0YXRlIjoxfQ=="))