# 30篇新增期刊论文：证据与技能改进

核对日期：2026-09-30。逐篇定向阅读方法、结果图与图注；DOI、题名和期刊以出版方及Crossref交叉核验。不是系统综述，也未重做论文统计。原技能已引用的Crameri等（2020）和Thyng等（2016）不计入这30篇。

每条将“论文观察”与“本技能采用的改进”分开；后者是结合Origin操作的设计判断，不是期刊强制规定。论文PDF、全文和原图仅用于本地阅读，不随技能分发。

可机读条目见[literature-30.json](literature-30.json)，引用见[BibTeX](literature-30.bib)。图型实施见[期刊图型配方](journal-figure-recipes.md)。

| 分组 | 篇数 |
|---|---:|
| 配色与图形信息 | 2 |
| 模型诊断 | 7 |
| 水文分布与样本支持 | 4 |
| 概率与集合 | 4 |
| 多变量气候诊断 | 4 |
| 复合极端与事件 | 5 |
| 季节性与时频 | 4 |

## P01 · Crameri (2018)

**Geodynamic diagnostics, scientific visualisation and StagLab 3.0**. Geoscientific Model Development. [DOI](https://doi.org/10.5194/gmd-11-2541-2018)

- 阅读定位：Section 3; Figures 4–5 and 8–10。
- 论文观察：用同一数据比较色表、连续/离散映射和信息简化，说明色彩梯度与图形装饰会改变读者判断。
- 本技能采用：保留25套色表；增加任务驱动选色、灰度检查和分析图/成稿图两种信息密度。
- 使用边界：该文的色彩误差数值针对其试验，不作为所有色表的通用误差率。

## P02 · Stauffer et al. (2015)

**Somewhere Over the Rainbow: How to Make Effective Use of Colors in Meteorological Visualizations**. Bulletin of the American Meteorological Society. [DOI](https://doi.org/10.1175/bams-d-13-00155.1)

- 阅读定位：Meteorological examples; Figures 3–6, printed pp. 208–211。
- 论文观察：降水量、预警类别和锋区识别需要不同颜色编码；论文比较彩色、灰度和色觉缺陷条件。
- 本技能采用：先确定任务是读数、分类还是识别梯度；类别加符号，锋区加物理等值线，最终尺寸检查灰度。
- 使用边界：HCL或彩虹形外观本身不等于适用；需要核对实际亮度与色阶含义。
- 获取说明：AMS HTML 403. Read Article I in author compilation, printed journal pages 203–216; compilation not counted as another paper. [全文入口](https://retostauffer.org/files/2025-05-13-habilitation.pdf)

## P03 · Knoben et al. (2019)

**Technical note: Inherent benchmark or not? Comparing Nash–Sutcliffe and Kling–Gupta efficiency scores**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-23-4323-2019)

- 阅读定位：Figure 1; Sections 3.1–3.3。
- 论文观察：NSE与KGE并不等价，零值和基准模型之间的关系不能跨指标照搬。
- 本技能采用：技能比较图写清指标版本、方向和显式基准；KGE不自动以0作为达标线。
- 使用边界：原始KGE的均值流量基准1−√2不是所有变体和业务任务的统一阈值。

## P04 · Schwemmle et al. (2021)

**Technical note: Diagnostic efficiency – specific evaluation of model performance**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-25-2187-2021)

- 阅读定位：Sections 2.1–2.3; Figures 2–5。
- 论文观察：过程线、流量历时曲线和诊断极坐标图联合区分恒定、动态和时序误差。
- 本技能采用：总分旁配FDC与误差分量；有验证过的实现时才采用DE极图，否则用分量点图。
- 使用边界：排序后的FDC丢失时间顺序，不能单凭FDC重合判断洪峰时间正确。

## P05 · Westerberg et al. (2011)

**Calibration of hydrological models using flow-duration curves**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-15-2205-2011)

