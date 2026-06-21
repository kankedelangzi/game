# CC套（宫廷套装）各职业加成数值 — 稳态核查报告

**核查时间**: 2026-06-22 03:33 (Asia/Shanghai)  
**核查版本**: v213 稳态维护  
**核查类型**: 周期性稳态验证（独立验算 + 交叉验证）

---

## 一、核查清单

### 1.1 CC套6件套核心属性验证

| 属性 | 报告数值 | 预期数值 | 状态 |
|------|----------|----------|------|
| 力量 | +310 | 55+55+50+50+50+50 = 310 | ✅ |
| 物理攻击 | +110 | 20+20+18+18+18+16 = 110 | ✅ |
| 独立攻击 | +120 | 20+20+18+18+18+26 = 120 | ✅ |
| 暴击率 | +3% | 0.5%×6 = 3% | ✅ |

### 1.2 狂战士收益验证

| 乘区 | 报告数值 | Python验算 | 状态 |
|------|----------|------------|------|
| 独立攻击收益 | +8.0% | (1+1370/250)/(1+1250/250)-1 = 6.48/6.0-1 = 8.0% | ✅ |
| 暴击收益 | +1.2% | (1.29/1.275)-1 = 1.18% ≈ 1.2% | ✅ |
| 固伤综合 | +9.27% | (1+8.0%)(1+1.18%)-1 = 9.27% | ✅ |
| 力量收益（百分比） | +24.42% | (1+1329.2/250)/(1+1019.2/250)-1 = 6.3168/5.0768-1 = 24.42% | ✅ |
| 物理攻击收益 | +5.50% | 2110/2000-1 = 5.50% | ✅ |
| 百分比综合 | +32.81% | 6.3168/5.0768 × 2110/2000 × 1290/1275 - 1 = 32.81% | ✅ |

### 1.3 剑魂收益验证

| 乘区 | 报告数值 | Python验算 | 状态 |
|------|----------|------------|------|
| 力量收益 | +36.5% | (1+910/250)/(1+600/250)-1 = 4.64/3.4-1 = 36.47% ≈ 36.5% | ✅ |
| 物理攻击收益 | +4.23% | 2710/2600-1 = 4.23% | ✅ |
| 暴击收益 | +1.2% | (1.265/1.25)-1 = 1.2% | ✅ |
| 百分比综合 | +43.95% | 1.3647 × 1.0423 × 1.012 - 1 = 43.95% | ✅ |

---

## 二、Python独立验算脚本

```python
# CC套收益验算 - 2026-06-22 稳态核查

# ===== 狂战士 =====
# 基础面板
berserker_power = 728  # 基础力量
berserker_power_berserk = 728 * 1.40  # 暴走后
berserker_indep = 1250  # 独立攻击
berserker_phy = 2000  # 物理攻击
berserker_crit = 0.55  # 暴击率55%

# CC套加成
cc_power = 310
cc_phy = 110
cc_indep = 120
cc_crit = 0.03

# 固伤收益
indep_old = 1 + berserker_indep / 250
indep_new = 1 + (berserker_indep + cc_indep) / 250
indep_gain = indep_new / indep_old - 1
print(f"独立攻击收益: {indep_gain*100:.2f}%")

# 暴击收益（期望伤害系数）
crit_old = (1 - berserker_crit) + berserker_crit * 1.5
crit_new = (1 - (berserker_crit + cc_crit)) + (berserker_crit + cc_crit) * 1.5
crit_gain = crit_new / crit_old - 1
print(f"暴击收益: {crit_gain*100:.2f}%")

# 固伤综合
berserker_fixed_total = (1 + indep_gain) * (1 + crit_gain) - 1
print(f"固伤综合收益: {berserker_fixed_total*100:.2f}%")

# 百分比收益
power_old = 1 + berserker_power_berserk / 250
power_new = 1 + (berserker_power_berserk + cc_power) / 250
power_gain = power_new / power_old - 1
print(f"力量收益: {power_gain*100:.2f}%")

phy_old = berserker_phy
phy_new = berserker_phy + cc_phy
phy_gain = phy_new / phy_old - 1
print(f"物理攻击收益: {phy_gain*100:.2f}%")

# 百分比综合
berserker_percent_total = power_new/power_old * phy_new/phy_old * crit_new/crit_old - 1
print(f"百分比综合收益: {berserker_percent_total*100:.2f}%")

# ===== 剑魂 =====
swordsman_power = 600
swordsman_phy_base = 2000
swordsman_phy_burst = swordsman_phy_base * 1.30  # 破极兵刃
swordsman_crit = 0.50

# 力量收益
sp_power_old = 1 + swordsman_power / 250
sp_power_new = 1 + (swordsman_power + cc_power) / 250
sp_power_gain = sp_power_new / sp_power_old - 1
print(f"剑魂力量收益: {sp_power_gain*100:.2f}%")

# 物理攻击收益（破极后）
sp_phy_old = swordsman_phy_burst
sp_phy_new = swordsman_phy_burst + cc_phy
sp_phy_gain = sp_phy_new / sp_phy_old - 1
print(f"剑魂物理攻击收益: {sp_phy_gain*100:.2f}%")

# 暴击收益
sp_crit_old = (1 - swordsman_crit) + swordsman_crit * 1.5
sp_crit_new = (1 - (swordsman_crit + cc_crit)) + (swordsman_crit + cc_crit) * 1.5
sp_crit_gain = sp_crit_new / sp_crit_old - 1
print(f"剑魂暴击收益: {sp_crit_gain*100:.2f}%")

# 百分比综合
swordsman_total = sp_power_new/sp_power_old * sp_phy_new/sp_phy_old * sp_crit_new/sp_crit_old - 1
print(f"剑魂百分比综合收益: {swordsman_total*100:.2f}%")
```

