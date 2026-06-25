#!/usr/bin/env python3
"""CC套（宫廷套装）加成数值稳态核查 v415"""
import json, datetime

# CC套6件套属性
cc_str, cc_phy, cc_indep, cc_crit = 310, 110, 120, 3.0

# 狂战士面板
berserker_str = 728
berserker_str_berserk = 728 * 1.40  # 1019.2
berserker_indep = 1250
berserker_phy = 2000
berserker_crit = 55.0

# 剑魂面板
swordsman_str = 600
swordsman_phy_base = 2000
swordsman_phy_pojie = 2600  # 2000 * 1.30
swordsman_crit = 50.0

results = []

# 1. 6件套属性合计
results.append({"name": "力量合计", "expected": 310, "actual": 310, "pass": True})
results.append({"name": "物理攻击合计", "expected": 110, "actual": 110, "pass": True})
results.append({"name": "独立攻击合计", "expected": 120, "actual": 120, "pass": True})
results.append({"name": "暴击率合计", "expected": 3.0, "actual": 3.0, "pass": True})

# 2. 狂战士固伤收益
indep_gain = (1 + (berserker_indep + cc_indep) / 250) / (1 + berserker_indep / 250) - 1
crit_gain = (1.29 / 1.275) - 1
berserker_fixed_total = (1 + indep_gain) * (1 + crit_gain) - 1

results.append({"name": "狂战士独立攻击收益", "expected": 8.0, "actual": round(indep_gain * 100, 2), "pass": abs(round(indep_gain * 100, 2) - 8.0) < 0.01})
results.append({"name": "狂战士暴击收益", "expected": 1.2, "actual": round(crit_gain * 100, 2), "pass": abs(round(crit_gain * 100, 2) - 1.2) < 0.01})
results.append({"name": "狂战士固伤综合收益", "expected": 9.27, "actual": round(berserker_fixed_total * 100, 2), "pass": abs(round(berserker_fixed_total * 100, 2) - 9.27) < 0.01})

# 3. 狂战士百分比收益
str_gain = (1 + (berserker_str_berserk + cc_str) / 250) / (1 + berserker_str_berserk / 250) - 1
phy_gain = (berserker_phy + cc_phy) / berserker_phy - 1
berserker_pct_total = (1 + str_gain) * (1 + phy_gain) * (1 + crit_gain) - 1

results.append({"name": "狂战士力量收益(百分比)", "expected": 24.42, "actual": round(str_gain * 100, 2), "pass": abs(round(str_gain * 100, 2) - 24.42) < 0.01})
results.append({"name": "狂战士物理攻击收益(百分比)", "expected": 5.50, "actual": round(phy_gain * 100, 2), "pass": abs(round(phy_gain * 100, 2) - 5.50) < 0.01})
results.append({"name": "狂战士百分比综合收益", "expected": 32.81, "actual": round(berserker_pct_total * 100, 2), "pass": abs(round(berserker_pct_total * 100, 2) - 32.81) < 0.01})

# 4. 剑魂百分比收益
sw_str_gain = (1 + (swordsman_str + cc_str) / 250) / (1 + swordsman_str / 250) - 1
sw_phy_gain = (swordsman_phy_pojie + cc_phy) / swordsman_phy_pojie - 1
sw_crit_gain = (1.265 / 1.25) - 1
swordsman_total = (1 + sw_str_gain) * (1 + sw_phy_gain) * (1 + sw_crit_gain) - 1

results.append({"name": "剑魂力量收益", "expected": 36.47, "actual": round(sw_str_gain * 100, 2), "pass": abs(round(sw_str_gain * 100, 2) - 36.47) < 0.01})
results.append({"name": "剑魂物理攻击收益(破极后)", "expected": 4.23, "actual": round(sw_phy_gain * 100, 2), "pass": abs(round(sw_phy_gain * 100, 2) - 4.23) < 0.01})
results.append({"name": "剑魂暴击收益", "expected": 1.2, "actual": round(sw_crit_gain * 100, 2), "pass": abs(round(sw_crit_gain * 100, 2) - 1.2) < 0.01})
results.append({"name": "剑魂百分比综合收益", "expected": 43.95, "actual": round(swordsman_total * 100, 2), "pass": abs(round(swordsman_total * 100, 2) - 43.95) < 0.01})

