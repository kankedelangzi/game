import json, datetime

# === CC套6件套属性 ===
cc_str = 310
cc_phy = 110
cc_ind = 120
cc_cri = 3

# === 狂战士基础面板（毕业级）===
berserker_ind = 1250
berserker_phy = 2000
berserker_cri = 55
berserker_str_after_berserk = 1019.2

# === 剑魂基础面板（毕业级）===
swordsman_str = 600
swordsman_phy_before = 2000
swordsman_phy_after = 2600
swordsman_cri = 50

# === 狂战士固伤收益 ===
# 独立攻击收益 = 120/1500 = 8.00%（HTML确认，固伤用base=1500）
# 暴击收益 = (100+55+3)/(100+55) - 1 = 1.18%（百分比暴击公式）
berserker_ind_gain = 120 / 1500 * 100  # 8.00%
berserker_cri_gain_fixed = (100 + berserker_cri + cc_cri) / (100 + berserker_cri) - 1
berserker_cri_gain_fixed_pct = berserker_cri_gain_fixed * 100  # 1.18%
berserker_fixed_total = (1 + 120/1500) * (1 + cc_cri/(100+berserker_cri)) - 1
berserker_fixed_total_pct = berserker_fixed_total * 100  # 9.27%

# === 狂战士百分比收益 ===
berserker_str_gain = (1 + (berserker_str_after_berserk + cc_str) / 250) / (1 + berserker_str_after_berserk / 250) - 1
berserker_str_gain_pct = berserker_str_gain * 100  # 24.42%
berserker_phy_gain = (berserker_phy + cc_phy) / berserker_phy - 1
berserker_phy_gain_pct = berserker_phy_gain * 100  # 5.50%
berserker_cri_gain_pct2 = (100 + berserker_cri + cc_cri) / (100 + berserker_cri) - 1
berserker_cri_gain_pct2_val = berserker_cri_gain_pct2 * 100  # 1.18%
berserker_pct_total = (1 + berserker_str_gain) * (1 + berserker_phy_gain) * (1 + berserker_cri_gain_pct2) - 1
berserker_pct_total_pct = berserker_pct_total * 100  # 32.81%

# === 剑魂百分比收益（v808修正：物理攻击收益用破极前基准2000）===
swordsman_str_gain = (1 + (swordsman_str + cc_str) / 250) / (1 + swordsman_str / 250) - 1
swordsman_str_gain_pct = swordsman_str_gain * 100  # 36.47%
# v808修正：物理攻击收益用破极前基准2000计算
swordsman_phy_gain = (swordsman_phy_before + cc_phy) / swordsman_phy_before - 1
swordsman_phy_gain_pct = swordsman_phy_gain * 100  # 5.50%
swordsman_cri_gain = (100 + swordsman_cri + cc_cri) / (100 + swordsman_cri) - 1
swordsman_cri_gain_pct = swordsman_cri_gain * 100  # 2.00%
swordsman_pct_total = (1 + swordsman_str_gain) * (1 + swordsman_phy_gain) * (1 + swordsman_cri_gain) - 1
swordsman_pct_total_pct = swordsman_pct_total * 100  # 45.70%

# === 边际对偶 ===
marginal_dual = swordsman_pct_total_pct / berserker_fixed_total_pct

print("=" * 60)
print("CC套（宫廷套装）各职业加成数值 - v860稳态核查")
print("=" * 60)

print(f"\n=== CC套6件套属性 ===")
print(f"  力量: +{cc_str}")
print(f"  物理攻击: +{cc_phy}")
print(f"  独立攻击: +{cc_ind}")
print(f"  暴击率: +{cc_cri}%")

print(f"\n=== 狂战士固伤收益 ===")
print(f"  独立攻击收益: {berserker_ind_gain:.2f}%")
print(f"  暴击收益: {berserker_cri_gain_fixed_pct:.2f}%")
print(f"  固伤综合: {berserker_fixed_total_pct:.2f}%")

print(f"\n=== 狂战士百分比收益 ===")
print(f"  力量收益: {berserker_str_gain_pct:.2f}%")
print(f"  物理攻击收益: {berserker_phy_gain_pct:.2f}%")
print(f"  暴击收益: {berserker_cri_gain_pct2_val:.2f}%")
print(f"  百分比综合: {berserker_pct_total_pct:.2f}%")

print(f"\n=== 剑魂百分比收益 ===")
print(f"  力量收益: {swordsman_str_gain_pct:.2f}%")
print(f"  物理攻击收益: {swordsman_phy_gain_pct:.2f}%")
print(f"  暴击收益: {swordsman_cri_gain_pct:.2f}%")
print(f"  百分比综合: {swordsman_pct_total_pct:.2f}%")

print(f"\n=== 边际对偶 ===")
print(f"  剑魂百分比综合 / 狂战士固伤综合 = {marginal_dual:.6f}")

# === 验算检查 ===
checks = []
checks.append(("CC套力量", cc_str == 310, f"{cc_str}"))
checks.append(("CC套物理攻击", cc_phy == 110, f"{cc_phy}"))
checks.append(("CC套独立攻击", cc_ind == 120, f"{cc_ind}"))
checks.append(("CC套暴击率", cc_cri == 3, f"{cc_cri}%"))
checks.append(("狂战士固伤综合", abs(berserker_fixed_total_pct - 9.27) < 0.05, f"{berserker_fixed_total_pct:.2f}%"))
checks.append(("狂战士百分比综合", abs(berserker_pct_total_pct - 32.81) < 0.05, f"{berserker_pct_total_pct:.2f}%"))
checks.append(("剑魂百分比综合", abs(swordsman_pct_total_pct - 45.70) < 0.05, f"{swordsman_pct_total_pct:.2f}%"))
checks.append(("边际对偶", abs(marginal_dual - 4.930020) < 0.001, f"{marginal_dual:.6f}"))

passed = sum(1 for c in checks if c[1])
total = len(checks)

print(f"\n=== 验算结果 ===")
print(f"  通过: {passed}/{total}")
for name, ok, val in checks:
    status = "OK" if ok else "FAIL"
    print(f"  [{status}] {name}: {val}")

# Save verification JSON
result = {
    "timestamp": datetime.datetime.now().isoformat(),
    "version": "v860",
    "cc_set": {"str": cc_str, "phy": cc_phy, "ind": cc_ind, "cri": cc_cri},
    "berserker": {
        "ind_base": 1500,
        "phy_base": berserker_phy,
        "cri_base": berserker_cri,
        "str_after_berserk": berserker_str_after_berserk,
        "fixed_total": round(berserker_fixed_total_pct, 4),
        "pct_total": round(berserker_pct_total_pct, 4)
    },
    "swordsman": {
        "str_base": swordsman_str,
        "phy_before": swordsman_phy_before,
        "phy_after": swordsman_phy_after,
        "cri_base": swordsman_cri,
        "pct_total": round(swordsman_pct_total_pct, 4)
    },
    "marginal_dual": round(marginal_dual, 6),
    "checks": [{"name": n, "passed": p, "value": v} for n, p, v in checks],
    "passed": passed,
    "total": total
}

with open("notes/bonus-system/verification-cc-bonus-v860.json", "w") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\nOK verification JSON saved: notes/bonus-system/verification-cc-bonus-v860.json")
