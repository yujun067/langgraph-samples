作业代码参照characterglm_api_demo_streamlit.py。

分为2个文件
1. novel_example.py
测试了调用chatglm,根据段落内容生成人物画像；
测试了调用characterglm, 根据人物描述做单轮对话。
2. novel_api_demo_streamlit.py
代表角色2输入一句启动的话，然后 用角色2的query和历史对话调用模型1生成角色1的回复；
互换user和assist的身份、互换对话历史标记，然后 用角色1的query和历史对话调用模型2生成角色2的回复；
目前默认进行5轮对话，到达6句就删除头两句以限制上下文的长度，然后写入对话历史到output.txt中。

