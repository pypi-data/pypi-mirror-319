from nonebot import get_plugin_config, on_message
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, MessageSegment
import httpx
import jwt
from datetime import datetime, timedelta
import time
from .config import Config
import base64
import random
from nonebot.plugin import PluginMetadata


__plugin_meta__ = PluginMetadata(
    name="玉！",
    description="基于 LLM 的玉检测插件",
    usage="none",
    type="application",
    homepage="https://github.com/XTxiaoting14332/nonebot-plugin-llm-jade",
    config=Config,
    supported_adapters={"~onebot.v11"},

)

config = get_plugin_config(Config)
def generate_token(apikey: str):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("错误的apikey！", e)

    payload = {
        "api_key": id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )
token = config.jadefoot_token

#生成JWT
def generate_token(apikey: str):
    try:
        id, secret = apikey.split(".")
    except Exception as e:
        raise Exception("错误的apikey！", e)

    payload = {
        "api_key": id,
        "exp": datetime.utcnow() + timedelta(days=1),
        "timestamp": int(round(time.time() * 1000)),
    }

    return jwt.encode(
        payload,
        secret,
        algorithm="HS256",
        headers={"alg": "HS256", "sign_type": "SIGN"},
    )


jade = on_message(priority=1, block=False)

@jade.handle()
async def handle(bot: Bot, event: GroupMessageEvent):
    for i in event.message:
        if i.type == "image":
            if random.randint(0, 1) < config.jadefoot_probability:
                img_url = i.data["url"]
                logger.info(img_url)
                auth = generate_token(token)
                res = await req_glm(auth, img_url)
                #  判断回复是否为true
                if (res == "true" or res == "True"):
                    await jade.finish("玉！", reply_message=True)
                else:
                    await jade.finish()








#异步请求AI
async def req_glm(auth_token, img_url):
    img_base = await url_to_base64(img_url)
    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    data = {
            "model": "glm-4v-flash",
            "temperature": 0.3,
            "messages": [{
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": "判断图片中是否出现了人类的脚，（包括裸足，穿袜，穿鞋等），如果是请仅回复“true”，如果不是请仅回复“false”"
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": img_base
                  }
                }
              ]
            }]
        }

    async with httpx.AsyncClient(timeout=httpx.Timeout(connect=10, read=20, write=20, pool=30)) as client:
        res = await client.post("https://open.bigmodel.cn/api/paas/v4/chat/completions", headers=headers, json=data)
        res = res.json()
    try:
        res_raw = res['choices'][0]['message']['content']
    except Exception as e:
        res_raw = res
    return res_raw


#url转base64
async def url_to_base64(url):
    async with httpx.AsyncClient(verify=False) as client:
        response = await client.get(url)
        if response.status_code == 200:
            image_data = response.content
            base64_encoded = base64.b64encode(image_data).decode('utf-8')
            return base64_encoded
        else:
            raise Exception("无法下载图片，状态码：", response.status_code)