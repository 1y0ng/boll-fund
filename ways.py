from wechatpy import WeChatClient, WeChatClientException
from wechatpy.client.api import WeChatMessage
def read_f(file_name):
    list_id=[]
    for line in open(file_name,encoding='utf-8'):
        list_id.append(line.rstrip('\n'))
    return list_id
def send_msg(template_id,data):
    app_id='wx709f5f578b08d4d1'
    app_secret='7dd50a4ffaeb43fa18e4a616b540d4cb'
    user_id='ov4e45r9uuXF7Sq-T7DhXOz0W-uI'
    try:
        client = WeChatClient(app_id, app_secret)
    except WeChatClientException as e:
        print('微信获取 token 失败，请检查 APP_ID 和 APP_SECRET，或当日调用量是否已达到微信限制。')
        exit(502)

    wm = WeChatMessage(client)
    count = 0
    try:
        print('正在发送给 %s, 数据如下：%s' % (user_id, data))
        res = wm.send_template(user_id, template_id, data)
        count+=1
    except WeChatClientException as e:
        print('微信端返回错误：%s。错误代码：%d' % (e.errmsg, e.errcode))
        exit(502)