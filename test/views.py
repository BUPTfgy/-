from django.shortcuts import render
import erniebot
import json
from django.http import JsonResponse

def index(request):
    return render(request ,'main.html')

def detail(request):
    return render(request ,'detail.html')

def ask(request):
    question = request.GET.get('question','')

    import erniebot									#引入文心api包
    erniebot.api_type = 'aistudio'					#定义使用的令牌的aistudio平台的
    erniebot.access_token = "xxxxxxxxxxxxxxxxxxxxxxxx"			#引入自己的令牌:https://aistudio.baidu.com/usercenter/token
    model = 'ernie-3.5'								#定义使用的模型是ernie-3.5
    message_content ="The task scenario is: I need you to refine four computer configuration plans based on the requirements I provide for me to choose from. Each plan should include necessary content such as GPU, CPU, memory, hard disk, motherboard, total budget, etc."\
                     "The best way is to provide references under different budgets, and you need to stand from the perspective of a computer configuration expert to help me choose solutions that meet my needs and minimize expenses."\
                     "对每个方案进行介绍，让读者能够直观的知道该方案的特点 我提供的基本需求为：{question}}，注意要基于我提供的基本需求进行方案设计，注意给出方案的大致预算区间，尽量覆盖不同的价位区间"\
                     "示例json文件如下，参考它的格式:[{\"模块主题\":\"\",\"本模块内容简介\":\"\"},]"\
                     "Strictly follow the format I provided "\
                     "每个方案的简介在30个中文汉字左右,注意务必给出方案的大致预算区间(例如¥3000-¥5000)。"\
                     "The output is just pure JSON format, with no other descriptions."				   
                     #传给文心的文本
    messages = [									#将文本和其他参数封装成消息，便于传给文心
        {
            'role': 'user',
            'top_p': '0.001',
            'content': message_content				#传输的文本
        }
    ]
    response = erniebot.ChatCompletion.create(		# 调用文心一言回答问题，下方是相关参数
        model=model,
        messages=messages,
    )
    answer = response.result						#将回答的文本传给answer变量
    print(answer)									#输出查看
    
    #从文心一言的回复内容中拆分四个模块内容

    try:
        json_start = answer.find("[")
        json_end= answer.rfind("]")
        if json_start !=-1 and json_end != -1:
            json_content=answer[json_start:json_end+1]
            
            answer_dict= json.loads(json_content)
        else:
            answer_dict={}
    except json.JSONDecodeError:
        answer_dict ={}

    #获取各个模块的主题
    module_titles = []
    if answer_dict:  # 检查 answer_dict 是否为空
        for item in answer_dict:
            module_title = item.get("模块主题", "")
            module_discription = item.get("本模块内容简介", "")

            if module_title and module_discription:
                module_titles.append({"模块主题": module_title, "本模块内容简介": module_discription})
                print("模块主题:", module_title)  # 打印模块标题
                print("本模块内容简介:", module_discription)  # 打印模块内容简介
    #把获取的内容返回给前端
    return JsonResponse(module_titles,safe=False)


import json
from django.http import JsonResponse
import erniebot  # 引入文心api包

from django.http import JsonResponse
import json
import erniebot