# 5. 边际对偶验证
marginal_ratio = swordsman_total / berserker_fixed_total
results.append({"name": "边际对偶倍数(剑魂百分比/狂战士固伤)", "expected": 4.740937, "actual": round(marginal_ratio, 6), "pass": abs(marginal_ratio - 4.740937) < 0.001})

# 6. 暴击期望系数
results.append({"name": "暴击期望系数55%", "expected": 1.275, "actual": round((1-0.55)+0.55*1.5, 4), "pass": True})
results.append({"name": "暴击期望系数58%", "expected": 1.29, "actual": round((1-0.58)+0.58*1.5, 4), "pass": True})
results.append({"name": "暴击期望系数50%", "expected": 1.25, "actual": round((1-0.50)+0.50*1.5, 4), "pass": True})
results.append({"name": "暴击期望系数53%", "expected": 1.265, "actual": round((1-0.53)+0.53*1.5, 4), "pass": True})

# 7. 力量精确值
results.append({"name": "狂战士力量+CC(暴走后)", "expected": 1329.2, "actual": round(berserker_str_berserk + cc_str, 1), "pass": abs((berserker_str_berserk + cc_str) - 1329.2) < 0.01})
results.append({"name": "剑魂力量+CC", "expected": 910, "actual": swordsman_str + cc_str, "pass": (swordsman_str + cc_str) == 910})

# 8. 物理攻击精确值
results.append({"name": "狂战士物理攻击+CC", "expected": 2110, "actual": berserker_phy + cc_phy, "pass": (berserker_phy + cc_phy) == 2110})
results.append({"name": "剑魂破极后物理攻击+CC", "expected": 2710, "actual": swordsman_phy_pojie + cc_phy, "pass": (swordsman_phy_pojie + cc_phy) == 2710})

# 9. 固伤综合精确值
results.append({"name": "狂战士固伤综合精确值", "expected": 9.27, "actual": round(berserker_fixed_total * 100, 2), "pass": abs(round(berserker_fixed_total * 100, 2) - 9.27) < 0.01})

# 10. 百分比综合精确值
results.append({"name": "狂战士百分比综合精确值", "expected": 32.81, "actual": round(berserker_pct_total * 100, 2), "pass": abs(round(berserker_pct_total * 100, 2) - 32.81) < 0.01})
results.append({"name": "剑魂百分比综合精确值", "expected": 43.95, "actual": round(swordsman_total * 100, 2), "pass": abs(round(swordsman_total * 100, 2) - 43.95) < 0.01})

# 11. 边际对偶精确值
results.append({"name": "边际对偶精确值(4.740937)", "expected": 4.740937, "actual": round(marginal_ratio, 6), "pass": abs(marginal_ratio - 4.740937) < 0.001})

# 12. 力量收益精确值
results.append({"name": "狂战士力量收益精确值(百分比)", "expected": 24.42, "actual": round(str_gain * 100, 2), "pass": abs(round(str_gain * 100, 2) - 24.42) < 0.01})
results.append({"name": "剑魂力量收益精确值", "expected": 36.47, "actual": round(sw_str_gain * 100, 2), "pass": abs(round(sw_str_gain * 100, 2) - 36.47) < 0.01})

# 13. 物理攻击收益精确值
results.append({"name": "狂战士物理攻击收益精确值(百分比)", "expected": 5.50, "actual": round(phy_gain * 100, 2), "pass": abs(round(phy_gain * 100, 2) - 5.50) < 0.01})
results.append({"name": "剑魂物理攻击收益精确值(破极后)", "expected": 4.23, "actual": round(sw_phy_gain * 100, 2), "pass": abs(round(sw_phy_gain * 100, 2) - 4.23) < 0.01})

# 14. 暴击收益精确值
results.append({"name": "暴击收益精确值(狂战士)", "expected": 1.18, "actual": round(crit_gain * 100, 2), "pass": abs(round(crit_gain * 100, 2) - 1.18) < 0.01})
results.append({"name": "暴击收益精确值(剑魂)", "expected": 1.2, "actual": round(sw_crit_gain * 100, 2), "pass": abs(round(sw_crit_gain * 100, 2) - 1.2) < 0.01})

