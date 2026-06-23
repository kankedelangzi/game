#!/usr/bin/env python3
# 任务19 CC套（宫廷套装）精确验算

cc_power = 310
cc_phys_atk = 110
cc_independent = 120
cc_crit = 0.03

print("=" * 70)
print("任务19 CC套（宫廷套装）精确验算（修正版）")
print("=" * 70)
print(f"\n【CC套6件套属性】力量+{cc_power} / 物理攻击+{cc_phys_atk} / 独立攻击+{cc_independent} / 暴击+{cc_crit*100}%")

# ===== 狂战士 =====
print("\n" + "=" * 70)
print("狂战士（红眼）")
print("=" * 70)

# 固伤
b_ind_base = 1250
b_ind_new = b_ind_base + cc_independent
b_ind_gain = (b_ind_new / b_ind_base - 1) * 100
b_crit_gain = cc_crit * 100
b_fixed = (1 + b_ind_gain/100) * (1 + b_crit_gain/100) - 1
b_fixed_pct = b_fixed * 100

print(f"\n【固伤技能】")
print(f"  独立攻击: {b_ind_base} → {b_ind_new} = +{b_ind_gain:.4f}%")
print(f"  暴击期望: +{b_crit_gain:.4f}%")
print(f"  综合: (1+{b_ind_gain:.4f}%)×(1+{b_crit_gain:.4f}%)-1 = +{b_fixed_pct:.4f}%")

# 百分比
b_pwr_base = 1019.2
b_pwr_new = b_pwr_base + cc_power
b_pwr_gain = (b_pwr_new / b_pwr_base - 1) * 100
b_pa_base = 2000
b_pa_new = b_pa_base + cc_phys_atk
b_pa_gain = (b_pa_new / b_pa_base - 1) * 100
b_percent = (1 + b_pwr_gain/100) * (1 + b_pa_gain/100) * (1 + b_crit_gain/100) - 1
b_percent_pct = b_percent * 100

print(f"\n【百分比技能】")
print(f"  力量(暴走后): {b_pwr_base} → {b_pwr_new} = +{b_pwr_gain:.4f}%")
print(f"  物理攻击: {b_pa_base} → {b_pa_new} = +{b_pa_gain:.4f}%")
print(f"  暴击期望: +{b_crit_gain:.4f}%")
print(f"  综合: (1+{b_pwr_gain:.4f}%)×(1+{b_pa_gain:.4f}%)×(1+{b_crit_gain:.4f}%)-1 = +{b_percent_pct:.4f}%")

# ===== 剑魂 =====
print("\n" + "=" * 70)
print("剑魂（白手）破极兵刃状态")
print("=" * 70)

s_pwr_base = 600
s_pwr_new = s_pwr_base + cc_power
s_pwr_gain = (s_pwr_new / s_pwr_base - 1) * 100
s_pa_base = 2600
s_pa_new = s_pa_base + cc_phys_atk
s_pa_gain = (s_pa_new / s_pa_base - 1) * 100
s_percent = (1 + s_pwr_gain/100) * (1 + s_pa_gain/100) * (1 + b_crit_gain/100) - 1
s_percent_pct = s_percent * 100

print(f"\n【百分比技能】")
print(f"  力量: {s_pwr_base} → {s_pwr_new} = +{s_pwr_gain:.4f}%")
print(f"  物理攻击(破极后): {s_pa_base} → {s_pa_new} = +{s_pa_gain:.4f}%")
print(f"  暴击期望: +{b_crit_gain:.4f}%")
print(f"  综合: (1+{s_pwr_gain:.4f}%)×(1+{s_pa_gain:.4f}%)×(1+{b_crit_gain:.4f}%)-1 = +{s_percent_pct:.4f}%")

# ===== 对偶验证 =====
print("\n" + "=" * 70)
print("边际对偶验证")
print("=" * 70)
ratio = s_percent_pct / b_fixed_pct
print(f"  剑魂百分比综合 / 狂战士固伤综合 = {s_percent_pct:.4f}% / {b_fixed_pct:.4f}% = {ratio:.4f}倍")

# ===== 修正报告中的错误 =====
print("\n" + "=" * 70)
print("🔧 报告数据修正")
print("=" * 70)
print(f"  狂战士固伤综合: 报告9.27% → 实际{b_fixed_pct:.2f}% (差异{b_fixed_pct-9.27:.2f}pp)")
print(f"  狂战士百分比综合: 报告32.81% → 实际{b_percent_pct:.2f}% (差异{b_percent_pct-32.81:.2f}pp)")
print(f"  剑魂百分比综合: 报告43.95% → 实际{s_percent_pct:.2f}% (差异{s_percent_pct-43.95:.2f}pp)")
print(f"  对偶倍数: 报告4.74倍 → 实际{ratio:.2f}倍 (差异{ratio-4.74:.2f})")