- 阅读定位：Publisher PDF abstract and methods: evaluation points and limits of acceptability。
- 论文观察：FDC评价点可按应用强调高流或低流，同时考虑观测流量的不确定性。
- 本技能采用：FDC写明选取时段、超越概率定义和重点分位段；观测也可有区间。
- 使用边界：FDC分布拟合不能替代对积雪过程或亚日尺度峰时的验证。
- 获取说明：Publisher PDF methods and selected figure evidence read using web PDF extraction; local large-PDF download abandoned after slow transfer. [全文入口](https://hess.copernicus.org/articles/15/2205/2011/hess-15-2205-2011.pdf)

## P06 · Ridolfi et al. (2020)

**A methodology to estimate flow duration curves at partially ungauged basins**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-24-2043-2020)

- 阅读定位：Section 3; Figures 3, 7–11 and 13。
- 论文观察：按水文年和供体/目标时段比较FDC，并按百分位报告误差。
- 本技能采用：用分位误差小面板定位高/中/低流问题，标注水文年起点与各曲线的样本期。
- 使用边界：不同记录长度或时期的曲线不应直接解释为纯模型差异。

## P07 · Kratzert et al. (2018)

**Rainfall–runoff modelling using Long Short-Term Memory (LSTM) networks**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-22-6005-2018)

- 阅读定位：Figures 6–8 and 14–15。
- 论文观察：过程图、流域技能分布和内部状态对照共同评价径流网络；部分图采用坐标截断。
- 本技能采用：给出过程、跨流域分布和峰/低流诊断；若截断负技能分数，另报截断数与完整范围。
- 使用边界：内部状态与水文变量相似不是物理机制被唯一识别的证明。

## P08 · Kratzert et al. (2019)

**Towards learning universal, regional, and local hydrological behaviors via machine learning applied to large-sample datasets**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-23-5089-2019)

- 阅读定位：Figures 3–6 and 9–12。
- 论文观察：用经验累计分布比较大样本技能，另外展示扰动稳健性和流域嵌入。
- 本技能采用：新增技能ECDF和配对改进图；区分跨流域、随机重训与聚类重启三个变异来源。
- 使用边界：独立排序的两条ECDF不能显示同一流域是否改善，需保留配对键。

## P09 · Gauch et al. (2021)

**Rainfall–runoff prediction at multiple timescales with a single Long Short-Term Memory network**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-25-2045-2021)

- 阅读定位：Section 2.3.2; Figures 3–4。
- 论文观察：逐时间尺度展示NSE分布与峰时误差，并评价跨尺度一致性。
- 本技能采用：小时/日尺度分面并标累计或平均含义；峰时偏差保留小时/天单位。
- 使用边界：不同时间尺度的技能不强行同轴解释；聚合规则必须先由上游确定。

## P10 · Klotz et al. (2022)

**Uncertainty estimation with deep learning for rainfall–runoff modeling**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-26-1673-2022)

- 阅读定位：Sections 2–3; Figures 2 and 8–11。
- 论文观察：预测分布用概率图及相对理想线的偏差评价，事件过程图用内外分位区间。
- 本技能采用：新增概率校准偏差图与嵌套预测区间；保留逐流域检查而非只报全域聚合。
- 使用边界：预测区间、均值置信区间和模型间范围不是同一种不确定性。

## P11 · Addor et al. (2017)

**The CAMELS data set: catchment attributes and meteorology for large-sample studies**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-21-5293-2017)

- 阅读定位：Figures 1–4; Tables 2–3; Sections 4–5。
- 论文观察：流域地图配样本分布，并明确记录可用性、属性单位和水文指标定义。
- 本技能采用：数据概况图补缺测覆盖、记录长度与分组样本数；Q5/Q95注明非超越分位还是超越概率。
- 使用边界：间歇河流的对数FDC斜率可能未定义，不用0填充。
- 获取说明：Publisher PDF methods and selected figure evidence read using web PDF extraction; local large-PDF download abandoned after slow transfer. [全文入口](https://hess.copernicus.org/articles/21/5293/2017/hess-21-5293-2017.pdf)

## P12 · Wagener et al. (2026)

**Metrics that matter: objective functions and their impact on signature representation in conceptual hydrological models**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-30-4867-2026)

