#!/usr/bin/env python3
"""发送任务19最终修正版汇报邮件（v57定稿）"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

SMTP_SERVER = "smtp.163.com"
SMTP_PORT = 465
SENDER = "13220707709@163.com"
SENDER_PASS = "PWZVn3AQVSKePhGM"
RECIPIENT = "308035773@qq.com"

msg = MIMEMultipart("alternative")
msg["Subject"] = "[DNF研究] 任务19完成：CC套（宫廷套装）各职业加成数值分析（v57最终定稿）"
msg["From"] = SENDER
msg["To"] = RECIPIENT

html_content = """
<html>
<body style="font-family: 'Microsoft YaHei', sans-serif; line-height: 1.8; color: #333; max-width: 800px;">
<h2 style="color: #c0392b;">📊 任务19完成汇报（v57最终定稿）</h2>

<p><strong>任务</strong>: CC套（宫廷套装）各职业加成数值分析<br>
<strong>状态</strong>: ✅ 已完成（v57最终定稿，审核100%通过，30/30项）<br>
<strong>发送时间</strong>: """ + datetime.now().strftime("%Y-%m-%d %H:%M") + """</p>

<h3 style="color: #2c3e50;">🎯 核心结论（最终修正版）</h3>

<h4>CC套6件套基础属性（阈值激活）</h4>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
  <tr style="background: #ecf0f1;"><th>部位</th><th>力量</th><th>物理攻击</th><th>独立攻击</th><th>暴击率</th></tr>
  <tr><td>上衣</td><td>55</td><td>20</td><td>20</td><td>0.5%</td></tr>
  <tr><td>下装</td><td>55</td><td>20</td><td>20</td><td>0.5%</td></tr>
  <tr><td>头饰/帽子/脸部</td><td>50×3=150</td><td>18×3=54</td><td>18×3=54</td><td>0.5%×3=1.5%</td></tr>
  <tr><td>胸部</td><td>50</td><td>16</td><td>26</td><td>0.5%</td></tr>
  <tr style="background: #f39c12; color: white;"><td><strong>合计（6件）</strong></td><td><strong>310</strong></td><td><strong>110</strong></td><td><strong>120</strong></td><td><strong>3.0%</strong></td></tr>
</table>
<p>⚠️ <strong>胸部力量修正</strong>: 实际为50（非55），故6件合计310而非315。已修正。</p>

<h4>双职业伤害收益对比（最终版）</h4>
<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; width: 100%;">
  <tr style="background: #ecf0f1;"><th>职业</th><th>流派</th><th>力量收益</th><th>物理攻击收益</th><th>独立攻击收益</th><th>暴击收益</th><th>综合收益</th></tr>
  <tr style="background: #fadbd8;"><td>🔴 狂战士</td><td>固伤流</td><td>0%</td><td>0%</td><td><strong>+8.0%</strong></td><td><strong>+1.2%</strong></td><td><strong>+9.3%</strong></td></tr>
  <tr style="background: #d6eaf8;"><td>🔵 剑魂</td><td>百分比流</td><td><strong>+36.5%</strong></td><td><strong>+2.2%</strong></td><td>0%</td><td><strong>+1.2%</strong></td><td><strong>+41.1%</strong></td></tr>
</table>

<h4>关键修正记录</h4>
<ul>
  <li>胸部力量 55→50（6件合计310而非315）</li>
  <li>物理攻击系数分母：2500（DNF 70标准公式）</li>
  <li>狂战士百分比物理攻击：+2.44%（精确验算）</li>
  <li>狂战士百分比综合：+36.67%→+36.50%（差异0.17pp）</li>
  <li>暴击收益统一：+1.2%（期望伤害系数公式）</li>
</ul>

<h3 style="color: #2c3e50;">📋 推荐搭配方案</h3>
<ul>
  <li><strong>狂战士</strong>: E2血之狂暴6件 + CC套2件（上衣+下装技能+1）</li>
  <li><strong>剑魂</strong>: E2剑舞6件 + CC套2件（上衣+下装技能+1）</li>
</ul>

<h3 style="color: #2c3e50;">📁 产出文件</h3>
<ul>
  <li>HTML报告: <code>game-damage-research/notes/bonus-system/dnf-costume-bonus.html</code></li>
  <li>GitHub: <a href="https://github.com/kankedelangzi/game">kankedelangzi/game</a></li>
  <li>知识库更新: <code>BERSERKER.md</code> + <code>SWORDSMAN.md</code></li>
</ul>

<h3 style="color: #2c3e50;">📌 下一步</h3>
<p><strong>阶段2全部完成！</strong>（20/20）<br>
待执行：阶段3远期100个任务（31-100）</p>

<hr>
<p style="color: #999; font-size: 12px;">数据来源: DNF Wiki / NGA DNF专区精品帖 / 多玩DNF攻略 | 版本锁定: 70版本末期<br>
生成时间: 2026-05-31 | 研究仓库: kankedelangzi/game</p>
</body>
</html>
"""

text_content = """
任务19完成汇报（v57最终定稿）
=====================================

任务: CC套（宫廷套装）各职业加成数值分析
状态: ✅ 已完成（v57最终定稿，审核100%通过，30/30项）

核心结论（最终修正版）
----------------------

CC套6件套基础属性（阈值激活）:
  力量: +310
  物理攻击: +110
  独立攻击: +120
  暴击率: +3%

双职业伤害收益对比:
  狂战士（固伤流）: 综合 +9.3%（独立+8.0% × 暴击+1.2%）
  剑魂（百分比流）: 综合 +41.1%（力量+36.5% × 物攻+2.2% × 暴击+1.2%）

关键修正:
  - 胸部力量 55→50（6件合计310而非315）
  - 物理攻击系数分母: 2500（DNF 70标准公式）
  - 狂战士百分比物理攻击: +2.44%
  - 狂战士百分比综合: +36.67%→+36.50%
  - 暴击收益统一: +1.2%

推荐搭配:
  狂战士: E2血之狂暴6件 + CC套2件（上衣+下装）
  剑魂: E2剑舞6件 + CC套2件（上衣+下装）

产出文件:
  HTML报告: game-damage-research/notes/bonus-system/dnf-costume-bonus.html
  GitHub: https://github.com/kankedelangzi/game

阶段2全部完成！（20/20）
"""

msg.attach(MIMEText(text_content, "plain", "utf-8"))
msg.attach(MIMEText(html_content, "html", "utf-8"))

try:
    server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
    server.login(SENDER, SENDER_PASS)
    server.sendmail(SENDER, [RECIPIENT], msg.as_string())
    server.quit()
    print("✅ 邮件发送成功！")
except Exception as e:
    print(f"❌ 邮件发送失败: {e}")
