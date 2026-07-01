#!/usr/bin/env python3
"""CC套（宫廷套装）各职业加成数值验证 — v1190
基于HTML报告中经审核确认的基础面板参数进行Python独立验算
"""
import json

# ========== 基础面板参数（来自HTML报告，经多轮审核确认） ==========
# 狂战士（红眼）— 暴走状态下
BERSERKER_BASE = {
    "strength": 728.0,          # 基础力量
    "strength_aura": 1019.2,     # 暴走后力量 = 728 × 1.40
    "independent_attack": 1250,  # 独立攻击（毕业）
    "physical_attack": 2000,     # 物理攻击（毕业）
    "crit_rate_pct": 55.0        # 暴击率
}

# 剑魂（白手）— 破极兵刃状态下
SWORDSMAN_BASE = {
    "strength": 600,             # 基础力量
    "physical_attack": 2000,     # 破极前物理攻击
    "physical_attack_pj": 2600,  # 破极后物理攻击
    "crit_rate_pct": 50.0        # 暴击率
}

# CC套6件属性（6件阈值激活）
CC_SET = {
    "strength": 310,
    "physical_attack": 110,
    "independent_attack": 120,
    "crit_rate_pct": 3.0
}

# ========== 计算函数 ==========

def crit_expectation(crit_pct):
    """暴击期望伤害系数：1 + crit_rate * 0.5（70版本暴击伤害150%）"""
    return 1 + crit_pct / 100 * 0.5

def strength_multiplier(strength):
    """力量伤害乘数：1 + strength / 250"""
    return 1 + strength / 250

# ========== 狂战士固伤收益 ==========
# 独立攻击收益
ind_old = strength_multiplier(BERSERKER_BASE["independent_attack"])
ind_new = strength_multiplier(BERSERKER_BASE["independent_attack"] + CC_SET["independent_attack"])
berserker_fixed_ind = ind_new / ind_old - 1

# 暴击收益
crit_old = crit_expectation(BERSERKER_BASE["crit_rate_pct"])
crit_new = crit_expectation(BERSERKER_BASE["crit_rate_pct"] + CC_SET["crit_rate_pct"])
berserker_fixed_crit = crit_new / crit_old - 1

# 固伤综合（乘区叠加）
berserker_fixed_combined = (1 + berserker_fixed_ind) * (1 + berserker_fixed_crit) - 1

# ========== 狂战士百分比收益 ==========
# 力量收益（以暴走后力量为基准）
str_old = strength_multiplier(BERSERKER_BASE["strength_aura"])
str_new = strength_multiplier(BERSERKER_BASE["strength_aura"] + CC_SET["strength"])
berserker_pct_str = str_new / str_old - 1

# 物理攻击收益
berserker_pct_phys = (BERSERKER_BASE["physical_attack"] + CC_SET["physical_attack"]) / BERSERKER_BASE["physical_attack"] - 1

# 暴击收益（同固伤）
berserker_pct_crit = crit_new / crit_old - 1

# 百分比综合（乘区叠加）
berserker_pct_combined = (1 + berserker_pct_str) * (1 + berserker_pct_phys) * (1 + berserker_pct_crit) - 1

# ========== 剑魂百分比收益 ==========
# 力量收益
str_old_s = strength_multiplier(SWORDSMAN_BASE["strength"])
str_new_s = strength_multiplier(SWORDSMAN_BASE["strength"] + CC_SET["strength"])
swordsman_pct_str = str_new_s / str_old_s - 1

# 物理攻击收益（以破极前2000为基准，CC套+110为固定数值加成）
swordsman_pct_phys = (SWORDSMAN_BASE["physical_attack"] + CC_SET["physical_attack"]) / SWORDSMAN_BASE["physical_attack"] - 1

# 暴击收益
crit_old_s = crit_expectation(SWORDSMAN_BASE["crit_rate_pct"])
crit_new_s = crit_expectation(SWORDSMAN_BASE["crit_rate_pct"] + CC_SET["crit_rate_pct"])
swordsman_pct_crit = crit_new_s / crit_old_s - 1

# 百分比综合（乘区叠加）
swordsman_pct_combined = (1 + swordsman_pct_str) * (1 + swordsman_pct_phys) * (1 + swordsman_pct_crit) - 1

# ========== 边际对偶 ==========
marginal_duality = swordsman_pct_combined / berserker_fixed_combined

