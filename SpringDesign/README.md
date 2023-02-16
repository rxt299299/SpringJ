# Optimal Helical Compression Srping Design
### A flexible methodology for Optimal Helical Compression Srping Design

#### after the Feasibility check

```
#set the spring class
#initial parameters
spring_para_dict_input = {
    'end_closed':True,
    'L_free':85.5,
    'L_hard':20,
    'G':77,
}

constraint_policy = {
    'outerDiamMax':60,
    'MaximumShearStressMax': 0.7,
    'CoilBindingGapMin': 0.5,
}

objective = {
    'spring_rate_spring_index': {'MaxorMin':'min', 'k_max': 20, 'c_max':10}
}

sping = Spring(spring_para_dict_input,
               constraint_policy,
               objective)

feasible_arr = spring.Feasibility(bounds_inputs)

if len(list(feasible_arr))<1:
    print ("do not pass the Feasibility test!")

bounds = list(bounds_inputs.values())
res = minimize(sping_1.ConstraintsForOptimize, bounds=bounds)

print (res)
```

#### References
 - Poisson's Ratio:
   - https://www.engineeringtoolbox.com/Poissons-ratio-d_1224.html
 - 弹簧的相关参数
   - https://www.tanhuang1688.com/news_view.asp?id=2
 - 弹簧常见的4种材料
   - https://zhuanlan.zhihu.com/p/396721931
 - 常用材料弹性模量以及泊松比
   - https://www.xd-sj.com/1838/.html
 - 需要买一下
   - https://bbs.pinggu.org/thread-11160063-1-1.html
 - google search: Spring steel Poisson's ratio
    - https://blog.federnshop.com/en/spring-steel-properties/
    - https://www.matweb.com/search/datasheet_print.aspx?matguid=4bcaab41d4eb43b3824d9de31c2c6849
    - https://www.makeitfrom.com/material-properties/ASTM-A227-Spring-Steel
    - https://www.tokaibane.com/en/topic/10701
    - https://www.acxesspring.com/properties-of-common-spring-materials-spring-wires.html


 - 资料
   - 65Mn弹簧钢的密度，泊松比，E是: 65Mn密度, ρ=7.81克/立方厘米, 杨氏模量E=196500-198600MPa, 剪切模量G=78600-80670MPa, 泊松比u=E/2G
   - 根据查询弹簧钢相关资料显示，弹簧钢的弹性模量是206GPa。60Si2Mn弹簧钢泊松比为0.26~0.32、弹性模量206GPa。弹簧钢是指由于在淬火和回火状态下的弹性，而专门用于制造弹簧和弹性元件的钢。
   - 弹簧钢 45号钢: 密度7.85g/cm3, 弹性模量210GPa, 泊松比0.31 http://www.cxspring.com/fabu/202211/74025.html
   - 铬钒钢、铬镍钢、铬镍钼钢、铬锰钢、硅钢、铬锰硅镍钢、硅锰钢、硅铬钢的密度都是7.85 .
