"""
feishu_lib — 飞书自建应用共享库（被所有 feishu-* skills 复用）。

设计目标：
- 统一凭证管理：~/.config/feishu/credentials.json（一次配置全 skill 共用）
- 统一 token 缓存：~/.cache/feishu/{tenant_token,user_token}.json
- 业务配置分离：~/.config/feishu/<skill>.json（每个 skill 自己一份）
- 通用工具：HTTP / multipart / OAuth / 认证请求 / 常用 API

两套 token：
- tenant_access_token: 应用身份。能力受限（飞书 2024+ 不允许应用作为 Wiki 协作者）
- user_access_token: 用户身份，通过 OAuth 拿。能访问该用户可见的全部 Wiki

依赖：仅 Python 3.8+ 标准库。
"""
import http.server
import json
import mimetypes
import os
import sys
import time
import uuid
import webbrowser
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlencode, urlparse
from urllib.request import Request, urlopen

API_BASE = "https://open.feishu.cn/open-apis"
CONFIG_DIR = Path.home() / ".config" / "feishu"
CACHE_DIR = Path.home() / ".cache" / "feishu"
CREDENTIALS_PATH = CONFIG_DIR / "credentials.json"
TOKEN_CACHE_PATH = CACHE_DIR / "token.json"           # tenant_access_token
USER_TOKEN_CACHE_PATH = CACHE_DIR / "user_token.json"  # user_access_token

# OAuth
OAUTH_REDIRECT_PORT = 8765
OAUTH_REDIRECT_URI = f"http://localhost:{OAUTH_REDIRECT_PORT}/callback"


class FeishuError(RuntimeError):
    """飞书 API 业务错误（msg 已用户友好化）。"""


# ---------- HTTP 基础 ----------

def http_request(url, method="GET", headers=None, data=None, timeout=30):
    """通用 HTTP 请求。data 是 dict → 自动 JSON；是 bytes → 原样发送。"""
    headers = dict(headers or {})
    if isinstance(data, dict):
        data = json.dumps(data, ensure_ascii=False).encode("utf-8")
        headers.setdefault("Content-Type", "application/json; charset=utf-8")
    req = Request(url, method=method, headers=headers, data=data)
    try:
        with urlopen(req, timeout=timeout) as r:
            body = r.read().decode("utf-8")
            return json.loads(body) if body else {}
    except HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {e.code}: {body}")


def build_multipart(fields, files):
    """构造 multipart/form-data。
    fields: dict[str, str]
    files: list[(name, filename, bytes, mime)]
    返回 (payload_bytes, boundary)
    """
    boundary = "feishu-skill-" + uuid.uuid4().hex
    parts = []
    for k, v in fields.items():
        parts.append(f"--{boundary}\r\n".encode())
        parts.append(f'Content-Disposition: form-data; name="{k}"\r\n\r\n'.encode())
        parts.append(f"{v}\r\n".encode())
    for name, filename, content, mime in files:
        parts.append(f"--{boundary}\r\n".encode())
        parts.append(
            f'Content-Disposition: form-data; name="{name}"; filename="{filename}"\r\n'.encode()
        )
        parts.append(f"Content-Type: {mime}\r\n\r\n".encode())
        parts.append(content)
        parts.append(b"\r\n")
    parts.append(f"--{boundary}--\r\n".encode())
    return b"".join(parts), boundary


# ---------- 凭证管理 ----------

def load_credentials():
    if not CREDENTIALS_PATH.exists():
        raise FeishuError(
            f"未找到飞书凭证 {CREDENTIALS_PATH}。\n"
            f"请按 SKILL.md 的「凭证 setup」流程创建自建应用，然后运行：\n"
            f"  python3 <skill_path>/push.py --init-credentials <app_id> <app_secret>"
        )
    return json.loads(CREDENTIALS_PATH.read_text())


def save_credentials(app_id, app_secret):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CREDENTIALS_PATH.write_text(
        json.dumps({"app_id": app_id, "app_secret": app_secret}, ensure_ascii=False, indent=2)
    )
    os.chmod(CREDENTIALS_PATH, 0o600)
    # 凭证变更后强制清掉 token 缓存
    if TOKEN_CACHE_PATH.exists():
        TOKEN_CACHE_PATH.unlink()


def credentials_exist():
    return CREDENTIALS_PATH.exists()


# ---------- 业务配置（每个 skill 一个 ----------

def load_business_config(name):
    """name: 'wiki' | 'bitable' | 'bot' | ..."""
    path = CONFIG_DIR / f"{name}.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def save_business_config(name, data):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    path = CONFIG_DIR / f"{name}.json"
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    os.chmod(path, 0o600)


def business_config_exists(name):
    return (CONFIG_DIR / f"{name}.json").exists()


# ---------- Token 缓存 ----------