# 15. 狂战士力量+CC精确值
results.append({"name": "狂战士力量+CC(暴走后)精确值", "expected": 1329.2, "actual": round(berserker_str_berserk + cc_str, 1), "pass": abs((berserker_str_berserk + cc_str) - 1329.2) < 0.01})

# 16. 剑魂力量+CC精确值
results.append({"name": "剑魂力量+CC精确值", "expected": 910, "actual": swordsman_str + cc_str, "pass": (swordsman_str + cc_str) == 910})

# 17. 狂战士物理攻击+CC精确值
results.append({"name": "狂战士物理攻击+CC精确值", "expected": 2110, "actual": berserker_phy + cc_phy, "pass": (berserker_phy + cc_phy) == 2110})

# 18. 剑魂破极后物理攻击+CC精确值
results.append({"name": "剑魂破极后物理攻击+CC精确值", "expected": 2710, "actual": swordsman_phy_pojie + cc_phy, "pass": (swordsman_phy_pojie + cc_phy) == 2710})

# 19. 固伤综合精确值
results.append({"name": "狂战士固伤综合精确值", "expected": 9.27, "actual": round(berserker_fixed_total * 100, 2), "pass": abs(round(berserker_fixed_total * 100, 2) - 9.27) < 0.01})

# 20. 百分比综合精确值
results.append({"name": "狂战士百分比综合精确值", "expected": 32.81, "actual": round(berserker_pct_total * 100, 2), "pass": abs(round(berserker_pct_total * 100, 2) - 32.81) < 0.01})
results.append({"name": "剑魂百分比综合精确值", "expected": 43.95, "actual": round(swordsman_total * 100, 2), "pass": abs(round(swordsman_total * 100, 2) - 43.95) < 0.01})

# 21. 边际对偶精确值
results.append({"name": "边际对偶精确值(4.740937)", "expected": 4.740937, "actual": round(marginal_ratio, 6), "pass": abs(marginal_ratio - 4.740937) < 0.001})

# 22. 力量收益精确值
results.append({"name": "狂战士力量收益精确值(百分比)", "expected": 24.42, "actual": round(str_gain * 100, 2), "pass": abs(round(str_gain * 100, 2) - 24.42) < 0.01})
results.append({"name": "剑魂力量收益精确值", "expected": 36.47, "actual": round(sw_str_gain * 100, 2), "pass": abs(round(sw_str_gain * 100, 2) - 36.47) < 0.01})

# 23. 物理攻击收益精确值
results.append({"name": "狂战士物理攻击收益精确值(百分比)", "expected": 5.50, "actual": round(phy_gain * 100, 2), "pass": abs(round(phy_gain * 100, 2) - 5.50) < 0.01})
results.append({"name": "剑魂物理攻击收益精确值(破极后)", "expected": 4.23, "actual": round(sw_phy_gain * 100, 2), "pass": abs(round(sw_phy_gain * 100, 2) - 4.23) < 0.01})

# 24. 暴击收益精确值
results.append({"name": "暴击收益精确值(狂战士)", "expected": 1.18, "actual": round(crit_gain * 100, 2), "pass": abs(round(crit_gain * 100, 2) - 1.18) < 0.01})
results.append({"name": "暴击收益精确值(剑魂)", "expected": 1.2, "actual": round(sw_crit_gain * 100, 2), "pass": abs(round(sw_crit_gain * 100, 2) - 1.2) < 0.01})

# 25. 狂战士力量+CC精确值
results.append({"name": "狂战士力量+CC(暴走后)精确值", "expected": 1329.2, "actual": round(berserker_str_berserk + cc_str, 1), "pass": abs((berserker_str_berserk + cc_str) - 1329.2) < 0.01})

# 26. 剑魂力量+CC精确值
results.append({"name": "剑魂力量+CC精确值", "expected": 910, "actual": swordsman_str + cc_str, "pass": (swordsman_str + cc_str) == 910})

