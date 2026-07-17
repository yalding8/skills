#!/bin/bash
# notify-managers 发送脚本
# 用法: send.sh <message_file> [姓名1 姓名2 ...]
#   message_file 中可用 {NAME} 占位收件人姓名（自动替换）
#   不传姓名 = 发送全部 9 位主管；传姓名 = 仅发送指定人
set -u

MSG_FILE="${1:?用法: send.sh <message_file> [姓名...]}"
shift || true
FILTER=("$@")

declare -a PEOPLE=(
  "王强|ou_a9ba23e7a1b5c7a448587c326016fb4e"
  "鲍馨柔|ou_a4c72aed5683f05fc3f37f2096daa6c5"
  "刘雅婷|ou_79bb8c9614b709c77d7c0a86e09f0159"
  "韦刚|ou_fa3c91bcee8321ee05bc1f717b771b5a"
  "闫明亮|ou_4993a9a76580073b63fea586f3c95fdc"
  "张博|ou_e49600c8d1e60d762219fad118eae8c5"
  "雷宇航|ou_7668fa6e878bed2de42fee93a37d15c8"
  "杨传玉|ou_40049ccb3240bc57f95911a5cac971cd"
  "王金姣|ou_fa6c7cdf203b39a32ca5104324dab136"
)

TEMPLATE="$(cat "$MSG_FILE")"
SENT=0; FAILED=0

for p in "${PEOPLE[@]}"; do
  name="${p%%|*}"; oid="${p##*|}"
  if [ ${#FILTER[@]} -gt 0 ]; then
    match=0
    for f in "${FILTER[@]}"; do [ "$f" = "$name" ] && match=1; done
    [ $match -eq 0 ] && continue
  fi
  msg="${TEMPLATE//\{NAME\}/$name}"
  result=$(LARKSUITE_CLI_NO_UPDATE_NOTIFIER=1 LARKSUITE_CLI_NO_SKILLS_NOTIFIER=1 \
    lark-cli im +messages-send --user-id "$oid" --text "$msg" --as user 2>&1)
  if echo "$result" | grep -q '"ok": true'; then
    echo "✅ $name"; SENT=$((SENT+1))
  else
    echo "❌ $name: $(echo "$result" | head -2 | tr '\n' ' ')"; FAILED=$((FAILED+1))
  fi
  sleep 1
done

echo "---"
echo "发送完成: 成功 $SENT, 失败 $FAILED"
[ $FAILED -gt 0 ] && exit 1
exit 0
