#!/usr/bin/env python3
"""CC套（宫廷套装）v1301 稳态核查 - Python独立验算
基于v1267验证公式（15/15通过）
公式约定:
  - 独立攻击收益 = (1 + (ind+cc_ind)/250) / (1 + ind/250) - 1
  - 力量收益 = (1 + (str+cc_str)/250) / (1 + str/250) - 1
  - 物理攻击收益 = (phy+cc_phy)/phy - 1
  - 暴击收益 = 期望伤害系数公式: (1-crit+crit*1.5)
  - 综合 = 各乘区乘积 - 1
  - 边际对偶 = 剑魂百分比综合 / 狂战士固伤综合
"""
import json
from datetime import datetime

# === CC套核心数据 ===
cc = {"strength": 310, "p_atk": 110, "i_atk": 120, "crit": 0.03}

# === 基础面板（v808修正值） ===
berserker_fixed = {"ind": 1250, "crit": 0.55}
berserker_pct = {"str": 1019.2, "phy": 2000, "crit": 0.55}
swordsman = {"str": 600, "phy": 2000, "crit": 0.50}

# === 期望值 ===
EXPECTED = {
    "狂战士固伤综合": 9.27,
    "狂战士百分比综合": 32.81,
    "剑魂百分比综合": 45.70,
    "边际对偶": 4.930020,
}

R = []

# 1. 6件套属性合计
for name, k, exp in [("力量","strength",310),("物攻","p_atk",110),("独攻","i_atk",120),("暴击%","crit",0.03)]:
    R.append({"check":f"CC套{name}","expected":exp,"actual":cc[k],"passed":abs(cc[k]-exp)<0.001})

# 2. 狂战士固伤收益
b_ind_before = 1 + berserker_fixed["ind"]/250
b_ind_after = 1 + (berserker_fixed["ind"] + cc["i_atk"])/250
b_ind_bonus = b_ind_after / b_ind_before - 1

b_crit_exp_before = (1 - berserker_fixed["crit"]) + berserker_fixed["crit"] * 1.5
b_crit_exp_after = (1 - berserker_fixed["crit"] - cc["crit"]) + (berserker_fixed["crit"] + cc["crit"]) * 1.5
b_crit_bonus = b_crit_exp_after / b_crit_exp_before - 1

b_fixed_total = (1 + b_ind_bonus) * (1 + b_crit_bonus) - 1

R.append({"check":"狂战士-独立攻击收益","expected":8.0,"actual":round(b_ind_bonus*100,2),"passed":abs(round(b_ind_bonus*100,2)-8.0)<0.01})
R.append({"check":"狂战士-暴击收益","expected":1.18,"actual":round(b_crit_bonus*100,2),"passed":abs(round(b_crit_bonus*100,2)-1.18)<0.01})
R.append({"check":"狂战士-固伤综合","expected":EXPECTED["狂战士固伤综合"],"actual":round(b_fixed_total*100,2),"passed":abs(round(b_fixed_total*100,2)-EXPECTED["狂战士固伤综合"])<0.05})

# 3. 狂战士百分比收益
b_str_before = 1 + berserker_pct["str"]/250
b_str_after = 1 + (berserker_pct["str"] + cc["strength"])/250
b_str_bonus = b_str_after / b_str_before - 1

b_phy_bonus = (berserker_pct["phy"] + cc["p_atk"]) / berserker_pct["phy"] - 1

b_crit_exp_before2 = (1 - berserker_pct["crit"]) + berserker_pct["crit"] * 1.5
b_crit_exp_after2 = (1 - berserker_pct["crit"] - cc["crit"]) + (berserker_pct["crit"] + cc["crit"]) * 1.5
b_crit_bonus2 = b_crit_exp_after2 / b_crit_exp_before2 - 1

b_pct_total = (1 + b_str_bonus) * (1 + b_phy_bonus) * (1 + b_crit_bonus2) - 1

