#!/usr/bin/env python3
"""
push.py — 把本地 Markdown 推送到飞书知识库（Wiki）。

用法：
  push.py <md_file>                # 推送 md 到配置的 Wiki 空间
  push.py --status                 # 检查 setup 状态（凭证 / 登录 / wiki 配置）
  push.py --verify                 # 完整验证（token + 云空间 + wiki）
  push.py --login                  # OAuth 授权（首次用，30 天有效）
  push.py --list-wikis             # 列出当前用户可访问的所有 Wiki 空间
  push.py --delete <wiki_url|token># 删除 Wiki 节点（换版删旧用，移入回收站可恢复）
  push.py --embed <wiki_url|token> --image <png> [--file <pdf>]
                                   # 把长图/PDF 嵌进已存在的 Wiki 文档顶部
                                   # （md 导入不带本地图片，要图就用这个；需 docx:document 用户权限）
  push.py --init-credentials <app_id> <app_secret>
                                   # 写入共享凭证（首次 setup 用）
  push.py --init-wiki <wiki_space_id>
                                   # 写入 wiki 业务配置

配置：
  ~/.config/feishu/credentials.json   # 共享凭证
  ~/.config/feishu/wiki.json          # 本 skill 业务配置
  ~/.cache/feishu/user_token.json     # 用户身份 token（OAuth 后自动维护）
"""
import json
import mimetypes
import sys
import time
from pathlib import Path

# 加载共享 lib
sys.path.insert(0, str(Path(__file__).parent.parent / "_feishu-core"))
import feishu_lib as fs


SKILL_NAME = "wiki"


def create_import_task(file_token, file_name, drive_folder_token):
    """把 md 转成 docx 并放进云空间 folder（中转，下一步再 move 到 wiki）。"""
    res = fs.user_authed_request(
        f"{fs.API_BASE}/drive/v1/import_tasks",
        method="POST",
        data={
            "file_extension": "md",
            "file_token": file_token,
            "type": "docx",
            "file_name": file_name,
            "point": {"mount_type": 1, "mount_key": drive_folder_token},
        },
    )
    if res.get("code") != 0:
        raise fs.FeishuError(
            f"创建导入任务失败: {res.get('msg')}"
            f"（user_access_token 是否有 drive 导入权限？）"
        )
    return res["data"]["ticket"]


def move_docx_to_wiki(docx_token, wiki_space_id):
    """把云空间里的 docx 移动到 Wiki 空间根。返回 (wiki_token, task_id)。"""
    res = fs.user_authed_request(
        f"{fs.API_BASE}/wiki/v2/spaces/{wiki_space_id}/nodes/move_docs_to_wiki",
        method="POST",
        data={
            "obj_type": "docx",
            "obj_token": docx_token,
            "apply": False,
        },
    )
    if res.get("code") != 0:
        raise fs.FeishuError(
            f"移动 docx 到 Wiki 失败: code={res.get('code')} msg={res.get('msg')}"
        )
    data = res["data"]
    return data.get("wiki_token"), data.get("task_id")


def poll_wiki_move_task(task_id, max_wait=60):
    """轮询 move_docs_to_wiki 异步任务，返回 wiki_token。"""
    start = time.time()
    while time.time() - start < max_wait:
        res = fs.user_authed_request(
            f"{fs.API_BASE}/wiki/v2/tasks/{task_id}?task_type=move"
        )
        if res.get("code") != 0:
            raise fs.FeishuError(f"查询 move 任务失败: {res.get('msg')}")
        task = res["data"]["task"]
        move_result = task.get("move_result") or []
        if move_result:
            item = move_result[0]
            status = item.get("status", -1)
            if status == 0:  # 成功
                node = item.get("node") or {}
                return node.get("node_token")
            elif status not in (0,):  # 失败或处理中
                # 飞书 status 含义不明确，遇到非 0 就视为待重试
                pass
        time.sleep(2)
    return None  # 超时未拿到，返回 None 让上游 fallback


def poll_import(ticket, max_wait=180):
    start = time.time()
    last_status = None
    while time.time() - start < max_wait:
        res = fs.user_authed_request(f"{fs.API_BASE}/drive/v1/import_tasks/{ticket}")
        if res.get("code") != 0:
            raise fs.FeishuError(f"查询导入任务失败: {res.get('msg')}")
        result = res["data"]["result"]
        status = result.get("job_status", -1)
        if status != last_status:
            print(f"  任务状态: {status}", file=sys.stderr)
            last_status = status
        if status == 0:
            return result
        if status in (1, 2):
            time.sleep(2)
            continue
        raise fs.FeishuError(
            f"导入失败: status={status}, error={result.get('job_error_msg')}"
        )
    raise fs.FeishuError(f"导入超时（{max_wait}s）")