- 阅读定位：Figures 3–6 and 10; Sections 3–4。
- 论文观察：不同目标函数在不同水文特征上表现不同；分布图给出保留运行数并对照观测。
- 本技能采用：新增指标×模型图和特征值分布；用显式观测基准，保留各组分母。
- 使用边界：参数集合大小不是独立流域样本数；多个高度相关指标不能冒充独立证据。

## P13 · Pizarro et al. (2025)

**Combining uncertainty quantification and entropy-inspired concepts into a single objective function for rainfall-runoff model calibration**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-29-4913-2025)

- 阅读定位：Figures 4–6。
- 论文观察：分别展示率定/验证的过程、不确定性、分布及观测—模拟水文特征对照。
- 本技能采用：将率定与独立验证分面；特征散点使用1:1线并标单位。
- 使用边界：原图的截断坐标不照搬；先检查被隐藏的离群值和极端误差。

## P14 · Pulkkinen et al. (2019)

**Pysteps: an open-source Python library for probabilistic precipitation nowcasting (v1.0)**. Geoscientific Model Development. [DOI](https://doi.org/10.5194/gmd-12-4185-2019)

- 阅读定位：Section 4.2; Figures 5–7, 19 and 22–24。
- 论文观察：短临降水同时按阈值、预报时效、空间尺度检查可靠度、秩、ROC和邻域技能。
- 本技能采用：可靠度旁列分箱样本数；新增时效×尺度技能图，阈值作为分面条件。
- 使用边界：确定性技能、概率校准和空间容错评价不能互相代替。

## P15 · Zhu et al. (2025)

**Quantifying the analysis uncertainty for nowcasting application**. Geoscientific Model Development. [DOI](https://doi.org/10.5194/gmd-18-1545-2025)

- 阅读定位：Section 4; Figures 2, 4, 8–11。
- 论文观察：误差、集合离散度、秩直方图和可靠度共同评价分析与短临集合，并分训练/测试站。
- 本技能采用：新增spread–error图与秩直方图；注明成员数、时效和独立站点。
- 使用边界：秩近似均匀不单独证明预报有技巧，sharpness也不等同于resolution。

## P16 · Eyring et al. (2020)

**Earth System Model Evaluation Tool (ESMValTool) v2.0 – an extended set of large-scale diagnostics for quasi-operational and comprehensive evaluation of Earth system models in CMIP**. Geoscientific Model Development. [DOI](https://doi.org/10.5194/gmd-13-3383-2020)

- 阅读定位：Section 3.1; Figures 1–5。
- 论文观察：相对误差矩阵、相关诊断、QBO时高图和多变量场图组织综合模式评价。
- 本技能采用：新增portrait矩阵与QBO时高配方；同一比较固定参考数据、权重和标准化。
- 使用边界：相对集合中位数的配色会随入选模式变化；不能解释为固定绝对合格标准。

## P17 · Weigel et al. (2021)

**Earth System Model Evaluation Tool (ESMValTool) v2.0 – diagnostics for extreme events, regional and impact evaluation, and analysis of Earth system models in CMIP**. Geoscientific Model Development. [DOI](https://doi.org/10.5194/gmd-14-3159-2021)

- 阅读定位：Sections 3.1–3.4; Figures 5–7 and 13–16。
- 论文观察：极端指数趋势、区域季节偏差和多模式分布互补；阴影明确为集合四分位范围。
- 本技能采用：极端图附阈值基期、持续天数与分位范围；率和频次分开。
- 使用边界：不同指标的阈值或累计时长不能复用；集合IQR不标作95% CI。

## P18 · Lauer et al. (2025)

**Monitoring and benchmarking Earth system model simulations with ESMValTool v2.12.0**. Geoscientific Model Development. [DOI](https://doi.org/10.5194/gmd-18-1169-2025)

- 阅读定位：Sections 3.1–3.6; Figures 2 and 5–8。
- 论文观察：时间、季节、空间和相对技能矩阵共同定位模式异常；点状覆盖可代表集合基准比较。
- 本技能采用：总览—异常定位—详细证据三层诊断；图注说明点状覆盖到底表示什么。
- 使用边界：点状纹理不必然表示p<0.05；不能用习惯替换论文中的实际语义。

## P19 · Li et al. (2021)

**A standardized index for assessing sub-monthly compound dry and hot conditions with application in China**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-25-1587-2021)

- 阅读定位：Section 2.4; Figures 2–3 and 8–12。
- 论文观察：联合指标等值线与游程事件示意区分持续时间、严重度、强度和频次。
- 本技能采用：新增复合事件阈值象限与事件带图；分开累计严重度和平均强度。
- 使用边界：阈值和最短历时是研究定义，不能把文中数值写成领域通用标准。

## P20 · Zscheischler et al. (2021)

**Evaluating the dependence structure of compound precipitation and wind speed extremes**. Earth System Dynamics. [DOI](https://doi.org/10.5194/esd-12-1-2021)

- 阅读定位：Section 3; Figures 3–4 and 6–7。
- 论文观察：原始/变换边际散点和随分位阈值变化的尾依赖曲线共同检查复合风险。
- 本技能采用：尾依赖诊断注明边际变换、时空窗口、阈值与区间；原单位图和变换图分面。
- 使用边界：相关系数不等于尾依赖，尾部共现也不自动构成因果证据。

## P21 · Jin et al. (2026)

**Global escalation of more frequent and intense compound heatwave-extreme precipitation events**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-30-5229-2026)

- 阅读定位：Sections 3.2–3.4; Figures 1 and 4–7。
- 论文观察：通过事件定义图、特征时间变化与差值累计分布比较复合和单一极端事件。
- 本技能采用：新增热后雨事件条带与特征对照；同一特征对比共享单位，场景分面。
- 使用边界：条件概率、偶遇概率及其比值必须区分；比值中性值是1。

## P22 · Liu et al. (2026)

**Understanding meteorological, runoff, and agricultural drought propagation and their influencing factors in an ensemble of multiple datasets**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-30-2775-2026)

- 阅读定位：Sections 2.3–2.6; Figures 2–4, 6 and 8。
- 论文观察：区分相关分析响应时间与事件匹配滞后，另展示数据集差异和趋势。
- 本技能采用：新增干旱传播响应/滞后矩阵，明确两种时间定义并单列数据集不确定性。
- 使用边界：均值接近0时CV可能不稳定；缺测、未显著和无事件采用不同编码。

## P23 · Hall et al. (2018)

**Spatial patterns and characteristics of flood seasonality in Europe**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-22-3883-2018)

- 阅读定位：Section 3.1; Figures 3–4 and 9–10。
- 论文观察：圆形统计同时表示洪水平均日期和季节集中程度，并识别无明显季节性的站点。
- 本技能采用：新增日期角度—集中度半径图；图例写清日历、水文年起点、样本年数。
- 使用边界：不能对12月和1月日期做普通算术平均；双峰季节性不压缩成单一平均日期。

## P24 · Tramblay et al. (2023)

**Changes in Mediterranean flood processes and seasonality**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-27-2973-2023)

- 阅读定位：Sections 3.2–3.4; Figures 4, 6, 8 and 10。
- 论文观察：季节变化结合天气类型和产洪机制分类，避免只给一条总体时间趋势。
- 本技能采用：新增季节×事件类型小面板；保留不同阶段各类型样本数和分类规则。
- 使用边界：百分比变化在基期类别稀少时不稳定，配套给出原始次数。

## P25 · Fang et al. (2024)

**An increase in the spatial extent of European floods over the last 70 years**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-28-3755-2024)