def get_tenant_token(force_refresh=False):
    """带缓存的 tenant_access_token。距过期 60s 以内自动续。"""
    if not force_refresh and TOKEN_CACHE_PATH.exists():
        try:
            cache = json.loads(TOKEN_CACHE_PATH.read_text())
            if cache.get("expires_at", 0) > time.time() + 60:
                return cache["token"]
        except (json.JSONDecodeError, OSError):
            pass  # 缓存坏了就当没有
    creds = load_credentials()
    res = http_request(
        f"{API_BASE}/auth/v3/tenant_access_token/internal",
        method="POST",
        data={"app_id": creds["app_id"], "app_secret": creds["app_secret"]},
    )
    if res.get("code") != 0:
        raise FeishuError(
            f"获取 tenant_access_token 失败: code={res.get('code')} msg={res.get('msg')}"
        )
    token = res["tenant_access_token"]
    expire = res.get("expire", 7200)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    TOKEN_CACHE_PATH.write_text(
        json.dumps({"token": token, "expires_at": int(time.time()) + expire})
    )
    os.chmod(TOKEN_CACHE_PATH, 0o600)
    return token


def authed_request(url, method="GET", data=None, content_type=None):
    """带 tenant_access_token 的请求，token 过期自动重试一次。
    data: dict（自动 JSON）或 bytes（原样，需指定 content_type）
    """
    def _do(token):
        headers = {"Authorization": f"Bearer {token}"}
        if content_type:
            headers["Content-Type"] = content_type
        return http_request(url, method=method, headers=headers, data=data)

    token = get_tenant_token()
    try:
        return _do(token)
    except RuntimeError as e:
        # 99991661/99991663 = token 失效；401 = 未授权
        if "99991663" in str(e) or "99991661" in str(e) or "HTTP 401" in str(e):
            token = get_tenant_token(force_refresh=True)
            return _do(token)
        raise


# ---------- OAuth + user_access_token ----------

def save_user_token(token_data):
    """token_data 来自 /authen/v1/access_token 或 /authen/v1/refresh_access_token 的 data 字段。
    v1 字段名：access_token / refresh_token / expires_in / refresh_expires_in
    """
    now = int(time.time())
    data = {
        "access_token": token_data["access_token"],
        "refresh_token": token_data["refresh_token"],
        "expires_at": now + token_data["expires_in"],
        "refresh_expires_at": now + token_data.get("refresh_expires_in", 30 * 86400),
    }
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    USER_TOKEN_CACHE_PATH.write_text(json.dumps(data, indent=2))
    os.chmod(USER_TOKEN_CACHE_PATH, 0o600)


def _get_app_access_token():
    """获取 app_access_token（v1 OAuth 接口的 header 需要它，注意和 tenant_access_token 不同）。"""
    creds = load_credentials()
    res = http_request(
        f"{API_BASE}/auth/v3/app_access_token/internal",
        method="POST",
        data={"app_id": creds["app_id"], "app_secret": creds["app_secret"]},
    )
    if res.get("code") != 0:
        raise FeishuError(f"获取 app_access_token 失败: code={res.get('code')} msg={res.get('msg')}")
    return res["app_access_token"]


def _exchange_oauth_token(payload):
    """OAuth v1: 用 app_access_token 做 Bearer，响应包在 data 里，**默认带 refresh_token**。
    payload: {"grant_type": "authorization_code"|"refresh_token", "code"/"refresh_token": "..."}
    """
    app_token = _get_app_access_token()
    # 根据 grant_type 选 endpoint
    if payload.get("grant_type") == "authorization_code":
        endpoint = f"{API_BASE}/authen/v1/access_token"
    else:
        endpoint = f"{API_BASE}/authen/v1/refresh_access_token"
    res = http_request(
        endpoint,
        method="POST",
        headers={"Authorization": f"Bearer {app_token}"},
        data=payload,
    )
    if res.get("code") != 0:
        raise FeishuError(f"OAuth 换 token 失败: code={res.get('code')} msg={res.get('msg')}")
    return res["data"]


def oauth_login():
    """启动 OAuth 流程：起本地 HTTP server → 浏览器授权 → 收到 code → 换 token 存本地。"""
    creds = load_credentials()
    expected_state = uuid.uuid4().hex
    auth_url = (
        f"{API_BASE}/authen/v1/index?"
        + urlencode({
            "app_id": creds["app_id"],
            "redirect_uri": OAUTH_REDIRECT_URI,
            "state": expected_state,
        })
    )

    captured = {}

    class CallbackHandler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            params = parse_qs(urlparse(self.path).query)
            if "code" in params:
                captured["code"] = params["code"][0]
                captured["state"] = params.get("state", [None])[0]
                msg = "<h1>✅ 授权成功</h1><p>可以关闭此页面，回终端查看。</p>"
                self.send_response(200)
            else:
                msg = f"<h1>❌ 授权失败</h1><pre>{params}</pre>"
                self.send_response(400)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(msg.encode("utf-8"))

        def log_message(self, *args):
            pass  # 静默

    server = http.server.HTTPServer(("localhost", OAUTH_REDIRECT_PORT), CallbackHandler)
    print(f"→ 在浏览器中授权：\n  {auth_url}\n", file=sys.stderr)
    print(f"  等待回调（http://localhost:{OAUTH_REDIRECT_PORT}/callback）...", file=sys.stderr)
    try:
        webbrowser.open(auth_url)
    except Exception:
        pass  # 没浏览器就让用户手动复制
    server.handle_request()
    server.server_close()

    if "code" not in captured:
        raise FeishuError("OAuth 回调未收到 code")
    if captured["state"] != expected_state:
        raise FeishuError(
            f"OAuth state 不匹配（防 CSRF）：expected={expected_state} got={captured['state']}"
        )

    token_data = _exchange_oauth_token({
        "grant_type": "authorization_code",
        "code": captured["code"],
    })
    save_user_token(token_data)
    print("  ✓ token 已保存", file=sys.stderr)
    return token_data["access_token"]


