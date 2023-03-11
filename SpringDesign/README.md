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
