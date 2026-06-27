#!/usr/bin/env python3
"""
任务19 CC套（宫廷套装）各职业加成数值 — 稳态核查 v630
验算时间：2026-06-27 16:04
使用HTML报告中的精确基准值
"""
import json, datetime

results = {}

# ===== 1. CC套6件套属性合计 =====
str_total = 55+55+50+50+50+50
results['力量合计'] = {'expected': 310, 'actual': str_total, 'pass': str_total == 310}

phy_total = 20+20+18+18+18+16
results['物理攻击合计'] = {'expected': 110, 'actual': phy_total, 'pass': phy_total == 110}

ind_total = 20+20+18+18+18+26
results['独立攻击合计'] = {'expected': 120, 'actual': ind_total, 'pass': ind_total == 120}

crit_total = 0.5 * 6
results['暴击率合计'] = {'expected': 3.0, 'actual': crit_total, 'pass': crit_total == 3.0}

# ===== 2. 狂战士固伤收益 =====
# 基准：独立攻击1250, 暴击率55%
berserker_ind_base = 1250
berserker_crit_base = 0.55

# 独立攻击收益 = (1+(1250+120)/250)/(1+1250/250)-1
ind_benefit = (1 + (berserker_ind_base + 120) / 250) / (1 + berserker_ind_base / 250) - 1
results['狂战士独立攻击收益'] = {'expected': 0.08, 'actual': round(ind_benefit, 6), 'pass': abs(ind_benefit - 0.08) < 0.001}

# 暴击收益（期望伤害系数）
# 期望伤害系数 = 1 - 暴击率 + 暴击率 × 1.5 = 1 + 暴击率 × 0.5
crit_coeff_old = 1 + berserker_crit_base * 0.5  # 1.275
crit_coeff_new = 1 + (berserker_crit_base + 0.03) * 0.5  # 1.29
crit_benefit = crit_coeff_new / crit_coeff_old - 1  # 1.29/1.275-1 = 0.011765
results['狂战士暴击收益'] = {'expected': 0.011765, 'actual': round(crit_benefit, 6), 'pass': abs(crit_benefit - 0.011765) < 0.001}

# 固伤综合 = (1+独立收益)*(1+暴击收益)-1
fixed_total = (1 + ind_benefit) * (1 + crit_benefit) - 1
results['狂战士固伤综合'] = {'expected': 0.0927, 'actual': round(fixed_total, 6), 'pass': abs(fixed_total - 0.0927) < 0.001}

# ===== 3. 狂战士百分比收益 =====
# 基准：暴走后力量1019.2, 物理攻击2000, 暴击率55%
berserker_str_buff = 1019.2
berserker_phy_base = 2000

str_benefit = (1 + (berserker_str_buff + 310) / 250) / (1 + berserker_str_buff / 250) - 1
results['狂战士力量收益'] = {'expected': 0.2442, 'actual': round(str_benefit, 6), 'pass': abs(str_benefit - 0.2442) < 0.001}

phy_benefit = (berserker_phy_base + 110) / berserker_phy_base - 1
results['狂战士物理攻击收益'] = {'expected': 0.055, 'actual': round(phy_benefit, 6), 'pass': abs(phy_benefit - 0.055) < 0.001}

percent_total = (1 + str_benefit) * (1 + phy_benefit) * (1 + crit_benefit) - 1
results['狂战士百分比综合'] = {'expected': 0.3281, 'actual': round(percent_total, 6), 'pass': abs(percent_total - 0.3281) < 0.001}

# ===== 4. 剑魂百分比收益 =====
# 基准：力量600, 物理攻击2600(破极后), 暴击率50%
swordsman_str_base = 600
swordsman_phy_buff = 2600
swordsman_crit_base = 0.50

sw_str_benefit = (1 + (swordsman_str_base + 310) / 250) / (1 + swordsman_str_base / 250) - 1
results['剑魂力量收益'] = {'expected': 0.3647, 'actual': round(sw_str_benefit, 6), 'pass': abs(sw_str_benefit - 0.3647) < 0.001}

sw_phy_benefit = (swordsman_phy_buff + 110) / swordsman_phy_buff - 1
results['剑魂物理攻击收益'] = {'expected': 0.0423, 'actual': round(sw_phy_benefit, 6), 'pass': abs(sw_phy_benefit - 0.0423) < 0.001}

sw_crit_coeff_old = 1 + swordsman_crit_base * 0.5  # 1.25
sw_crit_coeff_new = 1 + (swordsman_crit_base + 0.03) * 0.5  # 1.265
sw_crit_benefit = sw_crit_coeff_new / sw_crit_coeff_old - 1  # 1.265/1.25-1 = 0.012
results['剑魂暴击收益'] = {'expected': 0.012, 'actual': round(sw_crit_benefit, 6), 'pass': abs(sw_crit_benefit - 0.012) < 0.001}

sw_percent_total = (1 + sw_str_benefit) * (1 + sw_phy_benefit) * (1 + sw_crit_benefit) - 1
results['剑魂百分比综合'] = {'expected': 0.4395, 'actual': round(sw_percent_total, 6), 'pass': abs(sw_percent_total - 0.4395) < 0.001}

# ===== 5. 边际对偶验证 =====
marginal_duality = sw_percent_total / fixed_total if fixed_total != 0 else 0
results['边际对偶'] = {'expected': 4.740937, 'actual': round(marginal_duality, 6), 'pass': abs(marginal_duality - 4.740937) < 0.001}

# ===== 汇总 =====
pass_count = sum(1 for v in results.values() if v['pass'])
total_count = len(results)
all_pass = (pass_count == total_count)

summary = {
    'task': '任务19 - CC套（宫廷套装）各职业加成数值',
    'version': 'v630',
    'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'total_checks': total_count,
    'pass_count': pass_count,
    'fail_count': total_count - pass_count,
    'pass_rate': f'{pass_count}/{total_count} ({100*pass_count/total_count:.1f}%)',
    'all_pass': all_pass,
    'core_data': {
        'cc_6pc_stats': f'力量+{str_total}/物理攻击+{phy_total}/独立攻击+{ind_total}/暴击+{crit_total}%',
        'berserker_fixed': f'+{fixed_total*100:.2f}%',
        'berserker_percent': f'+{percent_total*100:.2f}%',
        'swordsman_percent': f'+{sw_percent_total*100:.2f}%',
        'marginal_duality': f'{marginal_duality:.6f}x'
    },
    'details': results
}

print(json.dumps(summary, ensure_ascii=False, indent=2))

with open('/root/.openclaw/workspace/game-damage-research/notes/bonus-system/verifications/verification-cc-bonus-v630-2026-06-27.json', 'w') as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print(f"\n✅ 验算完成: {pass_count}/{total_count} 通过")
print(f"📊 核心数据: CC套6件(力量+{str_total}/物理攻击+{phy_total}/独立攻击+{ind_total}/暴击+{crit_total}%)")
print(f"📊 狂战士固伤+{fixed_total*100:.2f}% / 百分比+{percent_total*100:.2f}% / 剑魂百分比+{sw_percent_total*100:.2f}%")
print(f"🔬 边际对偶: {marginal_duality:.6f}x")