### Python验算结果

```
独立攻击收益: 8.00%
暴击收益: 1.18%
固伤综合收益: 9.27%
力量收益: 24.42%
物理攻击收益: 5.50%
百分比综合收益: 32.81%
剑魂力量收益: 36.47%
剑魂物理攻击收益: 4.23%
剑魂暴击收益: 1.20%
剑魂百分比综合收益: 43.95%
```

**全部10项验算与报告数据精确匹配** ✅

---

## 三、交叉验证检查

### 3.1 技能分类验证

| 职业 | 技能 | 类型 | 来源 | 状态 |
|------|------|------|------|------|
| 狂战士 | 十字斩 | 固伤 | NGA精品帖 | ✅ |
| 狂战士 | 血气之刃 | 固伤 | NGA精品帖 | ✅ |
| 狂战士 | 怒气爆发 | 固伤 | NGA精品帖 | ✅ |
| 狂战士 | 嗜魂之手 | 固伤 | NGA精品帖 | ✅ |
| 狂战士 | 崩山击 | 混合（百分比主伤+出血固伤） | DNF Wiki | ✅ |
| 狂战士 | 崩山裂地斩 | 百分比 | NGA精品帖 | ✅ |
| 狂战士 | 嗜魂封魔斩 | 百分比 | NGA精品帖 | ✅ |
| 剑魂 | 幻影剑舞 | 百分比 | DNF Wiki | ✅ |
| 剑魂 | 破军升龙击 | 百分比 | DNF Wiki | ✅ |
| 剑魂 | 猛龙断空斩 | 百分比 | DNF Wiki | ✅ |

### 3.2 武器类型验证

| 武器 | 类型 | 等级 | 来源 | 状态 |
|------|------|------|------|------|
| 屠戮之刃 | 太刀 | 55级SS | DNF Wiki | ✅ |
| 魂·巨剑 | 巨剑 | 65级SS | DNF Wiki | ✅ |

### 3.3 数据来源标注检查

| 数据类型 | 标注情况 | 状态 |
|----------|----------|------|
| CC套单件属性 | DNF Wiki-时装属性表 | ✅ |
| 6件套套装效果 | DNF Wiki/玩家实测 | ✅ |
| 狂战士面板 | 任务15验证 | ✅ |
| 剑魂面板 | 任务17验证 | ✅ |
| 伤害公式 | 任务11-17验证体系 | ✅ |

---

## 四、知识库一致性检查

### 4.1 BERSERKER.md 一致性

| 项目 | 知识库数值 | HTML报告数值 | 状态 |
|------|------------|--------------|------|
| 6件套力量 | +310 | +310 | ✅ |
| 6件套物理攻击 | +110 | +110 | ✅ |
| 6件套独立攻击 | +120 | +120 | ✅ |
| 6件套暴击 | +3% | +3% | ✅ |
| 固伤综合收益 | +9.27% | +9.27% | ✅ |
| 百分比综合收益 | +32.81% | +32.81% | ✅ |

### 4.2 SWORDSMAN.md 一致性

| 项目 | 知识库数值 | HTML报告数值 | 状态 |
|------|------------|--------------|------|
| 6件套力量 | +310 | +310 | ✅ |
| 6件套物理攻击 | +110 | +110 | ✅ |
| 6件套独立攻击 | +120 | +120 | ✅ |
| 6件套暴击 | +3% | +3% | ✅ |
| 百分比综合收益 | +43.95% | +43.95% | ✅ |

---

## 五、审核结论

| 检查项 | 数量 | 通过 | 通过率 |
|--------|------|------|--------|
| CC套属性验证 | 4 | 4 | 100% |
| 狂战士收益验算 | 6 | 6 | 100% |
| 剑魂收益验算 | 4 | 4 | 100% |
| 技能分类验证 | 7 | 7 | 100% |
| 武器类型验证 | 2 | 2 | 100% |
| 数据来源标注 | 5 | 5 | 100% |
| 知识库一致性 | 2 | 2 | 100% |
| **总计** | **30** | **30** | **100%** |

---

## 六、稳态维护确认

✅ **CC套（宫廷套装）各职业加成数值数据持续准确**  
✅ **所有核心数据与Python独立验算精确匹配**  
✅ **知识库与HTML报告数据一致**  
✅ **数据来源标注完整**  

**阶段2任务19状态**: ✅ 完成（稳态维护中）  
**连续稳态核查轮次**: 第16轮（v199→v214）  
**累计稳态核查通过率**: 100%

---

**审核报告保存路径**: `notes/bonus-system/REVIEW-2026-06-22-cron-0333-CC-steady-state.md`  
**Git提交**: 待推送至 `kankedelangzi/game`