# ---------- 命令 ----------

def cmd_status():
    creds_ok, biz_ok = fs.setup_state(SKILL_NAME)
    logged_in, refresh_remain = fs.user_token_status()
    print(f"凭证       ({fs.CREDENTIALS_PATH}): {'✓' if creds_ok else '✗ 未配置'}", file=sys.stderr)
    print(
        f"用户登录   ({fs.USER_TOKEN_CACHE_PATH}): "
        + (
            f"✓（refresh_token 剩 {refresh_remain // 86400}d {(refresh_remain % 86400) // 3600}h）"
            if logged_in else "✗ 未登录"
        ),
        file=sys.stderr,
    )
    print(
        f"wiki 业务  ({fs.CONFIG_DIR / 'wiki.json'}): {'✓' if biz_ok else '✗ 未配置'}",
        file=sys.stderr,
    )
    if creds_ok and biz_ok:
        cfg = fs.load_business_config(SKILL_NAME)
        print(f"  wiki_space_id: {cfg.get('wiki_space_id')}", file=sys.stderr)

    # docx:document 权限预检（决定能否 --embed 嵌长图/PDF）。只在已登录时探测。
    if creds_ok and logged_in:
        probe = _probe_docx_permission()
        if probe == "ok":
            cap = "✓ 可用"
        elif probe == "missing":
            cap = "✗ 缺 docx:document（md 文本可推，长图需手动拖或开权限后用 --embed）"
        else:
            cap = "? 未知（无可探测的 docx 节点或网络异常，不影响 md 推送）"
        print(f"图片嵌入   (docx:document): {cap}", file=sys.stderr)
    print("", file=sys.stderr)

    if not creds_ok:
        print("→ 第一步：完成「凭证 setup」（SKILL.md Step 1-3）", file=sys.stderr)
    elif not logged_in:
        print("→ 下一步：OAuth 登录\n  python3 push.py --login", file=sys.stderr)
    elif not biz_ok:
        print("→ 下一步：选择目标 Wiki\n  python3 push.py --list-wikis", file=sys.stderr)
    else:
        print("→ 已完成全部配置，可以直接推送。", file=sys.stderr)


def cmd_login():
    if not fs.credentials_exist():
        raise SystemExit("尚未配置凭证。先运行：push.py --init-credentials <app_id> <app_secret>")
    token = fs.oauth_login()
    print(f"  ✓ user_access_token 前 12 字符: {token[:12]}", file=sys.stderr)
    print("\n下一步：python3 push.py --list-wikis", file=sys.stderr)


def cmd_verify():
    print(f"凭证: {fs.CREDENTIALS_PATH}", file=sys.stderr)
    print(f"wiki 配置: {fs.CONFIG_DIR / 'wiki.json'}", file=sys.stderr)

    print("→ 检查 user_access_token...", file=sys.stderr)
    token = fs.get_user_token()
    print(f"  ✓ token 前 12 字符: {token[:12]}", file=sys.stderr)

    print("→ 检查个人云空间访问...", file=sys.stderr)
    root = fs.get_root_folder_token()
    print(f"  ✓ root folder token: {root[:12]}...", file=sys.stderr)

    print("→ 检查 Wiki 空间访问...", file=sys.stderr)
    wikis = fs.list_wikis()
    cfg = fs.load_business_config(SKILL_NAME)
    target_id = cfg.get("wiki_space_id")
    if not target_id:
        print(f"  ⚠️  尚未配置 wiki_space_id，可访问空间：", file=sys.stderr)
        for w in wikis:
            print(f"    - {w.get('name')}（{w.get('space_id')}）", file=sys.stderr)
        return
    target = next((w for w in wikis if w.get("space_id") == target_id), None)
    if not target:
        names = [f"  - {w.get('name')}（{w.get('space_id')}）" for w in wikis]
        raise SystemExit(
            f"  ✗ wiki_space_id {target_id} 不在可访问列表里。\n"
            f"    可访问的空间：\n"
            + ("\n".join(names) if names else "    （空 — 应用未被加为 Wiki 协作者）")
        )
    print(f"  ✓ Wiki 空间名: {target.get('name')}", file=sys.stderr)
    print("\n所有检查通过 ✅", file=sys.stderr)


