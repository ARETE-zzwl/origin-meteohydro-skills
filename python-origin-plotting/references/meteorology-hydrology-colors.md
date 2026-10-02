# 气象水文色标选用

颜色要对应物理量、比较对象及归一化，不存在适用于所有气象图的单一“标准colorbar”。`assets/palette_catalog.json`为机器可读目录；`assets/palettes/`包含RGB/HEX CSV和Origin可读JASC PAL。原始LUT、许可和SHA另行保留。低端到高端的方向按文件行序，不自行假定红色总是正值。

## 变量与配色

2026-10-02新增15套并保留原25套，现有40套。新增配色及精简colorbar的尺寸、主刻度、浅填充、Origin设置见[科研配色精修](scientific-color-recipes.md)；[四页参考册](../assets/scientific_color_reference/Origin_scientific_color_reference.pdf)含12类原生Origin合成实例。下方2026-09-30文献学习段落中的25套为当时的资产规模。

| 变量/用途 | 可选色标 | 数值映射与注意点 |
|---|---|---|
| 日/累计降水、径流量 | cmocean_rain、Blues、YlGnBu | 非负顺序；先说明mm、mm/d或m³/s；无雨与NaN分开 |
| 降水业务分级或复现NCL旧图 | ncl_precip_11lev、ncl_WhiteBlueGreenYellowRed | 离散边界需单独指定；LUT名字不是降水等级标准；传统多色表非感知均匀 |
| 降水/土壤湿度/径流距平、SPI/SPEI | BrBG、cmocean_delta、ncl_precip_diff_12lev | 0为物理中心，约定负干/正湿；SPI/SPEI无量纲，水文量勿错写标准化单位 |
| 温度/SST绝对值 | cmocean_thermal、batlow、magma | 顺序；K→°C转换必须明确；不为对比方便把绝对值当距平 |
| 温度/SST距平、Z500距平、回归系数 | RdBu_r、vik、cmocean_balance、PuOr | 发散，以0为中心；正负端色义写清；共有尺度 |
| 风速、IVT模长 | cmocean_speed、viridis、cividis | 顺序；风矢量给参考箭头；IVT常用kg m⁻¹ s⁻¹ |
| ω或−ω、VIMFC、散度、垂直速度差 | vik、RdBu_r、cmocean_balance | 发散；ω>0是下沉；辐合是否用−div(Q)先确认 |
| 土壤湿度绝对值、比湿、水量 | YlGnBu、viridis、batlow | 顺序；体积含水率/质量含水率及单位不同 |
| 相关系数r、技能变化、风险差 | RdBu_r、vik | r可固定[-1,1]；百分点与相对百分比不同；风险比中性值是1，不是0 |
| 概率、可靠度热图 | cividis、viridis、Blues | 概率界限[0,1]或[0,100]；BSS有负值则用0中心发散 |
| 风向、相位角、日内相位 | cmocean_phase、twilight | 循环首尾相接；风向“来自”与矢量“指向”区分；月份分类未必需连续循环色标 |
| 模式/试验/流域类别 | okabe_ito、tab10、heat_rain_roles | 类别离散，不插值成连续物理colorbar；配合符号/线型 |

`heat_rain_roles`是本地项目角色配色（热/对照/雨/重建剩余等），不是气象领域通用标准。

## 分级与归一化

- 正常连续量用Normalize；真正长尾且严格正的数据可用LogNorm，0及负数需单独处理而非偷偷截断。
- 差值通常用关于0对称的范围。物理上确需非对称范围时可用TwoSlopeNorm，明确两侧每单位颜色跨度不同。
- 离散图用明确边界数组和BoundaryNorm；N个区间需要N+1个边界。`palette_tools export`从连续LUT等间距取N个颜色（含两端），将其依次映射到N个区间；这与按原物理数值线性着色不同。原始分级LUT保留全部颜色，区间数量不匹配时提示，不无声补齐或丢弃。
- 所有例子中的分级仅用于演示。用实际产品/机构规定时引用对应标准、变量和累计时长，不把日降水等级用于小时雨强。
- colorbar标明单位和刻度，越界值用extend；缺测常用浅灰或掩膜并标注；不能让缺测白色与零距平白色无从区分。
- 多面板同变量统一边界、中心和缺测处理。模型逐图自动色阶会破坏幅值比较。
- 色盲/灰度友好是设计目标，不保证任意色标组合、任意缩版都通过；类别须用符号/线型冗余。传统彩虹主要用于复现或离散业务约定，分析连续差值优先平滑顺序/发散表。

## 来自新增文献的配色检查

- 先明确任务是精确读值、区分类别还是识别梯度，再选择映射。锋区位置应由物理梯度支持，不由高饱和色表的突变代替。（新增P01–P02）
- 技能矩阵的相对误差以显式基准为中心；加入/移除模式可能改变相对集合中位数，不比较未注明基准的两套颜色。（P16、P18）
- 缺测、无事件、未通过检验、真实0分开编码。纹理含义写在图注，不能默认都是显著性。（P18、P22、P30）
- 25套离线色表保持原样，本次新增的是选用依据与检查方法，没有为凑数量增加未经核对的色表。色觉缺陷模拟与灰度是检查步骤，不保证任意图自动可读。

出处和具体阅读位置见[30篇文献](literature-30.md)。

## Origin导入方法

Tools → Color Manager → Import from Files，选`assets/palettes/*.pal`；或支持版本中拖入PAL。少于20色的文件可能被Origin自动保存为Color List而非连续Palette，这是官方默认行为，不必改全局@MPS。在Colormap/Contours中另设Levels和缺测/越界颜色；导入LUT不等于设置了单位或阈值。

这些JASC PAL仅含颜色，不含bin边界、单位、NaN/over/under行为；配套区间CSV/metadata必须一起使用。未自动把色标写进用户全局Origin色库。

## 来源

- [Matplotlib色标分类](https://matplotlib.org/stable/users/explain/colors/colormaps.html)与[归一化](https://matplotlib.org/stable/users/explain/colors/colormapnorms.html)。
- [cmocean官方说明](https://matplotlib.org/cmocean/)；Thyng等，2016，True colors of oceanography，doi:10.5670/oceanog.2016.66。
- [Scientific colour maps](https://www.fabiocrameri.ch/colourmaps/)，以cmcrameri所附Scientific colour maps 8.0数据为本次来源；Crameri等2020，doi:10.1038/s41467-020-19160-7。
- [NCAR/NCL色表](https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml)。收录表示常见/可复用，不表示全都优于感知均匀色标。
- [Origin导入格式](https://docs.originlab.com/quick-help/use-external-color-palette/)与[Color Manager](https://docs.originlab.com/origin-help/color-manager/)。