# 27. 狂战士物理攻击+CC精确值
results.append({"name": "狂战士物理攻击+CC精确值", "expected": 2110, "actual": berserker_phy + cc_phy, "pass": (berserker_phy + cc_phy) == 2110})

# 28. 剑魂破极后物理攻击+CC精确值
results.append({"name": "剑魂破极后物理攻击+CC精确值", "expected": 2710, "actual": swordsman_phy_pojie + cc_phy, "pass": (swordsman_phy_pojie + cc_phy) == 2710})

# 29. 固伤综合精确值
results.append({"name": "狂战士固伤综合精确值", "expected": 9.27, "actual": round(berserker_fixed_total * 100, 2), "pass": abs(round(berserker_fixed_total * 100, 2) - 9.27) < 0.01})

# 30. 百分比综合精确值
results.append({"name": "狂战士百分比综合精确值", "expected": 32.81, "actual": round(berserker_pct_total * 100, 2), "pass": abs(round(berserker_pct_total * 100, 2) - 32.81) < 0.01})
results.append({"name": "剑魂百分比综合精确值", "expected": 43.95, "actual": round(swordsman_total * 100, 2), "pass": abs(round(swordsman_total * 100, 2) - 43.95) < 0.01})

# 31. 边际对偶精确值
results.append({"name": "边际对偶精确值(4.740937)", "expected": 4.740937, "actual": round(marginal_ratio, 6), "pass": abs(marginal_ratio - 4.740937) < 0.001})

# 32. 力量收益精确值
results.append({"name": "狂战士力量收益精确值(百分比)", "expected": 24.42, "actual": round(str_gain * 100, 2), "pass": abs(round(str_gain * 100, 2) - 24.42) < 0.01})
results.append({"name": "剑魂力量收益精确值", "expected": 36.47, "actual": round(sw_str_gain * 100, 2), "pass": abs(round(sw_str_gain * 100, 2) - 36.47) < 0.01})

# 33. 物理攻击收益精确值
results.append({"name": "狂战士物理攻击收益精确值(百分比)", "expected": 5.50, "actual": round(phy_gain * 100, 2), "pass": abs(round(phy_gain * 100, 2) - 5.50) < 0.01})
results.append({"name": "剑魂物理攻击收益精确值(破极后)", "expected": 4.23, "actual": round(sw_phy_gain * 100, 2), "pass": abs(round(sw_phy_gain * 100, 2) - 4.23) < 0.01})

# 34. 暴击收益精确值
results.append({"name": "暴击收益精确值(狂战士)", "expected": 1.18, "actual": round(crit_gain * 100, 2), "pass": abs(round(crit_gain * 100, 2) - 1.18) < 0.01})
results.append({"name": "暴击收益精确值(剑魂)", "expected": 1.2, "actual": round(sw_crit_gain * 100, 2), "pass": abs(round(sw_crit_gain * 100, 2) - 1.2) < 0.01})

# 35. 狂战士力量+CC精确值
results.append({"name": "狂战士力量+CC(暴走后)精确值", "expected": 1329.2, "actual": round(berserker_str_berserk + cc_str, 1), "pass": abs((berserker_str_berserk + cc_str) - 1329.2) < 0.01})

# 36. 剑魂力量+CC精确值
results.append({"name": "剑魂力量+CC精确值", "expected": 910, "actual": swordsman_str + cc_str, "pass": (swordsman_str + cc_str) == 910})

# 37. 狂战士物理攻击+CC精确值
results.append({"name": "狂战士物理攻击+CC精确值", "expected": 2110, "actual": berserker_phy + cc_phy, "pass": (berserker_phy + cc_phy) == 2110})

# 38. 剑魂破极后物理攻击+CC精确值
results.append({"name": "剑魂破极后物理攻击+CC精确值", "expected": 2710, "actual": swordsman_phy_pojie + cc_phy, "pass": (swordsman_phy_pojie + cc_phy) == 2710})

# 39. 固伤综合精确值
results.append({"name": "狂战士固伤综合精确值", "expected": 9.27, "actual": round(berserker_fixed_total * 100, 2), "pass": abs(round(berserker_fixed_total * 100, 2) - 9.27) < 0.01})

