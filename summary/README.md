# 装备伤害效果综合总结报告

## 说明
此目录存放每30分钟自动生成的装备伤害效果汇总报告。

### 输出格式
- 文件名: summary-YYYY-MM-DD-HHMM.md
- 内容: 按7大分类汇总所有装备效果
- 每次独立生成，不依赖前次结果

### 数据来源
- BERSERKER.md（狂战士知识库）
- SWORDSMAN.md（剑魂知识库）
- notes/bonus-system/（加成系统系列报告）
- notes/02-dnf-formula-analysis.md（核心公式分析）

### 生成频率
每30分钟自动执行（cron: */30 * * * *）