def getdetail(request):
    detail_title = request.GET.get('detail_title', '')
    detail_content = request.GET.get('detail_content', '')

    erniebot.api_type = 'aistudio'
    erniebot.access_token = "217c58d769c1437832735929badb15664796f37b"
    model = 'ernie-3.5'
    
    message_content = (
        f"The task scenario is: I need you to refine four computer configuration plans based on the requirements I provide for me to choose from. Each plan should include necessary content such as GPU, CPU, memory, hard disk, motherboard, total budget, etc."
        "The best way is to provide references under different budgets, and you need to stand from the perspective of a computer configuration expert to help me choose solutions that meet my needs and minimize expenses."
        f"对方案进行详细设计，方案主题为：{detail_title}，注意要基于我提供的基本需求{detail_content}进行方案设计，注意特别关注方案的预算区间"
        "示例json文件如下，参考它的格式,注意各部分标题限定:[{\"方案主题\":\"\",\"CPU\":\"\"},\"主板\":\"\"},\"内存\":\"\"},\"存储设备\":\"\"},\"图形卡\":\"\"},\"电源供应器\":\"\"},\"机箱\":\"\"},\"散热器\":\"\"},\"风扇\":\"\"},\"显示器\":\"\"},\"键盘和鼠标\":\"\"},\"操作系统\":\"\"},]"
        "Strictly follow the format I provided.Each component should be described in a separate line of text."
        "CPU：价格符合预算的CPU"
        "主板：请选择符合方案主题需求,价格符合预算的主板"
        "内存：请选择符合方案主题需求,价格符合预算的内存"
        "存储设备：包括固态硬盘（SSD）或机械硬盘（HDD），请选择符合方案主题需求,价格符合预算的存储设备，如果没有说明，优先选择固态硬盘"
        "图形卡：可选,请选择符合方案主题需求,价格符合预算的GPU，如果预算不足，可以舍弃，但应当说明"
        "电源供应器：请选择符合方案主题需求,价格符合预算的电源。"
        "机箱：请选择符合方案主题需求,价格符合预算的机箱，注意符合说明的特殊需求，如ITS小机箱"
        "散热器：请选择符合方案主题需求,价格符合预算的散热器"
        "风扇：请选择符合方案主题需求,价格符合预算的风扇"
        "显示器：请选择符合方案主题需求,价格符合预算的显示器"
        "键盘和鼠标：默认不纳入方案中，除非特殊说明，请选择符合方案主题需求,价格符合预算的键盘鼠标"
        "操作系统：例如Windows、macOS或Linux，除非特别说明默认优先选用Windows系列,请选择符合方案主题需求,价格符合预算的操作系统"
        "注意以上配件的价格综合不能超过价格区间的上限,请选择符合方案主题需求,价格符合预算的所有配件"
        "The output is just pure JSON format, with no other descriptions,Please return only one JSON."
    )

    messages = [
        {
            'role': 'user',
            'top_p': '0.001',
            'content': message_content
        }
    ]

    response = erniebot.ChatCompletion.create(
        model=model,
        messages=messages,
    )

    answer = response.result

    print("ErnieBot Response:", answer)  # 打印从 ErnieBot 获取到的回答

    try:
        json_start = answer.find("[")
        json_end = answer.rfind("]")
        if json_start != -1 and json_end != -1:
            json_content = answer[json_start:json_end+1]
            answer_dict = json.loads(json_content)
        else:
            answer_dict = {}
    except json.JSONDecodeError:
        answer_dict = {}

    print("Parsed JSON Content:", answer_dict)  # 打印解析后的 JSON 内容

    module_titles = []
    if answer_dict:
        for item in answer_dict:
            module_title = item.get("方案主题", "")
            module_detail_1 = item.get("CPU", "")
            module_detail_2 = item.get("主板", "")
            module_detail_3 = item.get("内存", "")
            module_detail_4 = item.get("存储设备", "")
            module_detail_5 = item.get("图形卡", "")
            module_detail_6 = item.get("电源供应器", "")
            module_detail_7 = item.get("机箱", "")
            module_detail_8 = item.get("散热器", "")
            module_detail_9 = item.get("风扇", "")
            module_detail_10 = item.get("显示器", "")
            module_detail_11 = item.get("键盘和鼠标", "")
            module_detail_12 = item.get("操作系统", "")
            if module_title:
                module_titles.append({"方案主题": module_title, "CPU": module_detail_1, "主板": module_detail_2, "内存": module_detail_3, "存储设备": module_detail_4, "图形卡": module_detail_5, "电源供应器": module_detail_6, "机箱": module_detail_7, "散热器": module_detail_8, "风扇": module_detail_9, "显示器": module_detail_10, "键盘和鼠标": module_detail_11, "操作系统": module_detail_12,})

    print("Final Module Titles:", module_titles)  # 打印最终模块标题和内容

    return JsonResponse(module_titles, safe=False)