- 阅读定位：Sections 2.3–2.5; Figures 2–5。
- 论文观察：洪水范围、持续时间、频次和强度分别展示，并区分危害与人口暴露。
- 本技能采用：趋势面板一变量一单位；气泡面积编码物理量并标尺寸图例，暴露加权结果单列。
- 使用边界：不要用气泡半径与物理量线性对应；事件强度、影响面积和暴露不是同一量。

## P26 · Yildiz et al. (2023)

**Technical note: Statistical generation of climate-perturbed flow duration curves**. Hydrology and Earth System Sciences. [DOI](https://doi.org/10.5194/hess-27-2499-2023)

- 阅读定位：Section 3; Figures 2–4。
- 论文观察：相同平均流量变化可对应不同FDC形状，集合背景与重点情景并列。
- 本技能采用：用浅灰展示情景FDC族，突出已事先选定的情景；对不同分位段分别诊断。
- 使用边界：样本情景的包络不自动具有概率或置信度含义。

## P27 · Kay et al. (2024)

**Demonstrating the use of UNSEEN climate data for hydrological applications: case studies for extreme floods and droughts in England**. Natural Hazards and Earth System Sciences. [DOI](https://doi.org/10.5194/nhess-24-2953-2024)

- 阅读定位：Sections 2.4 and 3; Figures 2–7。
- 论文观察：按季节背景显示集合中位数、分位与极值，并跟踪极端后的恢复或持续。
- 本技能采用：新增嵌套集合带与恢复概率面板；单条故事线始终保留同一个成员标识。
- 使用边界：逐月挑选不同成员的最极端值拼成一条线，不代表真实可实现的成员轨迹。

## P28 · Grinsted et al. (2004)

**Application of the cross wavelet transform and wavelet coherence to geophysical time series**. Nonlinear Processes in Geophysics. [DOI](https://doi.org/10.5194/npg-11-561-2004)

- 阅读定位：Publisher PDF; Figures 1–5 and wavelet-coherence methods。
- 论文观察：小波功率/相干图配显著性、影响锥和相位信息，说明平滑与噪声模型的作用。
- 本技能采用：新增时频图配方：周期对数轴、COI遮罩、相位箭头图例及固定色标。
- 使用边界：相位必须交代变量顺序与箭头方向；图上领先关系不直接证明因果。

## P29 · Schulte (2019)

**Statistical hypothesis testing in wavelet analysis: theoretical developments and applications to Indian rainfall**. Nonlinear Processes in Geophysics. [DOI](https://doi.org/10.5194/npg-26-91-2019)

- 阅读定位：Section 2.2; Figures 7–12。
- 论文观察：比较多种小波显著性检验，展示降水与ENSO时频分析中显著区域的变化。
- 本技能采用：显著轮廓注明逐点或区域检验及零假设；绘图层只读取上游掩膜。
- 使用边界：相邻时频像素不是独立样本；不能把成片逐点显著当已控制多重比较。

## P30 · Levine et al. (2024)

**Storylines of summer Arctic climate change constrained by Barents–Kara seas and Arctic tropospheric warming for climate risk assessment**. Earth System Dynamics. [DOI](https://doi.org/10.5194/esd-15-1161-2024)

- 阅读定位：Section 2.2; Figures 1–6 and Appendix C。
- 论文观察：以物理驱动构造故事线，区分标准化响应、多模式平均与总体变化。
- 本技能采用：新增故事线四象限/小面板；写明每K归一化、基准时期和是否包含集合平均。
- 使用边界：故事线不是发生概率排序；模式符号一致性不等同于显著性检验。