# ========== 验证 ==========
checks = [
    ("力量+310", CC_SET["strength"] == 310, CC_SET["strength"]),
    ("物理攻击+110", CC_SET["physical_attack"] == 110, CC_SET["physical_attack"]),
    ("独立攻击+120", CC_SET["independent_attack"] == 120, CC_SET["independent_attack"]),
    ("暴击+3%", abs(CC_SET["crit_rate_pct"] - 3.0) < 0.01, CC_SET["crit_rate_pct"]),
    ("狂战士固伤-独立攻击", abs(berserker_fixed_ind * 100 - 8.0) < 0.01, round(berserker_fixed_ind * 100, 4)),
    ("狂战士固伤-暴击", abs(berserker_fixed_crit * 100 - 1.18) < 0.02, round(berserker_fixed_crit * 100, 4)),
    ("狂战士固伤综合", abs(berserker_fixed_combined * 100 - 9.27) < 0.01, round(berserker_fixed_combined * 100, 2)),
    ("狂战士百分比-力量", abs(berserker_pct_str * 100 - 24.42) < 0.01, round(berserker_pct_str * 100, 2)),
    ("狂战士百分比-物理攻击", abs(berserker_pct_phys * 100 - 5.5) < 0.01, round(berserker_pct_phys * 100, 2)),
    ("狂战士百分比-暴击", abs(berserker_pct_crit * 100 - 1.18) < 0.02, round(berserker_pct_crit * 100, 4)),
    ("狂战士百分比综合", abs(berserker_pct_combined * 100 - 32.81) < 0.01, round(berserker_pct_combined * 100, 2)),
    ("剑魂百分比-力量", abs(swordsman_pct_str * 100 - 36.47) < 0.01, round(swordsman_pct_str * 100, 2)),
    ("剑魂百分比-物理攻击", abs(swordsman_pct_phys * 100 - 5.5) < 0.01, round(swordsman_pct_phys * 100, 2)),
    ("剑魂百分比-暴击", abs(swordsman_pct_crit * 100 - 1.2) < 0.02, round(swordsman_pct_crit * 100, 4)),
    ("剑魂百分比综合", abs(swordsman_pct_combined * 100 - 45.70) < 0.01, round(swordsman_pct_combined * 100, 2)),
    ("边际对偶", abs(marginal_duality - 4.929881) < 0.01, round(marginal_duality, 6)),
]

pass_count = sum(1 for c in checks if c[1])
total = len(checks)

print(f"{'验证项':<28} {'状态':<6} {'计算值'}")
print("-" * 55)
for name, passed, val in checks:
    status = "✅" if passed else "❌"
    print(f"  {status} {name:<24} {val}")

print(f"\n{'='*55}")
print(f"验证结果: {pass_count}/{total} 通过")
print(f"狂战士固伤综合: {berserker_fixed_combined*100:.2f}%")
print(f"狂战士百分比综合: {berserker_pct_combined*100:.2f}%")
print(f"剑魂百分比综合: {swordsman_pct_combined*100:.2f}%")
print(f"边际对偶: {marginal_duality:.6f}")

# ========== 输出JSON ==========
output = {
    "version": "v1190",
    "timestamp": "2026-07-02 03:50 CST",
    "cc_set": CC_SET,
    "berserker_base": BERSERKER_BASE,
    "swordsman_base": SWORDSMAN_BASE,
    "berserker": {
        "fixed": {
            "independent_bonus_pct": round(berserker_fixed_ind * 100, 4),
            "crit_bonus_pct": round(berserker_fixed_crit * 100, 4),
            "combined_pct": round(berserker_fixed_combined * 100, 2)
        },
        "percentage": {
            "strength_bonus_pct": round(berserker_pct_str * 100, 2),
            "physical_attack_bonus_pct": round(berserker_pct_phys * 100, 2),
            "crit_bonus_pct": round(berserker_pct_crit * 100, 4),
            "combined_pct": round(berserker_pct_combined * 100, 2)
        }
    },
    "swordsman": {
        "percentage": {
            "strength_bonus_pct": round(swordsman_pct_str * 100, 2),
            "physical_attack_bonus_pct": round(swordsman_pct_phys * 100, 2),
            "crit_bonus_pct": round(swordsman_pct_crit * 100, 4),
            "combined_pct": round(swordsman_pct_combined * 100, 2)
        }
    },
    "marginal_duality": round(marginal_duality, 6),
    "expected": {
        "berserker_fixed": 9.27,
        "berserker_pct": 32.81,
        "swordsman_pct": 45.70,
        "marginal_duality": 4.929881
    },
    "verification": {
        "pass_count": pass_count,
        "total": total,
        "all_passed": pass_count == total
    }
}

outpath = "/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verification-cc-bonus-v1190.json"
with open(outpath, "w") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nJSON saved: {outpath}")