R.append({"check":"狂战士-力量收益","expected":24.42,"actual":round(b_str_bonus*100,2),"passed":abs(round(b_str_bonus*100,2)-24.42)<0.01})
R.append({"check":"狂战士-物理攻击收益","expected":5.5,"actual":round(b_phy_bonus*100,2),"passed":abs(round(b_phy_bonus*100,2)-5.5)<0.01})
R.append({"check":"狂战士-百分比综合","expected":EXPECTED["狂战士百分比综合"],"actual":round(b_pct_total*100,2),"passed":abs(round(b_pct_total*100,2)-EXPECTED["狂战士百分比综合"])<0.05})

# 4. 剑魂百分比收益
s_str_before = 1 + swordsman["str"]/250
s_str_after = 1 + (swordsman["str"] + cc["strength"])/250
s_str_bonus = s_str_after / s_str_before - 1

s_phy_bonus = (swordsman["phy"] + cc["p_atk"]) / swordsman["phy"] - 1

s_crit_exp_before = (1 - swordsman["crit"]) + swordsman["crit"] * 1.5
s_crit_exp_after = (1 - swordsman["crit"] - cc["crit"]) + (swordsman["crit"] + cc["crit"]) * 1.5
s_crit_bonus = s_crit_exp_after / s_crit_exp_before - 1

s_pct_total = (1 + s_str_bonus) * (1 + s_phy_bonus) * (1 + s_crit_bonus) - 1

R.append({"check":"剑魂-力量收益","expected":36.47,"actual":round(s_str_bonus*100,2),"passed":abs(round(s_str_bonus*100,2)-36.47)<0.01})
R.append({"check":"剑魂-物理攻击收益","expected":5.5,"actual":round(s_phy_bonus*100,2),"passed":abs(round(s_phy_bonus*100,2)-5.5)<0.01})
R.append({"check":"剑魂-暴击收益","expected":1.2,"actual":round(s_crit_bonus*100,2),"passed":abs(round(s_crit_bonus*100,2)-1.2)<0.01})
R.append({"check":"剑魂-百分比综合","expected":EXPECTED["剑魂百分比综合"],"actual":round(s_pct_total*100,2),"passed":abs(round(s_pct_total*100,2)-EXPECTED["剑魂百分比综合"])<0.05})

# 5. 边际对偶
marginal_duality = s_pct_total / b_fixed_total
R.append({"check":"边际对偶倍数","expected":EXPECTED["边际对偶"],"actual":round(marginal_duality,6),"passed":abs(round(marginal_duality,6)-EXPECTED["边际对偶"])<0.001})

passed = sum(1 for r in R if r["passed"])
total = len(R)

summary = {
    "version":"v1301","timestamp":datetime.now().strftime("%Y-%m-%d %H:%M CST"),
    "results":R,"passed":passed,"total":total,"all_passed":passed==total,
    "cc_set":cc,
    "berserker":{
        "fixed":{"independent_bonus_pct":round(b_ind_bonus*100,2),"crit_bonus_pct":round(b_crit_bonus*100,2),"combined_pct":round(b_fixed_total*100,2)},
        "percentage":{"strength_bonus_pct":round(b_str_bonus*100,2),"physical_attack_bonus_pct":round(b_phy_bonus*100,2),"crit_bonus_pct":round(b_crit_bonus2*100,2),"combined_pct":round(b_pct_total*100,2)}
    },
    "swordsman":{
        "percentage":{"strength_bonus_pct":round(s_str_bonus*100,2),"physical_attack_bonus_pct":round(s_phy_bonus*100,2),"crit_bonus_pct":round(s_crit_bonus*100,2),"combined_pct":round(s_pct_total*100,2)}
    },
    "marginal_duality":round(marginal_duality,6),"expected_marginal_duality":EXPECTED["边际对偶"]
}

print(json.dumps(summary,ensure_ascii=False,indent=2))
with open("notes/bonus-system/verification-cc-bonus-v1301.json","w") as f:
    json.dump(summary,f,ensure_ascii=False,indent=2)
print(f"\n✅ v1301: {passed}/{total} 通过")
