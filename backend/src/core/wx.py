import os
import time
import requests
from typing import Optional
import redis
from pydantic import BaseModel
from fastapi import HTTPException
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 微信接口URL
WECHAT_TOKEN_URL = "https://api.weixin.qq.com/cgi-bin/token"


class WechatTokenResponse(BaseModel):
    """微信返回的token结构"""
    access_token: str
    expires_in: int  # 有效期（秒），默认7200
    errcode: Optional[int] = None
    errmsg: Optional[str] = None


class AccessTokenManager:
    def __init__(self):
        # 初始化Redis连接
        self.redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            db=int(os.getenv("REDIS_DB")),
            password=os.getenv("REDIS_PASSWORD"),
            decode_responses=True  # 返回字符串而非bytes
        )
        self.cache_key = os.getenv("ACCESS_TOKEN_KEY")
        self.appid = os.getenv("WECHAT_APPID")
        self.appsecret = os.getenv("WECHAT_APPSECRET")

        # 校验必要配置
        if not all([self.appid, self.appsecret, self.cache_key]):
            raise ValueError("请配置完整的微信小程序信息和缓存键名")

    def _get_lock(self, lock_key: str, timeout: int = 10) -> bool:
        """获取分布式锁，防止并发获取token"""
        # NX: 只有key不存在时才设置成功，PX: 过期时间（毫秒）
        return self.redis_client.set(lock_key, "1", nx=True, px=timeout * 1000) is not None

    def _release_lock(self, lock_key: str):
        """释放分布式锁"""
        self.redis_client.delete(lock_key)

    def _fetch_from_wechat(self) -> str:
        """直接调用微信接口获取新的access_token"""
        params = {
            "grant_type": "client_credential",
            "appid": self.appid,
            "secret": self.appsecret
        }

        try:
            response = requests.get(WECHAT_TOKEN_URL, params=params, timeout=10)
            response.raise_for_status()  # 触发HTTP错误（如500）
            result = WechatTokenResponse(**response.json())

            if result.errcode != 0:
                raise HTTPException(
                    status_code=500,
                    detail=f"微信接口错误：{result.errcode} - {result.errmsg}"
                )
            return result.access_token, result.expires_in

        except requests.exceptions.RequestException as e:
            raise HTTPException(
                status_code=500,
                detail=f"请求微信接口失败：{str(e)}"
            )

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        获取有效的access_token（优先从缓存取，过期则刷新）
        :param force_refresh: 是否强制刷新（用于手动触发更新）
        """
        # 1. 强制刷新时，先删除缓存
        if force_refresh:
            self.redis_client.delete(self.cache_key)

        # 2. 尝试从缓存获取
        cached_token = self.redis_client.get(self.cache_key)
        if cached_token:
            return cached_token

        # 3. 缓存失效，获取分布式锁准备请求微信接口
        lock_key = f"{self.cache_key}_lock"
        try:
            # 尝试获取锁（最多等待3秒，防止死锁）
            for _ in range(3):
                if self._get_lock(lock_key):
                    # 4. 再次检查缓存（防止其他线程已更新）
                    cached_token = self.redis_client.get(self.cache_key)
                    if cached_token:
                        return cached_token

                    # 5. 调用微信接口获取新token
                    token, expires_in = self._fetch_from_wechat()

                    # 6. 缓存到Redis（提前200秒过期，避免临界点失效）
                    cache_seconds = max(10, expires_in - 200)  # 至少保留10秒
                    self.redis_client.setex(self.cache_key, cache_seconds, token)
                    return token
                else:
                    # 未获取到锁，等待1秒重试
                    time.sleep(1)

            # 7. 多次获取锁失败，抛出异常
            raise HTTPException(
                status_code=500,
                detail="获取access_token失败：并发锁竞争超时"
            )

        finally:
            # 释放锁（无论成功失败都要释放）
            self._release_lock(lock_key)

    def refresh_periodically(self):
        """定时刷新任务（可在后台线程中运行）"""
        while True:
            try:
                # 每1小时刷新一次（小于7200秒）
                time.sleep(3600)
                self.get_access_token(force_refresh=True)
                print("定时刷新access_token成功")
            except Exception as e:
                print(f"定时刷新access_token失败：{str(e)}")
                # 失败后重试间隔缩短为10分钟
                time.sleep(600)