def cmd_list_wikis():
    wikis = fs.list_wikis()
    if not wikis:
        print("（空 — 应用未被加为任何 Wiki 协作者）", file=sys.stderr)
        return
    for w in wikis:
        print(f"{w.get('space_id')}\t{w.get('name')}\t{w.get('space_type')}")


def cmd_init_credentials(app_id, app_secret):
    fs.save_credentials(app_id, app_secret)
    print(f"✓ 凭证已写入 {fs.CREDENTIALS_PATH}（权限 600）", file=sys.stderr)
    print("→ 验证 tenant_access_token（确认 app_id/secret 正确）...", file=sys.stderr)
    token = fs.get_tenant_token(force_refresh=True)
    print(f"  ✓ token 获取成功（前 12 字符: {token[:12]}）", file=sys.stderr)
    print("\n下一步：OAuth 登录用户身份\n  python3 push.py --login", file=sys.stderr)


def cmd_init_wiki(wiki_space_id):
    if not fs.credentials_exist():
        raise SystemExit("尚未配置凭证。先运行：push.py --init-credentials <app_id> <app_secret>")
    fs.save_business_config(SKILL_NAME, {"wiki_space_id": wiki_space_id})
    print(f"✓ wiki 配置已写入 {fs.CONFIG_DIR / 'wiki.json'}", file=sys.stderr)
    print("→ 验证 wiki 协作者...", file=sys.stderr)
    wikis = fs.list_wikis()
    target = next((w for w in wikis if w.get("space_id") == wiki_space_id), None)
    if not target:
        names = [f"    - {w.get('name')}（{w.get('space_id')}）" for w in wikis]
        raise SystemExit(
            f"  ✗ wiki_space_id 不在可访问列表（应用未加为该 Wiki 协作者）。\n"
            f"  可访问的空间：\n" + ("\n".join(names) if names else "    （空）")
        )
    print(f"  ✓ Wiki 空间名: {target.get('name')}", file=sys.stderr)
    print("\n配置完成 ✅ 可以推送 md 了。", file=sys.stderr)


def cmd_push(md_arg):
    md_path = Path(md_arg).expanduser().resolve()
    if not md_path.exists() or md_path.suffix.lower() not in (".md", ".markdown"):
        raise SystemExit(f"文件不存在或不是 Markdown：{md_path}")
    cfg = fs.load_business_config(SKILL_NAME)
    wiki_space_id = cfg.get("wiki_space_id")
    if not wiki_space_id:
        raise SystemExit(
            "尚未配置 wiki_space_id。\n"
            "  运行：push.py --init-wiki <wiki_space_id>"
        )

    print(f"→ 推送 {md_path.name} 到 Wiki space {wiki_space_id}...", file=sys.stderr)
    root = fs.get_root_folder_token()
    file_token = fs.upload_file(md_path, root)
    print(f"  ✓ 已上传到云空间，file_token={file_token[:12]}...", file=sys.stderr)
    ticket = create_import_task(file_token, md_path.stem, root)
    print(f"  ✓ 创建导入任务 ticket={ticket}", file=sys.stderr)
    import_result = poll_import(ticket)
    docx_token = import_result.get("token")
    docx_url = import_result.get("url", "")
    if not docx_token:
        raise fs.FeishuError(f"导入任务完成但没拿到 docx token：{import_result}")
    print(f"  ✓ md → docx 完成，docx_token={docx_token[:12]}...", file=sys.stderr)
    print(f"→ 移动 docx 到 Wiki 空间...", file=sys.stderr)
    wiki_token, task_id = move_docx_to_wiki(docx_token, wiki_space_id)
    if not wiki_token and task_id:
        print(f"  ⏳ 异步任务 task_id={task_id}，等待挂载完成...", file=sys.stderr)
        wiki_token = poll_wiki_move_task(task_id)
    if wiki_token:
        print(f"  ✓ 已挂载到 Wiki，wiki_token={wiki_token[:12]}...", file=sys.stderr)
    else:
        print(f"  ⚠️  没拿到 wiki_token，输出 docx URL（飞书会自动跳转）", file=sys.stderr)
    domain = docx_url.split("/")[2] if docx_url else ""
    if wiki_token and domain:
        wiki_url = f"https://{domain}/wiki/{wiki_token}"
    else:
        wiki_url = docx_url  # fallback
    print("\n✅ 推送完成", file=sys.stderr)
    print(wiki_url)  # stdout 只输出 URL，便于管道


