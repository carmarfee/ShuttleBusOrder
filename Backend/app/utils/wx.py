import requests

def get_access_token() -> dict:
    """
    获取微信小程序access_token
    
    :param appid: 小程序AppID
    :param secret: 小程序AppSecret
    :return: 返回结果字典
    """
    url = "https://api.weixin.qq.com/cgi-bin/token"
    
    params = {
        'grant_type': 'client_credential',
        'appid': 'wx0abbd02a012b378d',
        'secret': 'ec48fdac212b69463034a49f3dd1fe37'
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        result = response.json()
        
        # 检查是否有错误
        if 'errcode' in result and result['errcode'] != 0:
            return {
                'success': False,
                'errcode': result['errcode'],
                'errmsg': result['errmsg']
            }
        
        # 成功返回
        return {
            'success': True,
            'access_token': result['access_token'],
            'expires_in': result['expires_in']
        }
        
    except Exception as e:
        return {
            'success': False,
            'errcode': -1,
            'errmsg': str(e)
        }

# access_token = get_access_token().get('access_token')
# openid = '从你存储的用户信息中获取'
# template_id = d0CikXwRfK5apE3Yqo1wsiicNwW0mIodgyfXlZzF55M
# 例如data ={ "phrase3": { "value": "审核通过" }, "name1": { "value": "订阅" }, "date2": { "value": "2019-12-25 09:42" } } 
'''
订单编号 {{character_string1.DATA}}

订单状态 {{phrase5.DATA}}

下单人员 {{thing3.DATA}}

温馨提示 {{thing6.DATA}}
'''
def send_subscribe_message(access_token: str, openid: str, template_id: str, data: dict, page: str = None) -> dict:
    """
    发送微信小程序订阅消息
    
    :param access_token: 接口调用凭证
    :param openid: 接收者openid
    :param template_id: 模板ID
    :param data: 模板数据
    :param page: 点击消息跳转的小程序页面（可选）
    :return: 返回结果字典
    """
    url = f"https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={access_token}"
    
    payload = {
        "touser": openid,
        "template_id": template_id,
        "data": data
    }
    
    # 可选参数
    if page:
        payload["page"] = page
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        result = response.json()
        
        return {
            'success': result.get('errcode', -1) == 0,
            'errcode': result.get('errcode', -1),
            'errmsg': result.get('errmsg', '未知错误')
        }
        
    except Exception as e:
        return {
            'success': False,
            'errcode': -1,
            'errmsg': str(e)
        }