import httpx
import pandas as pd

# 设置显示所有列
pd.set_option('display.max_columns', None)
# 设置显示宽度为较大的值，避免换行
pd.set_option('display.width', 1000)
# 设置每列内容完全显示，不截断
pd.set_option('display.max_colwidth', None)


class APIShare:
    BASE_URL = "https://data.apishare.cn/api"  # 类级常量，API 基础地址
    HEADERS = {  # 类级常量，HTTP 请求头
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    def __init__(self, token):
        """
        初始化 ApiShare
        :param token: 认证Token
        """
        self._base_url = self.BASE_URL
        self._token = token
        self._headers = self.HEADERS

    def _make_request(self, method, payload):
        """
        通用请求方法
        :param method: HTTP 请求方法（仅支持 POST）
        :param payload: 请求的 JSON 数据
        :return: 返回的 JSON 数据或错误信息
        """
        try:
            response = httpx.request(method, self._base_url, json=payload, headers=self._headers)
            response.raise_for_status()  # 自动抛出非 2xx 状态码的异常
            return response.json()
        except httpx.RequestError as e:
            return {"error": f"Request error: {e}"}
        except httpx.HTTPStatusError as e:
            return {"error": f"HTTP error: {e.response.status_code}"}

    @staticmethod
    def _convert_to_dataframe(response):
        """
        将响应结果转换为 DataFrame
        :param response: 请求返回的 JSON 数据
        :return: DataFrame 或错误信息
        """
        if isinstance(response, dict) and "data" in response:
            try:
                return pd.DataFrame(response["data"])
            except Exception as e:
                return {"error": f"Failed to convert to DataFrame: {e}"}
        return response

    def get_data(self, api_name, as_dataframe=True, **params):
        """
        通用数据获取方法
        :param api_name: API名称
        :param as_dataframe: 是否将结果转换为 DataFrame，默认True
        :param params: 请求参数
        :return: 返回的 JSON 或 DataFrame
        """
        payload = {"token": self._token, "api_name": api_name, "params": params}
        response = self._make_request("POST", payload)

        # 返回 DataFrame 或原始 JSON
        return self._convert_to_dataframe(response) if as_dataframe else response


# # 示例用法
# if __name__ == "__main__":
#     # 初始化客户端，仅需设置一次 Token
#     api_client = APIShare(token="ccdd55e4-e5bb-4eac-967b-1b706df31525")
#
#     # 获取每日数据接口，默认返回 DataFrame
#     result_df = api_client.get_data(api_name="daily", code="000001.SZ", start_date="20240101", end_date="20241231")
#     print(result_df)
#
#     # 获取每日数据接口，返回原始 JSON
#     # result_json = api_client.get_data(api_name="daily", code="000001.SZ", as_dataframe=False)
#     # print("JSON Result:")
#     # print(result_json)