def refresh_user_token():
    if not USER_TOKEN_CACHE_PATH.exists():
        raise FeishuError("没有 user_token 缓存，请先运行 push.py --login")
    cache = json.loads(USER_TOKEN_CACHE_PATH.read_text())
    if cache.get("refresh_expires_at", 0) <= time.time():
        raise FeishuError(
            "refresh_token 已过期（默认 30 天），请重新运行 push.py --login"
        )
    token_data = _exchange_oauth_token({
        "grant_type": "refresh_token",
        "refresh_token": cache["refresh_token"],
    })
    save_user_token(token_data)
    return token_data["access_token"]


def get_user_token():
    """带缓存的 user_access_token。距过期 60s 以内自动 refresh。"""
    if not USER_TOKEN_CACHE_PATH.exists():
        raise FeishuError(
            "尚未登录用户身份。\n"
            "  运行：python3 <skill_path>/push.py --login"
        )
    try:
        cache = json.loads(USER_TOKEN_CACHE_PATH.read_text())
        if cache.get("expires_at", 0) > time.time() + 60:
            return cache["access_token"]
    except (json.JSONDecodeError, OSError):
        pass
    return refresh_user_token()


def user_authed_request(url, method="GET", data=None, content_type=None):
    """带 user_access_token 的请求，过期自动 refresh 重试。
    所有 Wiki/Drive 操作都用这个。
    """
    def _do(token):
        headers = {"Authorization": f"Bearer {token}"}
        if content_type:
            headers["Content-Type"] = content_type
        return http_request(url, method=method, headers=headers, data=data)

    token = get_user_token()
    try:
        return _do(token)
    except RuntimeError as e:
        if "99991668" in str(e) or "99991664" in str(e) or "HTTP 401" in str(e):
            token = refresh_user_token()
            return _do(token)
        raise


def user_token_status():
    """返回 (logged_in, expires_in_seconds_or_None)，给 --status 用。"""
    if not USER_TOKEN_CACHE_PATH.exists():
        return False, None
    try:
        cache = json.loads(USER_TOKEN_CACHE_PATH.read_text())
        remain = cache.get("refresh_expires_at", 0) - int(time.time())
        return True, max(0, remain)
    except Exception:
        return False, None


# ---------- 通用 API（所有 skill 都可能用到） ----------

def get_root_folder_token():
    """获取个人云空间根目录 token（用户身份）。"""
    res = user_authed_request(f"{API_BASE}/drive/explorer/v2/root_folder/meta")
    if res.get("code") != 0:
        raise FeishuError(
            f"获取个人云空间根目录失败: {res.get('msg')}"
            f"（user_access_token 是否有 drive 读权限？）"
        )
    return res["data"]["token"]


def upload_file(file_path, parent_node, parent_type="explorer", mime=None):
    """上传文件到云空间，返回 file_token（用户身份）。"""
    file_path = Path(file_path)
    content = file_path.read_bytes()
    if mime is None:
        mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    fields = {
        "file_name": file_path.name,
        "parent_type": parent_type,
        "parent_node": parent_node,
        "size": str(len(content)),
    }
    payload, boundary = build_multipart(
        fields, [("file", file_path.name, content, mime)]
    )
    res = user_authed_request(
        f"{API_BASE}/drive/v1/medias/upload_all",
        method="POST",
        data=payload,
        content_type=f"multipart/form-data; boundary={boundary}",
    )
    if res.get("code") != 0:
        raise FeishuError(
            f"上传文件失败: {res.get('msg')}（user_access_token 是否有 drive 上传权限？）"
        )
    return res["data"]["file_token"]


def list_wikis():
    """列出当前用户身份可访问的所有 Wiki 空间。"""
    res = user_authed_request(f"{API_BASE}/wiki/v2/spaces?page_size=50")
    if res.get("code") != 0:
        raise FeishuError(f"列出 Wiki 空间失败: {res.get('msg')}")
    return res["data"].get("items", [])


# ---------- Setup 状态判断（SKILL.md 流程用） ----------

def setup_state(skill_name):
    """返回 (creds_ok, business_ok)，决定走哪一段 setup。"""
    return credentials_exist(), business_config_exists(skill_name)