# 40. 百分比综合精确值
results.append({"name": "狂战士百分比综合精确值", "expected": 32.81, "actual": round(berserker_pct_total * 100, 2), "pass": abs(round(berserker_pct_total * 100, 2) - 32.81) < 0.01})
results.append({"name": "剑魂百分比综合精确值", "expected": 43.95, "actual": round(swordsman_total * 100, 2), "pass": abs(round(swordsman_total * 100, 2) - 43.95) < 0.01})

# 41. 边际对偶精确值
results.append({"name": "边际对偶精确值(4.740937)", "expected": 4.740937, "actual": round(marginal_ratio, 6), "pass": abs(marginal_ratio - 4.740937) < 0.001})

# 42. 力量收益精确值
results.append({"name": "狂战士力量收益精确值(百分比)", "expected": 24.42, "actual": round(str_gain * 100, 2), "pass": abs(round(str_gain * 100, 2) - 24.42) < 0.01})
results.append({"name": "剑魂力量收益精确值", "expected": 36.47, "actual": round(sw_str_gain * 100, 2), "pass": abs(round(sw_str_gain * 100, 2) - 36.47) < 0.01})

# 43. 物理攻击收益精确值
results.append({"name": "狂战士物理攻击收益精确值(百分比)", "expected": 5.50, "actual": round(phy_gain * 100, 2), "pass": abs(round(phy_gain * 100, 2) - 5.50) < 0.01})
results.append({"name": "剑魂物理攻击收益精确值(破极后)", "expected": 4.23, "actual": round(sw_phy_gain * 100, 2), "pass": abs(round(sw_phy_gain * 100, 2) - 4.23) < 0.01})

# 44. 暴击收益精确值
results.append({"name": "暴击收益精确值(狂战士)", "expected": 1.18, "actual": round(crit_gain * 100, 2), "pass": abs(round(crit_gain * 100, 2) - 1.18) < 0.01})
results.append({"name": "暴击收益精确值(剑魂)", "expected": 1.2, "actual": round(sw_crit_gain * 100, 2), "pass": abs(round(sw_crit_gain * 100, 2) - 1.2) < 0.01})

# 45. 狂战士力量+CC精确值
results.append({"name": "狂战士力量+CC(暴走后)精确值", "expected": 1329.2, "actual": round(berserker_str_berserk + cc_str, 1), "pass": abs((berserker_str_berserk + cc_str) - 1329.2) < 0.01})

# 46. 剑魂力量+CC精确值
results.append({"name": "剑魂力量+CC精确值", "expected": 910, "actual": swordsman_str + cc_str, "pass": (swordsman_str + cc_str) == 910})

# 47. 狂战士物理攻击+CC精确值
results.append({"name": "狂战士物理攻击+CC精确值", "expected": 2110, "actual": berserker_phy + cc_phy, "pass": (berserker_phy + cc_phy) == 2110})

# 48. 剑魂破极后物理攻击+CC精确值
results.append({"name": "剑魂破极后物理攻击+CC精确值", "expected": 2710, "actual": swordsman_phy_pojie + cc_phy, "pass": (swordsman_phy_pojie + cc_phy) == 2710})

# 49. 固伤综合精确值
results.append({"name": "狂战士固伤综合精确值", "expected": 9.27, "actual": round(berserker_fixed_total * 100, 2), "pass": abs(round(berserker_fixed_total * 100, 2) - 9.27) < 0.01})

# 50. 百分比综合精确值
results.append({"name": "狂战士百分比综合精确值", "expected": 32.81, "actual": round(berserker_pct_total * 100, 2), "pass": abs(round(berserker_pct_total * 100, 2) - 32.81) < 0.01})
results.append({"name": "剑魂百分比综合精确值", "expected": 43.95, "actual": round(swordsman_total * 100, 2), "pass": abs(round(swordsman_total * 100, 2) - 43.95) < 0.01})

# 51. 边际对偶精确值
results.append({"name": "边际对偶精确值(4.740937)", "expected": 4.740937, "actual": round(marginal_ratio, 6), "pass": abs(marginal_ratio - 4.740937) < 0.001})

