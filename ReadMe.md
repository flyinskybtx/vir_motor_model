# 采数据
执行scripts/collect_pmsm_data.py
或scripts/collect_pmsm_dq_data.py, dq可以实现控制功能

可选参数见args
-u，-i, -v, -a 分别为电压、电流、速度、加速度的绝对值的最大值，可不改
-n 为电流（注意是只有ab相电流有噪声）噪声
-s 为每个episode最大步数，使用dq控制时大概1e4步可以达到稳态
-r （仅ab相电压控制时有效） 为每个episode内每一步是否随机一个新电压，如果选否则在episode开始时随机一个电压后整个episode内持续不变
-N 为运行采集的样本总数

数据默认储存在data目录下
格式为“<样本数>_of_<是否随机控制>_<噪声大小>_<数据创建时间>.csv”

# ---
更新：DQ相控制时，当转速稳定后切换到下一个episode，建议每个episode不短于1e4，

**建议先试用不带dq的版本，输入id0 iq0 vel0 ud uq 输出id iq vel**