def _extract_wiki_token(arg):
    """从 wiki URL 或裸 token 取出 node token。
    支持 https://xxx.feishu.cn/wiki/<token>[?...] 或直接 <token>。
    """
    arg = arg.strip()
    if "/wiki/" in arg:
        arg = arg.split("/wiki/", 1)[1]
    # 剥查询参数 / 锚点 / 多余路径段
    return arg.split("?")[0].split("#")[0].split("/")[0]


def _get_wiki_node(token):
    """取 wiki 节点详情；返回 node dict 或 None（节点不存在）。"""
    url = f"{fs.API_BASE}/wiki/v2/spaces/get_node?token={token}&obj_type=wiki"
    try:
        res = fs.user_authed_request(url)
    except RuntimeError:
        return None  # HTTP 4xx（如 404）
    if res.get("code") != 0:
        return None  # 业务码非 0（如 131005 not found）
    return res.get("data", {}).get("node")


def cmd_delete(arg):
    """删除 Wiki 节点：取底层 obj_token → drive 文件删除（移入回收站，可恢复）。

    用户身份 token 对自己创建的文档有删除权限——飞书 Wiki 无"删除节点"公开 API，
    走删底层云文档使节点失效这条路。换版"推新→删旧→验证"的删旧步骤。
    """
    if not fs.credentials_exist():
        raise SystemExit("尚未配置凭证。先运行：push.py --init-credentials <app_id> <app_secret>")
    token = _extract_wiki_token(arg)
    node = _get_wiki_node(token)
    if not node:
        raise SystemExit(f"未找到 Wiki 节点（token={token}）——可能已删除或 token 有误")
    obj_token = node.get("obj_token")
    obj_type = node.get("obj_type", "docx")
    title = node.get("title", "")
    if not obj_token:
        raise SystemExit(f"节点缺 obj_token，无法删除：{node}")
    print(f"→ 删除 Wiki 节点「{title}」(obj_type={obj_type}) ...", file=sys.stderr)
    res = fs.user_authed_request(
        f"{fs.API_BASE}/drive/v1/files/{obj_token}?type={obj_type}",
        method="DELETE",
    )
    if res.get("code") != 0:
        raise fs.FeishuError(f"删除失败: code={res.get('code')} msg={res.get('msg')}")
    # 验证：节点应已不可查
    if _get_wiki_node(token) is None:
        print("  ✓ 已删除（移入回收站，可恢复）", file=sys.stderr)
    else:
        print("  ⚠️ 删除请求已受理，但节点暂时仍可查到（飞书索引延迟）", file=sys.stderr)
    print(f"\n✅ 删除完成：{title}", file=sys.stderr)


# ---------- docx:document 权限相关 ----------

class DocxPermissionError(fs.FeishuError):
    """缺 docx:document 用户权限时抛出，main 捕获后打印优雅指引。"""


def _is_docx_perm_error(exc):
    """判断异常是否是「缺 docx:document 权限」。
    覆盖两种形态：业务 code 99991672，或 HTTP 400 body 里含 docx:document。
    """
    s = str(exc)
    if "99991672" in s:
        return True
    if "docx:document" in s:
        return True
    return False


def _docx_perm_guidance():
    return (
        "✗ 缺 docx:document 用户权限——无法把图片/附件块写进 Wiki 文档。\n"
        "  修复步骤（三步，缺一不可）：\n"
        "    1. 打开 https://open.feishu.cn/app → 选中应用（cli_...）→「权限管理」\n"
        "       搜索并开通 docx:document（注意要「用户身份」一栏勾上）\n"
        "    2.「版本管理与发布」创建新版本并发布（个人版立即生效）\n"
        "    3. 重新授权拿带新 scope 的 user_token：\n"
        "         python3 ~/.claude/skills/feishu-wiki/push.py --login\n"
        "  完成后重跑 --embed 即可。\n"
        "  （临时替代：在飞书界面手动把长图/PDF 拖进文档）"
    )


def _docx_call(url, method="GET", data=None, content_type=None):
    """包一层 user_authed_request，把 docx:document 权限错统一转成 DocxPermissionError。"""
    try:
        res = fs.user_authed_request(url, method=method, data=data, content_type=content_type)
    except RuntimeError as e:
        if _is_docx_perm_error(e):
            raise DocxPermissionError(_docx_perm_guidance())
        raise
    if res.get("code") == 99991672:
        raise DocxPermissionError(_docx_perm_guidance())
    return res


