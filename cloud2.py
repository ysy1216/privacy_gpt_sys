#cloud2 腾讯云
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tbp.v20190627 import tbp_client, models

def cloud_model2(user_input):
    try:
        # 实例化一个认证对象，入参需要传入腾讯云账户 SecretId 和 SecretKey，此处还需注意密钥对的保密
        # 代码泄露可能会导致 SecretId 和 SecretKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考，建议采用更安全的方式来使用密钥，请参见：https://cloud.tencent.com/document/product/1278/85305
        # 密钥可前往官网控制台 https://console.cloud.tencent.com/cam/capi 进行获取
        SecretId = "AKIDBEGG7vaFyunddZMxW8asw492iCk8nUbh"
        SecretKey = "8472Km4CQURA4saGnAICtRvQm9SYYNzL"
        cred = credential.Credential(SecretId, SecretKey)
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "tbp.ap-guangzhou.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = tbp_client.TbpClient(cred, "", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.TextProcessRequest()
        params = {
            "BotId": "58d826e3-73af-4ddb-887d-350475e88a9a",
            "BotEnv": "release",
            "TerminalId": "user1",
            "SessionAttributes": "True",
            "InputText": user_input,
            "PlatformType": "True",
            "PlatformId": "True"
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个TextProcessResponse的实例，与请求对象对应
        resp = client.TextProcess(req)
        # 输出ResponseText里面的内容
        response_text = json.loads(resp.to_json_string())["ResponseText"]
        return response_text

    except TencentCloudSDKException as err:
        return err