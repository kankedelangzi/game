#!/usr/bin/env python3
"""CC套（宫廷套装）v1190 稳态核查 - Python独立验算
公式约定:
  - 力量% = 时装力量 / 角色基准力量 × 100
  - 百分比综合% = (1+力量%) × (1+物攻%) × (1+暴击%) - 1
  - 固伤综合% = (1+独攻%) × (1+暴击%) - 1
  - 边际对偶 = 百分比综合% / 固伤综合%
"""
import json
from datetime import datetime

cc = {"strength": 310, "p_atk": 110, "i_atk": 120, "crit": 3.0}
ber = {"str": 750, "patk": 2000, "iatk": 1500}
sw  = {"str": 810, "patk": 2000, "iatk": 1500}

R = []

# 1) 6件套属性
for name, k, exp in [("力量","strength",310),("物攻","p_atk",110),("独攻","i_atk",120),("暴击%","crit",3.0)]:
    R.append({"check":f"6件套{name}","expected":exp,"actual":cc[k],"passed":abs(cc[k]-exp)<0.01})

# 2) 狂战士固伤
ber_iatk = round(cc["i_atk"]/ber["iatk"]*100,2)
ber_crit = round(cc["crit"],2)
ber_fixed = round((1+ber_iatk/100)*(1+ber_crit/100)-1,4)*100
R.append({"check":"狂战士-固伤独攻%","expected":8.0,"actual":ber_iatk,"passed":abs(ber_iatk-8.0)<0.01})
R.append({"check":"狂战士-固伤暴击%","expected":3.0,"actual":ber_crit,"passed":abs(ber_crit-3.0)<0.01})
R.append({"check":"狂战士-固伤综合%","expected":9.27,"actual":round(ber_fixed,2),"passed":abs(round(ber_fixed,2)-9.27)<0.1})

# 3) 狂战士百分比
ber_str = round(cc["strength"]/ber["str"]*100,2)
ber_patk = round(cc["p_atk"]/ber["patk"]*100,2)
ber_crit2 = round(cc["crit"],2)
ber_pct = round((1+ber_str/100)*(1+ber_patk/100)*(1+ber_crit2/100)-1,4)*100
R.append({"check":"狂战士-百分比力量%","expected":41.33,"actual":ber_str,"passed":abs(ber_str-41.33)<0.01})
R.append({"check":"狂战士-百分比物攻%","expected":5.5,"actual":ber_patk,"passed":abs(ber_patk-5.5)<0.01})
R.append({"check":"狂战士-百分比综合%","expected":32.81,"actual":round(ber_pct,2),"passed":abs(round(ber_pct,2)-32.81)<0.1})

# 4) 剑魂百分比
sw_str = round(cc["strength"]/sw["str"]*100,2)
sw_patk = round(cc["p_atk"]/sw["patk"]*100,2)
sw_crit = round(cc["crit"],2)
sw_pct = round((1+sw_str/100)*(1+sw_patk/100)*(1+sw_crit/100)-1,4)*100
R.append({"check":"剑魂-百分比力量%","expected":38.27,"actual":sw_str,"passed":abs(sw_str-38.27)<0.01})
R.append({"check":"剑魂-百分比物攻%","expected":5.5,"actual":sw_patk,"passed":abs(sw_patk-5.5)<0.01})
R.append({"check":"剑魂-百分比暴击%","expected":3.0,"actual":sw_crit,"passed":abs(sw_crit-3.0)<0.01})
R.append({"check":"剑魂-百分比综合%","expected":45.70,"actual":round(sw_pct,2),"passed":abs(round(sw_pct,2)-45.70)<0.1})

# 5) 边际对偶
md = round(sw_pct/ber_fixed,6)
exp_md = 4.930020
R.append({"check":"边际对偶","expected":exp_md,"actual":round(md,6),"passed":abs(md-exp_md)<0.01})

passed = sum(1 for r in R if r["passed"])
total = len(R)

summary = {
    "version":"v1190","timestamp":datetime.now().strftime("%Y-%m-%d %H:%M CST"),
    "results":R,"passed":passed,"total":total,"all_passed":passed==total,
    "cc_set":cc,
    "berserker":{
        "fixed":{"independent_bonus_pct":ber_iatk,"crit_bonus_pct":ber_crit,"combined_pct":round(ber_fixed,2)},
        "percentage":{"strength_bonus_pct":ber_str,"physical_attack_bonus_pct":ber_patk,"crit_bonus_pct":ber_crit2,"combined_pct":round(ber_pct,2)}
    },
    "swordsman":{
        "percentage":{"strength_bonus_pct":sw_str,"physical_attack_bonus_pct":sw_patk,"crit_bonus_pct":sw_crit,"combined_pct":round(sw_pct,2)}
    },
    "marginal_duality":round(md,6),"expected_marginal_duality":exp_md
}

print(json.dumps(summary,ensure_ascii=False,indent=2))
with open("notes/bonus-system/verification-cc-bonus-v1190.json","w") as f:
    json.dump(summary,f,ensure_ascii=False,indent=2)
print(f"\n✅ v1190: {passed}/{total} 通过")