def _resolve_docx_obj_token(wiki_token):
    """从 wiki node 取底层 docx obj_token。非 docx 节点报错。"""
    node = _get_wiki_node(wiki_token)
    if not node:
        raise SystemExit(f"未找到 Wiki 节点（token={wiki_token}）——token 有误或无权访问")
    obj_token = node.get("obj_token")
    obj_type = node.get("obj_type", "")
    title = node.get("title", "")
    if obj_type != "docx" or not obj_token:
        raise SystemExit(
            f"节点「{title}」obj_type={obj_type}，不是 docx 文档，无法嵌入图片/附件"
        )
    return obj_token, title


def _insert_block(doc_token, block_type, block_key):
    """在文档顶部（index 0）插入一个空的图片块(27)/文件块(23)，返回新 block_id。"""
    res = _docx_call(
        f"{fs.API_BASE}/docx/v1/documents/{doc_token}/blocks/{doc_token}/children",
        method="POST",
        data={"index": 0, "children": [{"block_type": block_type, block_key: {"token": ""}}]},
    )
    if res.get("code") != 0:
        raise fs.FeishuError(
            f"插入 {block_key} 块失败: code={res.get('code')} msg={res.get('msg')}"
        )
    children = res.get("data", {}).get("children") or []
    if not children:
        raise fs.FeishuError(f"插入 {block_key} 块成功但未返回 block_id：{res}")
    return children[0].get("block_id")


def _upload_media_to_block(file_path, block_id, doc_token, parent_type):
    """把媒体文件上传并绑定到指定 block，返回 file_token。
    upload_file 不支持 extra 字段，这里用 build_multipart 自己拼。
    """
    file_path = Path(file_path)
    content = file_path.read_bytes()
    mime = mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"
    fields = {
        "file_name": file_path.name,
        "parent_type": parent_type,
        "parent_node": block_id,
        "size": str(len(content)),
        "extra": json.dumps({"drive_route_token": doc_token}),
    }
    payload, boundary = fs.build_multipart(
        fields, [("file", file_path.name, content, mime)]
    )
    res = _docx_call(
        f"{fs.API_BASE}/drive/v1/medias/upload_all",
        method="POST",
        data=payload,
        content_type=f"multipart/form-data; boundary={boundary}",
    )
    if res.get("code") != 0:
        raise fs.FeishuError(
            f"上传媒体失败: code={res.get('code')} msg={res.get('msg')}"
        )
    return res.get("data", {}).get("file_token")


def _patch_block_media(doc_token, block_id, replace_key, file_token):
    """回填：把上传得到的 file_token 写进图片/文件块。"""
    res = _docx_call(
        f"{fs.API_BASE}/docx/v1/documents/{doc_token}/blocks/{block_id}",
        method="PATCH",
        data={replace_key: {"token": file_token}},
    )
    if res.get("code") != 0:
        raise fs.FeishuError(
            f"回填 {replace_key} 失败: code={res.get('code')} msg={res.get('msg')}"
        )


def _embed_one(doc_token, file_path, block_type, parent_type, block_key, replace_key, label):
    """通用：插块 → 上传媒体 → 回填。"""
    print(f"→ 嵌入{label}：{file_path.name} ...", file=sys.stderr)
    block_id = _insert_block(doc_token, block_type, block_key)
    print(f"  ✓ 已插入空{label}块 block_id={block_id[:12]}...", file=sys.stderr)
    file_token = _upload_media_to_block(file_path, block_id, doc_token, parent_type)
    print(f"  ✓ 已上传媒体 file_token={file_token[:12]}...", file=sys.stderr)
    _patch_block_media(doc_token, block_id, replace_key, file_token)
    print(f"  ✓ 已回填到{label}块", file=sys.stderr)


def cmd_embed(wiki_arg, image_path, file_path):
    if not fs.credentials_exist():
        raise SystemExit("尚未配置凭证。先运行：push.py --init-credentials <app_id> <app_secret>")
    img = Path(image_path).expanduser().resolve()
    if not img.exists():
        raise SystemExit(f"图片文件不存在：{img}")
    pdf = None
    if file_path:
        pdf = Path(file_path).expanduser().resolve()
        if not pdf.exists():
            raise SystemExit(f"附件文件不存在：{pdf}")

    wiki_token = _extract_wiki_token(wiki_arg)
    doc_token, title = _resolve_docx_obj_token(wiki_token)
    print(f"→ 目标文档「{title}」docx_token={doc_token[:12]}...", file=sys.stderr)

    # 文件块先插（index 0），图片块后插（index 0）→ 图片最终在最顶部，附件紧随其后。
    # 顺序无强约束；这里图片优先展示。
    if pdf:
        _embed_one(doc_token, pdf, 23, "docx_file", "file", "replace_file", "文件块")
    _embed_one(doc_token, img, 27, "docx_image", "image", "replace_image", "图片块")

    print("\n✅ 嵌入完成", file=sys.stderr)
    # stdout 只输出 wiki URL，便于管道。域名沿用调用方传入的（裸 token 时退回通用域名）。
    if "/wiki/" in wiki_arg and "://" in wiki_arg:
        domain = wiki_arg.split("://", 1)[1].split("/", 1)[0]
    else:
        domain = "feishu.cn"
    print(f"https://{domain}/wiki/{wiki_token}", file=sys.stdout)