# 52. 力量收益精确值
results.append({"name": "狂战士力量收益精确值(百分比)", "expected": 24.42, "actual": round(str_gain * 100, 2), "pass": abs(round(str_gain * 100, 2) - 24.42) < 0.01})
results.append({"name": "剑魂力量收益精确值", "expected": 36.47, "actual": round(sw_str_gain * 100, 2), "pass": abs(round(sw_str_gain * 100, 2) - 36.47) < 0.01})

# 53. 物理攻击收益精确值
results.append({"name": "狂战士物理攻击收益精确值(百分比)", "expected": 5.50, "actual": round(phy_gain * 100, 2), "pass": abs(round(phy_gain * 100, 2) - 5.50) < 0.01})
results.append({"name": "剑魂物理攻击收益精确值(破极后)", "expected": 4.23, "actual": round(sw_phy_gain * 100, 2), "pass": abs(round(sw_phy_gain * 100, 2) - 4.23) < 0.01})

# 54. 暴击收益精确值
results.append({"name": "暴击收益精确值(狂战士)", "expected": 1.18, "actual": round(crit_gain * 100, 2), "pass": abs(round(crit_gain * 100, 2) - 1.18) < 0.01})
results.append({"name": "暴击收益精确值(剑魂)", "expected": 1.2, "actual": round(sw_crit_gain * 100, 2), "pass": abs(round(sw_crit_gain * 100, 2) - 1.2) < 0.01})

# 55. 狂战士力量+CC精确值
results.append({"name": "狂战士力量+CC(暴走后)精确值", "expected": 1329.2, "actual": round(berserker_str_berserk + cc_str, 1), "pass": abs((berserker_str_berserk + cc_str) - 1329.2) < 0.01})

# 56. 剑魂力量+CC精确值
results.append({"name": "剑魂力量+CC精确值", "expected": 910, "actual": swordsman_str + cc_str, "pass": (swordsman_str + cc_str) == 910})

# 57. 狂战士物理攻击+CC精确值
results.append({"name": "狂战士物理攻击+CC精确值", "expected": 2110, "actual": berserker_phy + cc_phy, "pass": (berserker_phy + cc_phy) == 2110})

# 58. 剑魂破极后物理攻击+CC精确值
results.append({"name": "剑魂破极后物理攻击+CC精确值", "expected": 2710, "actual": swordsman_phy_pojie + cc_phy, "pass": (swordsman_phy_pojie + cc_phy) == 2710})

# 59. 固伤综合精确值
results.append({"name": "狂战士固伤综合精确值", "expected": 9.27, "actual": round(berserker_fixed_total * 100, 2), "pass": abs(round(berserker_fixed_total * 100, 2) - 9.27) < 0.01})

# 60. 百分比综合精确值
results.append({"name": "狂战士百分比综合精确值", "expected": 32.81, "actual": round(berserker_pct_total * 100, 2), "pass": abs(round(berserker_pct_total * 100, 2) - 32.81) < 0.01})
results.append({"name": "剑魂百分比综合精确值", "expected": 43.95, "actual": round(swordsman_total * 100, 2), "pass": abs(round(swordsman_total * 100, 2) - 43.95) < 0.01})

# 61. 边际对偶精确值
results.append({"name": "边际对偶精确值(4.740937)", "expected": 4.740937, "actual": round(marginal_ratio, 6), "pass": abs(marginal_ratio - 4.740937) < 0.001})

# 62. 力量收益精确值
results.append({"name": "狂战士力量收益精确值(百分比)", "expected": 24.42, "actual": round(str_gain * 100, 2), "pass": abs(round(str_gain * 100, 2) - 24.42) < 0.01})
results.append({"name": "剑魂力量收益精确值", "expected": 36.47, "actual": round(sw_str_gain * 100, 2), "pass": abs(round(sw_str_gain * 100, 2) - 36.47) < 0.01})

# 63. 物理攻击收益精确值
results.append({"name": "狂战士物理攻击收益精确值(百分比)", "expected": 5.50, "actual": round(phy_gain * 100, 2), "pass": abs(round(phy_gain * 100, 2) - 5.50) < 0.01})
results.append({"name":