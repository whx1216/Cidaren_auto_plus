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

## 使用方法

#### 0.现在可以直接[下载](https://github.com/whx1216/Cidaren_auto_plus/releases/latest)打包好的可执行程序点击.exe直接运行
1. 点击 "点我运行.bat" 启动软件
2. 在设置-首选项-api设置中配置相关设置
模型可以二选一填写，都有填写优先使用ollama,chatgpt增加容错
3. 在软件界面中勾选 "启用Token监控"
4. 通过微信登录词达人界面 
5. 在程序获取到token后点击登录并开始完成任务

## 注意事项

- 使用本软件可能违反词达人平台用户协议，请自行承担风险
- 建议仅用于学习和研究用途

## 问题反馈

如遇到问题，请在GitHub仓库提交Issue
