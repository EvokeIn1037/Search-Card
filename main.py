from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
import astrbot.api.message_components as Comp

import requests
import urllib.parse

url = "https://ygocdb.com/api/v0/?search="

card_dict = {
    "红爹": "超魔导龙骑士-真红眼龙骑兵",
    "凤爹": "命运英雄 毁灭凤凰人",
    "虹爹": "虹光新宇侠",
    "魔术爹": "娱乐伙伴 灵摆魔术家",
    "白爹": "究极龙魔导师",
    "人渣": "欧尼斯特",
    "吃货": "教导的圣女 艾克莉西娅",
    "轮胎龙": "嵌合要塞龙",
    "飞天轮胎龙": "嵌合巨舰龙",
    "海龟": "海龟坏兽 加美西耶勒",
    "大宝贝": "熔岩魔神·岩浆魔像",
    "蛋": "拉之翼神龙-球体形",
    "蟑螂": "增殖的Z",
    "师匠": "黑魔术师",
    "高达": "神灭兵器－天霆号 扼宙斯",
    "书呆": "阴沉书呆魔术师",
    "陨石": "原始生命态 尼比鲁",
    "星遗孀": "领取星杯的巫女",
    "抗战": "铁兽的抗战",
    "姬哥": "铁兽战线 姬特",
    "鲜花": "鲜花之女男爵",
    "牢爪": "邪心英雄 堕恶爪魔",
    "问心无愧": "恐龙摔跤手·潘克拉辛角龙",
    "陀螺": "疾行机人 贝陀螺集合体",
    "除圣": "俱舍怒威族·阿莱斯哈特",
    "红高达": "俱舍怒威族·阿莱斯哈特",
    "博士": "秘旋谍-天才",
    "小蓝": "龙女仆·清扫龙女",
    "老艾": "被封印的艾克佐迪亚",
    "斧王": "巨斧袭击者",
    "奥特曼": "元素英雄 新宇侠",
    "大炮": "魔炮战机 达磨羯磨",
    "达磨炮": "魔炮战机 达磨羯磨",
    "寝姬": "梦见之妮穆蕾莉娅",
}

@register("card", "Evoke", "一个简单的 游戏王查卡 插件", "1.0.0")
class MyPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""
    
    # 注册指令的装饰器。指令名为 helloworld。注册成功后，发送 `/helloworld` 就会触发这个指令，并回复 `你好, {user_name}!`
    @filter.command("查卡")
    async def helloworld(self, event: AstrMessageEvent):
        """这是一个 hello world 指令""" # 这是 handler 的描述，将会被解析方便用户了解插件内容。建议填写。
        user_name = event.get_sender_name()
        message_str = event.message_str # 用户发的纯文本消息字符串
        message_chain = event.get_messages() # 用户所发的消息的消息链 # from astrbot.api.message_components import *
        logger.info(message_chain)

        search_str = message_str[3:]
        if search_str in card_dict:
            search_str = card_dict[search_str]

        msg_str = urllib.parse.quote(search_str)

        response = requests.get(url + msg_str)

        if response.status_code == 200:
            data = response.json().get("result", [])
            if len(data) == 0:
                yield event.plain_result("没有搜到这张卡捏~")
            elif len(data) > 1:
                sc_names = [card.get("sc_name", "") if card.get("sc_name") else card.get("nwbbs_n", "") for card in data]
                joined_names = ', '.join(sc_names)
                yield event.plain_result("这是搜到的所有卡片：" + joined_names)
            else:
                card = data[0]
                card_pic = "https://cdn.233.momobako.com/ygopro/pics/" + str(card.get("id")) + ".jpg"
                sc_name = card.get("sc_name")
                nwbbs_n = card.get("nwbbs_n")
                jp_name = card.get("jp_name")
                en_name = card.get("en_name")
                types = card.get("text", {}).get("types")
                pdesc = card.get("text", {}).get("pdesc")
                if len(pdesc) == 0:
                    pdesc = "无"
                desc = card.get("text", {}).get("desc")
                card_text = "简中卡名：" + sc_name + '\n' + "NWBBS卡名：" + nwbbs_n + '\n' + "日文卡名：" + jp_name + '\n' + "英文卡名：" + en_name + '\n\n' + "卡片信息：" + types + '\n' + "灵摆刻度：" + pdesc + '\n' + "卡片文本：" + desc
                chain = [
                    # Comp.At(qq=event.get_sender_id()), # At 消息发送者
                    Comp.Image.fromURL(card_pic), # 从 URL 发送图片
                    Comp.Plain(card_text),
                ]
                yield event.chain_result(chain)
        else:
            # print("Failed to fetch data. Status code:", response.status_code)
            yield event.plain_result("查卡功能维护中~")

        # yield event.plain_result(f"Hello, {user_name}, 你发了 {msg_str}!") # 发送一条纯文本消息

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""
