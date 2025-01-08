import httpx
import pandas as pd


class ApiShare:
    def __init__(self, token, base_url="https://data.apishare.cn/api", headers=None):
        """
        初始化 ApiShare
        :param token: 认证Token
        :param base_url: API的基础URL
        :param headers: 自定义请求头
        """
        self._base_url = base_url
        self._token = token
        self._headers = headers or {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    def _request(self, payload):
        """
        内部方法，用于发送 API 请求
        :param payload: 请求的 JSON 数据
        :return: 返回的JSON数据或错误信息
        """
        try:
            # 发送 POST 请求
            response = httpx.post(self._base_url, json=payload, headers=self._headers)
            # 检查 HTTP 状态码
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP error: {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def get_data(self, api_name, as_dataframe=True, **params):
        """
        通用数据获取方法
        :param api_name: API名称
        :param as_dataframe: 是否将结果转换为 DataFrame，默认True
        :param params: 可变参数字典
        :return: 返回的JSON数据或DataFrame或错误信息
        """
        payload = {
            "token": self._token,
            "api_name": api_name,
            "params": params,  # 动态传递参数
        }
        response = self._request(payload)

        # 检查是否需要返回 DataFrame
        if as_dataframe and isinstance(response, dict) and "data" in response:
            try:
                # 假设返回的数据格式为 {"data": [{"col1": val1, "col2": val2, ...}, ...]}
                return pd.DataFrame(response["data"])
            except Exception as e:
                return {"error": f"Failed to convert to DataFrame: {e}"}

        return response


# 示例用法
if __name__ == "__main__":
    # 初始化客户端，仅需设置一次 Token
    api_client = ApiShare(token="ccdd55e4-e5bb-4eac-967b-1b706df31525")

    # 获取每日数据接口
    result = api_client.get_data(api_name="daily", code="000001.SZ")
    print(result)