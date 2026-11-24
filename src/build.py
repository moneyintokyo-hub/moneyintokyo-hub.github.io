# 用法：python3 src/build.py  → 產生 src/artifact.html（預覽用）和 index.html（部署用）
import base64, subprocess, os, tempfile
here = os.path.dirname(os.path.abspath(__file__)); root = os.path.dirname(here)
tmp = os.path.join(tempfile.mkdtemp(), 'a.jpg')
subprocess.run(['sips', '-Z', '176', '-s', 'format', 'jpeg', '-s', 'formatOptions', '85', os.path.join(root, 'avatar.png'), '--out', tmp], check=True, capture_output=True)
b = base64.b64encode(open(tmp, 'rb').read()).decode()
p = open(os.path.join(here, 'page.html')).read().replace('{{AVATAR}}', 'data:image/jpeg;base64,' + b)
import re
p = re.sub(r'\{\{T:([A-Za-z0-9_-]+)\}\}', lambda m: 'data:image/jpeg;base64,' + base64.b64encode(open(os.path.join(here, 'thumbs', m.group(1) + '.jpg'), 'rb').read()).decode(), p)
open(os.path.join(here, 'artifact.html'), 'w').write(p)
head, body = p.split('<main', 1)
head = head.replace('<title>Money in Tokyo 連結主頁</title>', '<title>Money in Tokyo｜Josh</title>').replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
full = '''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="我是 Josh，在東京做交易。YouTube 頻道、Telegram 社群、Bitunix 手續費 8 折、TradingView 連結都在這裡。">
<meta property="og:title" content="Money in Tokyo｜Josh">
<meta property="og:description" content="在東京做交易，帶你從零開始學技術分析。">
<meta property="og:image" content="https://moneyintokyo-hub.github.io/avatar.png">
<meta property="og:url" content="https://moneyintokyo-hub.github.io/">
<meta name="theme-color" content="#090807">
<link rel="icon" href="avatar.png">
''' + head + '</head>\n<body>\n<main' + body + '</body>\n</html>\n'
open(os.path.join(root, 'index.html'), 'w').write(full)
print('ok', len(p))