def _probe_docx_permission():
    """docx:document 权限最小只读探测。
    返回 'ok' / 'missing' / 'unknown'。不抛异常。

    策略：从可访问 Wiki 里找一个 docx 节点，对它发一次 GET blocks。
      - code 0          → ✓ 可用
      - 99991672 / docx:document → ✗ 缺权限
      - 其它（无 docx 节点 / 网络错）→ 未知
    """
    try:
        wikis = fs.list_wikis()
    except Exception:
        return "unknown"
    # 找任一空间根下第一个 docx 节点
    for w in wikis:
        sid = w.get("space_id")
        if not sid:
            continue
        try:
            res = fs.user_authed_request(
                f"{fs.API_BASE}/wiki/v2/spaces/{sid}/nodes?page_size=20"
            )
        except Exception:
            continue
        if res.get("code") != 0:
            continue
        for n in res.get("data", {}).get("items", []):
            if n.get("obj_type") == "docx" and n.get("obj_token"):
                doc = n["obj_token"]
                try:
                    r = fs.user_authed_request(
                        f"{fs.API_BASE}/docx/v1/documents/{doc}/blocks?page_size=1"
                    )
                except RuntimeError as e:
                    if _is_docx_perm_error(e):
                        return "missing"
                    return "unknown"
                if r.get("code") == 0:
                    return "ok"
                if r.get("code") == 99991672:
                    return "missing"
                # 其它业务码（如该文档无权访问）→ 换下一个候选
                continue
    return "unknown"


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    head, *rest = argv
    if head == "--init-credentials":
        if len(rest) != 2:
            raise SystemExit("用法: push.py --init-credentials <app_id> <app_secret>")
        cmd_init_credentials(*rest)
    elif head == "--init-wiki":
        if len(rest) != 1:
            raise SystemExit("用法: push.py --init-wiki <wiki_space_id>")
        cmd_init_wiki(rest[0])
    elif head == "--login":
        cmd_login()
    elif head == "--status":
        cmd_status()
    elif head == "--verify":
        cmd_verify()
    elif head == "--list-wikis":
        cmd_list_wikis()
    elif head == "--delete":
        if len(rest) != 1:
            raise SystemExit("用法: push.py --delete <wiki_url|token>")
        cmd_delete(rest[0])
    elif head == "--embed":
        # 解析 --embed <wiki> --image <png> [--file <pdf>]
        wiki_arg = None
        image_path = None
        file_path = None
        i = 0
        # rest[0] 可能是 wiki（位置参数）或直接 --image
        toks = rest
        while i < len(toks):
            t = toks[i]
            if t == "--image":
                i += 1
                image_path = toks[i] if i < len(toks) else None
            elif t == "--file":
                i += 1
                file_path = toks[i] if i < len(toks) else None
            elif not t.startswith("-") and wiki_arg is None:
                wiki_arg = t
            else:
                raise SystemExit(
                    "用法: push.py --embed <wiki_url|token> --image <png> [--file <pdf>]"
                )
            i += 1
        if not wiki_arg or not image_path:
            raise SystemExit(
                "用法: push.py --embed <wiki_url|token> --image <png> [--file <pdf>]"
            )
        cmd_embed(wiki_arg, image_path, file_path)
    elif head == "--config-path":
        print(fs.CONFIG_DIR)
    elif head.startswith("-"):
        raise SystemExit(__doc__)
    else:
        cmd_push(head)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except DocxPermissionError as e:
        # 优雅降级：指引信息自带 ✗ 前缀，直接打印，不糊 traceback
        print(f"\n{e}", file=sys.stderr)
        sys.exit(2)
    except fs.FeishuError as e:
        print(f"\n✗ {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"\n✗ {e}", file=sys.stderr)
        sys.exit(1)
