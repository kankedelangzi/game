#!/usr/bin/env python3
"""
DNF 70版本 CC套（宫廷套装）各职业加成数值 — 独立验算脚本
版本: v414
时间: 2026-06-25 16:15 CST
"""

import json
from datetime import datetime

results = []
all_pass = True

def check(name, expected, actual, tol=0.001):
    global all_pass
    passed = abs(expected - actual) <= tol
    if not passed:
        all_pass = False
    results.append({
        "name": name,
        "expected": round(expected, 6),
        "actual": round(actual, 6),
        "diff": round(abs(expected - actual), 6),
        "pass": passed
    })
    status = "✅" if passed else "❌"
    print(f"  {status} {name}: 期望={expected:.6f}, 实际={actual:.6f}, 差异={abs(expected-actual):.6f}")

# ========== 1. CC套6件套属性合计 ==========
print("\n=== 1. CC套6件套属性合计 ===")
# 上衣: 55+20+20+0.5%, 下装: 55+20+20+0.5%, 头饰: 50+18+18+0.5%, 帽子: 50+18+18+0.5%, 脸部: 50+18+18+0.5%, 胸部: 50+16+26+0.5%
strength_total = 55+55+50+50+50+50  # = 310
phy_atk_total = 20+20+18+18+18+16   # = 110
ind_atk_total = 20+20+18+18+18+26   # = 120
crit_total = 0.5*6                   # = 3.0%

check("CC套力量合计", 310, strength_total)
check("CC套物理攻击合计", 110, phy_atk_total)
check("CC套独立攻击合计", 120, ind_atk_total)
check("CC套暴击率合计", 3.0, crit_total)

# ========== 2. 狂战士收益 ==========
print("\n=== 2. 狂战士收益 ===")

# 基础面板
berserk_strength = 728
berserk_strength_buff = 728 * 1.40  # 1019.2
berserk_ind_atk = 1250
berserk_phy_atk = 2000
berserk_crit = 0.55

# 2.1 独立攻击收益
berserk_ind_new = berserk_ind_atk + 120  # 1370
berserk_ind_gain = (1 + berserk_ind_new/250) / (1 + berserk_ind_atk/250) - 1
check("狂战士独立攻击收益", 0.08, berserk_ind_gain)

# 2.2 暴击收益（期望伤害系数）
berserk_crit_new = berserk_crit + 0.03  # 58%
berserk_crit_exp_old = (1 - berserk_crit) + berserk_crit * 1.5  # 1.275
berserk_crit_exp_new = (1 - berserk_crit_new) + berserk_crit_new * 1.5  # 1.29
berserk_crit_gain = berserk_crit_exp_new / berserk_crit_exp_old - 1
check("狂战士暴击收益", 0.011765, berserk_crit_gain)  # 1.18%

# 2.3 固伤综合收益
berserk_fixed_total = (1 + berserk_ind_gain) * (1 + berserk_crit_gain) - 1
check("狂战士固伤综合收益", 0.0927, berserk_fixed_total)

# 2.4 力量收益（百分比技能，暴走后）
berserk_str_new = berserk_strength_buff + 310  # 1329.2
berserk_str_gain = (1 + berserk_str_new/250) / (1 + berserk_strength_buff/250) - 1
check("狂战士力量收益(百分比)", 0.2442, berserk_str_gain)

# 2.5 物理攻击收益（百分比技能）
berserk_phy_new = berserk_phy_atk + 110  # 2110
berserk_phy_gain = berserk_phy_new / berserk_phy_atk - 1
check("狂战士物理攻击收益(百分比)", 0.055, berserk_phy_gain)

# 2.6 百分比综合收益
berserk_pct_total = (1 + berserk_str_gain) * (1 + berserk_phy_gain) * (1 + berserk_crit_gain) - 1
check("狂战士百分比综合收益", 0.3281, berserk_pct_total)

# ========== 3. 剑魂收益 ==========
print("\n=== 3. 剑魂收益 ===")

# 基础面板
swd_strength = 600
swd_phy_atk_base = 2000
swd_phy_atk_buff = 2000 * 1.30  # 2600 (破极兵刃)
swd_crit = 0.50

# 3.1 力量收益
swd_str_new = swd_strength + 310  # 910
swd_str_gain = (1 + swd_str_new/250) / (1 + swd_strength/250) - 1
check("剑魂力量收益", 0.3647, swd_str_gain)

# 3.2 物理攻击收益（破极后）
swd_phy_new = swd_phy_atk_buff + 110  # 2710
swd_phy_gain = swd_phy_new / swd_phy_atk_buff - 1
check("剑魂物理攻击收益(破极后)", 0.0423, swd_phy_gain)

# 3.3 暴击收益
swd_crit_new = swd_crit + 0.03  # 53%
swd_crit_exp_old = (1 - swd_crit) + swd_crit * 1.5  # 1.25
swd_crit_exp_new = (1 - swd_crit_new) + swd_crit_new * 1.5  # 1.265
swd_crit_gain = swd_crit_exp_new / swd_crit_exp_old - 1
check("剑魂暴击收益", 0.012, swd_crit_gain)

# 3.4 百分比综合收益
swd_pct_total = (1 + swd_str_gain) * (1 + swd_phy_gain) * (1 + swd_crit_gain) - 1
check("剑魂百分比综合收益", 0.4395, swd_pct_total)

# ========== 4. 边际对偶 ==========
print("\n=== 4. 边际对偶 ===")
marginal_duality = swd_pct_total / berserk_fixed_total
check("边际对偶倍数(剑魂百分比/狂战士固伤)", 4.740937, marginal_duality)

# ========== 5. 暴击期望系数 ==========
print("\n=== 5. 暴击期望系数 ===")
check("狂战士暴击期望系数(旧)", 1.275, berserk_crit_exp_old)
check("狂战士暴击期望系数(新)", 1.29, berserk_crit_exp_new)
check("剑魂暴击期望系数(旧)", 1.25, swd_crit_exp_old)
check("剑魂暴击期望系数(新)", 1.265, swd_crit_exp_new)

# ========== 汇总 ==========
print("\n" + "="*60)
passed = sum(1 for r in results if r["pass"])
total = len(results)
print(f"验算结果: {passed}/{total} 通过 ({passed/total*100:.1f}%)")
print(f"边际对偶: {marginal_duality:.6f} 倍")
print(f"狂战士固伤综合: {berserk_fixed_total*100:.2f}%")
print(f"狂战士百分比综合: {berserk_pct_total*100:.2f}%")
print(f"剑魂百分比综合: {swd_pct_total*100:.2f}%")

# 输出JSON
output = {
    "version": "v414",
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "total": total,
    "passed": passed,
    "pass_rate": f"{passed/total*100:.1f}%",
    "marginal_duality": round(marginal_duality, 6),
    "berserk_fixed_total": round(berserk_fixed_total * 100, 2),
    "berserk_pct_total": round(berserk_pct_total * 100, 2),
    "swd_pct_total": round(swd_pct_total * 100, 2),
    "results": results
}

with open("/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verifications/verification-cc-bonus-v414.json", "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n验算JSON已保存: verification-cc-bonus-v414.json")
print(f"全部通过: {all_pass}")
