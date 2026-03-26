"""
个人中心API封装
"""
import allure
from typing import Dict, Any
from utils.request_utils import request


class ProfileAPI:
    """个人中心接口"""

    @staticmethod
    @allure.step("获取个人信息")
    def get_profile():
        """获取当前用户个人信息"""
        return request.get("/system/user/profile")

    @staticmethod
    @allure.step("修改个人信息")
    def update_profile(profile_data: Dict[str, Any]):
        """
        修改当前用户个人信息

        Args:
            profile_data: 用户信息字典(nickName, email, phonenumber, sex等)
        """
        return request.put("/system/user/profile", json_data=profile_data)

    @staticmethod
    @allure.step("修改密码")
    def update_password(old_password: str, new_password: str):
        """
        修改当前用户密码

        Args:
            old_password: 旧密码
            new_password: 新密码
        """
        data = {
            "oldPassword": old_password,
            "newPassword": new_password
        }
        return request.put("/system/user/profile/updatePwd", json_data=data)


# 全局个人中心API实例
profile_api = ProfileAPI()
