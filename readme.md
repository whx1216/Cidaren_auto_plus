# 词达人自动刷题脚本

## 声明

本项目初始源码来源自:
- [github123666/cidaren](https://github.com/github123666/cidaren)
- [ularch/Cidaren_Automatic_Answer](https://github.com/ularch/Cidaren_Automatic_Answer)

**遵循MIT协议，仅供学习参考。**

### **若有侵权问题请联系 whx1216i@gmail.com**

## 主要改进

相较于 [ularch](https://github.com/ularch/Cidaren_Automatic_Answer/commits?author=ularch) 版本，主要改进：

1. **直接获取Token**: 现在可以在主程序中抓包获取token
2. **自动保存Token**: token会自动保存，无需手动操作
3. **智能匹配优化**: 使用ChatGPT替换了部分逻辑，提高了正确率
   - 解决了如音译汉字答案中 [n.测试，考试]、[n.考试，测试] 和 [n.(xx情况下)测试，考试] 等不能正常匹配的问题
   - 解决了填词题中提供前三个字母和词长度匹配到多个结果时选择错误的情况

## 系统要求

- Python 3.10+ 环境
- 网络连接（用于API调用）

## 安装步骤

1. 克隆或下载本仓库到本地
2. 在config文件中配置以下参数：

- `proxy_url`: 代理URL
- `openai_key`: OpenAI API密钥

## 使用方法

1. 点击 "点我运行.bat" 启动软件
2. 在软件界面中勾选 "启用Token监控"
3. 通过微信登录词达人界面
4. 程序获取到token后将自动登录并开始完成任务

## 注意事项

- 本项目使用ChatGPT进行匹配优化，如需使用本地LLM模型可自行修改相关代码
- 使用本软件可能违反词达人平台用户协议，请自行承担风险
- 建议仅用于学习和研究用途

## 问题反馈

如遇到问题，请在GitHub仓库提交Issue
