import json
import os

from log.log import Log


class PublicInfo:
    # 这俩暂时不知道有啥用
    task_type: str
    task_type_int: int

    #
    def __init__(self, path):
        self.get_word_list_result = {}
        self.path = path
        # 检查并创建配置文件
        self.check_and_create_config()
        with open(os.path.join(self.path, "config", "config.json"), 'r', encoding='utf-8') as f:
            # user config
            user_config = json.load(f)
            self._min_time = user_config['min_time']
            self._max_time = user_config['max_time']
            self._spend_min_time = user_config['spend_min_time']
            self._spend_max_time = user_config['spend_max_time']
            self._api_choices = user_config['api_choices']
            self._proxy_url = user_config['proxy_url']
            self._openai_key = user_config['openai_key']
            self._model = user_config['model']
            self._model_ollama = user_config['model_ollama']
            self._token = user_config['token']
        # 任务列表
        self.task_list = ""
        # query_answer
        self._topic_code = ''
        self.word_query_result = ''
        self.word_means = ''
        self.exam = ''
        # all word
        self.word_list = []
        # translate
        self.zh_en = ''
        # all unit info
        self.all_unit = []
        self.not_complete_unit = {}
        self.task_id = ''
        self.now_unit = ''
        self.course_id = ''
        # class task
        self.class_task = []
        # 任务类型选择（默认1）
        self._task_choices = 1
        # unit task amount
        self.task_total_count = ''
        self.now_page = ''
        self.release_id = ''
        # self_built
        self.get_book_words_data = []
        self.is_self_built = False  # bool
        self.all_unit_name = []
        self.source_option = []
        pub_info = Log("public_info")
        pub_info.logger.info("公共组件初始化成功")

    @property
    # only read
    def topic_code(self):
        return self._topic_code

    @topic_code.setter
    # only write
    def topic_code(self, value):
        self._topic_code = value

    @topic_code.deleter
    # only del
    def topic_code(self):
        del self._topic_code

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        # 更新配置文件
        self.update_config_file()

    @property
    def task_type_choices(self):
        return self._task_choices

    @property
    def min_time(self) -> int:
        return self._min_time

    @property
    def max_time(self) -> int:
        return self._max_time

    @property
    def spend_min_time(self) -> int:
        return self._spend_min_time

    @property
    def spend_max_time(self) -> int:
        return self._spend_max_time

    @property
    def api_choices(self) -> int:
        return self._api_choices

    @property
    def proxy_url(self) -> str:
        return self._proxy_url

    @property
    def openai_key(self) -> str:
        return self._openai_key

    @property
    def model(self) -> str:
        return self._model

    @property
    def model_ollama(self) -> str:
        return self._model_ollama


    def check_and_create_config(self):
        """检查配置文件是否存在，不存在则创建默认配置文件；如果存在但缺少字段，则添加默认值"""
        config_dir = os.path.join(self.path, "config")
        config_file = os.path.join(config_dir, "config.json")

        # 定义默认配置
        default_config = {
            "min_time": 1,
            "max_time": 2,
            "spend_min_time": 1,
            "spend_max_time": 5,
            "api_choices": 1,
            "proxy_url": "https://xxxx.xxx/v1/chat/completions",
            "openai_key": "sk-xxxxxx",
            "model": "gpt-4o",
            "model_ollama": None,
            "token": ""
        }

        # 检查配置目录是否存在，不存在则创建
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        # 检查配置文件是否存在
        if not os.path.exists(config_file):
            # 配置文件不存在，创建默认配置
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)

            log = Log("public_info")
            log.logger.info("配置文件不存在，已创建默认配置文件")
        else:
            # 配置文件存在，检查是否缺少字段
            try:
                with open(config_file, 'r', encoding='utf-8') as f:
                    current_config = json.load(f)

                # 检查是否有字段缺失
                updated = False
                for key, value in default_config.items():
                    if key not in current_config:
                        current_config[key] = value
                        updated = True

                # 如果有字段缺失，更新配置文件
                if updated:
                    with open(config_file, 'w', encoding='utf-8') as f:
                        json.dump(current_config, f, indent=2, ensure_ascii=False)

                    log = Log("public_info")
                    log.logger.info("配置文件缺少字段，已添加默认值")
            except Exception as e:
                # 如果读取配置文件出错，创建新的默认配置
                with open(config_file, 'w', encoding='utf-8') as f:
                    json.dump(default_config, f, indent=2, ensure_ascii=False)

                log = Log("public_info")
                log.logger.error(f"读取配置文件出错: {str(e)}，已重新创建默认配置文件")


    def input_info(self, min_time, max_time, min_time_2, max_time_2, choices_api, proxy_url=None, openai_key=None, model=None , model_ollama=None , token=None):
        self._min_time = min_time
        self._max_time = max_time
        self._spend_min_time = min_time_2
        self._spend_max_time = max_time_2
        self._api_choices = choices_api

        # Update the new parameters if provided
        if proxy_url is not None:
            self._proxy_url = proxy_url
        if openai_key is not None:
            self._openai_key = openai_key
        if model is not None:
            self._model = model
        if model_ollama is not None:
            self._model_ollama = model_ollama
        if token is not None:
            self._token = token

        with open(os.path.join(self.path, "config", "config.json"), 'r', encoding="utf-8") as f:
            data = json.load(f)
            data['min_time'] = self._min_time
            data['max_time'] = self._max_time
            data['spend_min_time'] = self._spend_min_time
            data['spend_max_time'] = self._spend_max_time
            data['api_choices'] = self._api_choices
            data['proxy_url'] = self._proxy_url
            data['openai_key'] = self._openai_key
            data['model'] = self._model
            data['model_ollama'] = self._model_ollama
            data['token'] = self._token
        data_str = json.dumps(data, indent=2)
        with open(os.path.join(self.path, "config", "config.json"), 'w', encoding="utf-8") as f:
            f.write(data_str)

    def update_config_file(self):
        """更新配置文件"""
        config_file_path = os.path.join(self.path, "config", "config.json")
        with open(config_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['token'] = self._token  # 更新 token 字段
        with open(config_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)