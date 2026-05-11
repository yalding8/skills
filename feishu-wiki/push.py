#!/usr/bin/env python3
"""
push.py — 把本地 Markdown 推送到飞书知识库（Wiki）。

用法：
  push.py <md_file>                # 推送 md 到配置的 Wiki 空间
  push.py --status                 # 检查 setup 状态（凭证 / 登录 / wiki 配置）
  push.py --verify                 # 完整验证（token + 云空间 + wiki）
  push.py --login                  # OAuth 授权（首次用，30 天有效）
  push.py --list-wikis             # 列出当前用户可访问的所有 Wiki 空间
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
    elif head == "--config-path":
        print(fs.CONFIG_DIR)
    elif head.startswith("-"):
        raise SystemExit(__doc__)
    else:
        cmd_push(head)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except fs.FeishuError as e:
        print(f"\n✗ {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"\n✗ {e}", file=sys.stderr)
        sys.exit(1)
