import time
import asyncio
import requests
from functools import wraps

class CiliciliConfig:
    FASTAPI_URL = "https://cilicili.club:12358/api/v1"

def Cilicili_AI(GPU_use=0, GPU_num=0, task_amount=0):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not args or not hasattr(args[0], "query_params") or 'session_id' not in dict(args[0].query_params):
                raise ValueError("URL参数出现问题，请重试这个操作")
            session_id = dict(args[0].query_params)['session_id']
            token_response = requests.post(
                f"{CiliciliConfig.FASTAPI_URL}/get_session",
                json={"session_id": session_id, "task_amount": task_amount}
            ).json()
            if not token_response.get('token'):
                raise Exception("该用户余额不足，请续费后再试")
            task_id = f"task-{int(time.time() * 1000)}"
            task = {
                "task_id": task_id,
                "gpu_use": GPU_use,
                "gpu_num": GPU_num
            }
            response = requests.post(f"{CiliciliConfig.FASTAPI_URL}/redis/add_task", json=task)
            if response.status_code != 200:
                raise Exception("任务推送失败，请稍后重试")
            print(f"任务 {task_id} 已成功提交到队列，等待分配GPU执行...")
            start_time = time.time()
            while True:
                notify_response = requests.get(f"{CiliciliConfig.FASTAPI_URL}/redis/check_notify/{task_id}")
                if notify_response.status_code == 200 and notify_response.json().get("ready"):
                    print(f"任务 {task_id} 已准备好，开始执行...")
                    break
                if time.time() - start_time > 3600:
                    raise TimeoutError("任务超时，请稍后重试")
                await asyncio.sleep(1)
            result = func(*args, **kwargs)
            print(result)
            return result
        return wrapper
    return decorator
