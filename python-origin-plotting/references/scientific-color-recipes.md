# 科研配色与colorbar精修

适用于统计图、分布图、效应图及热图。先区分“类别配色”与“数值色标”，再选颜色。离线库现有40套：原25套保留，新增9套Scientific Colour Maps与6套Paul Tol类别配色；不需要每次下载。

## 从数据角色选色

| 数据角色 | 优先试用 | 使用要点 |
| --- | --- | --- |
| 两组比较、时期、路径 | `#0072B2` / `#D55E00`；或tol_high_contrast中的适当两色 | 主线用原色，填充与白色混合至20%–35%原色；实线/虚线或不同点形辅助识别。蓝朱红为本项目惯例，不是所有项目的固定标准。 |
| 3–7组 | tol_bright、tol_vibrant | 组色在同一图组内固定；多于4组优先检查能否分面，避免所有曲线重叠。 |
| 更多类别 | tol_muted、okabe_ito | 保留离散色；类别无数值顺序时不绘制连续colorbar。 |
| 箱体、小提琴、区间带 | 主线同色浅填充；tol_pale作为填充候选 | 浅色不代替细线/小点的深色轮廓；填充透明度或与白色混合不改变原色表文件。 |
| 非负强度、含水量、概率 | navia、batlow、cividis、viridis；降水可用cmocean_rain | 颜色有顺序；真正有物理零点才从0起，概率保持0–1。不要把离散类别当强度。 |
| 正负距平、差值 | vik、broc、bam、cmocean_balance | 中性值放中心。同变量/单位的对比面板共用范围。风险比中点为1，不能机械设0。 |
| 更强调高值的幅度图 | lipari、lajolla、magma | 先检查低端细节和白底可读性；不用暗端裁切隐藏有效数值。 |
| 方向和相位 | romaO、cmocean_phase、twilight | 首尾颜色接续，0°和360°对应相同方向；明确角度和向量约定。 |

新色表原方向保持原样；需要反转用显式`--reverse`并记录。不能凭色名推断“蓝一定是负值”，最终以LUT的低值端、高值端为准。

## 一条精简、完整的色标

- 先设图的范围和Levels，再调整色标外观。颜色文件不含单位、边界、缺测或越界规则。
- 常用双栏180 mm图可先试3–4 mm厚、约45–75 mm长的水平色标，刻度7–8 pt、标题8 pt；这只是起点，按面板大小和期刊要求调整。
- 优先显示3–6个容易阅读的主刻度；端点和物理中心保留，不把每个色阶都印成小字。隐藏无用次刻度，删去重复单位和冗长标题。
- 连续色标按真实数值比例放刻度。离散区间保留原分级边界，不用均匀标签位置冒充线性映射。
- 同变量的多个面板可共用一条色标；不同单位、归一化或参考期的面板不能仅为省空间合并。
- 范围外仍有有效值时保留头尾/溢出提示，不能为整洁裁去。缺测与0分开；研究区域外或海上本来不属于分析域的格点直接掩膜，不必在每幅图重复添加缺测图例。
- 白色或极浅色中心应能与背景分辨；可以保留细边框或极浅中性色，不用粗黑框分割每个小色阶。

## Origin中的实际设置

1. Tools > Color Manager > Import from Files导入`assets/palettes/*.pal`。少于20色的PAL可能被列为Color List，这是正常行为。
2. Plot Details > Colormap/Contours设置真实Levels、颜色方向与缺测/越界处理。分类系列在Group或颜色索引中指定离散Color List。
3. 双击Color Scale，在Levels中挑选主刻度，在Labels中简化数值格式，在Title中写变量/单位，在Line and Ticks中调整线宽。不要把仅修改色标标签误当作已经修改数据映射。
4. 保存OPJU并复开，核对LUT颜色、范围、中心和真实绘图结果。Palette导入成功不等于图已经用上该Palette。

官方依据：[外部PAL导入](https://docs.originlab.com/quick-help/use-external-color-palette/)、[Color Scale设置](https://docs.originlab.com/origin-help/colorscale/)。

## 离线资源与实例

- [四页配色参考册](../assets/scientific_color_reference/Origin_scientific_color_reference.pdf)：前两页为重新绘制的12类原生Origin图，后两页为色表选择和数值色标示范。全为合成示例，不是论文结果。
- `assets/scientific_color_reference/origin_scientific_colors.opju`：独立、可编辑的Origin工程。密度与箱线用原生XY曲线和点实现，不冒称Origin内置统计小提琴对象；分裂热图色标为使用同一映射生成的原生矢量图例，不与ColorScale控件动态联动。
- [官方图型与应用表](origin-gallery-recipes.md)：12种画法的入口、数据要求及适用情形。
- `scripts/origin_color_gallery.py --out <新目录> --synthetic`：重绘12类示例；需要Origin、originpro、NumPy、pandas和SciPy。采用已验证的原生数据标签法；不改用户已打开的工程。
- `scripts/build_color_reference.py --out <新目录>`：用离线CSV生成后两页配色和色标说明，需要ReportLab；字体可按实际机器修改。
- 随后运行`scripts/assemble_color_reference.py --source <上面两脚本共用的目录> --out <参考册目录>`，合并四页、嵌入字体并生成预览；需要PyMuPDF、fontTools。保留OPJU原文件，PDF合并不会把后两页加入Origin工程。
- `scripts/extend_scientific_palettes.py`：通常无需运行。只有明确更新源数据时才加`--allow-network`；固定提交下载LUT文本，不安装或运行第三方程序。

多组轨迹和区间带：先绘制全部浅色区间，再绘制全部主线与点，避免后一组填充覆盖前一组主线。连续色条的矢量PDF若由大量矩形拼接，阅读器抗锯齿可能产生白色细缝；本参考册改用PDF轴向渐变，按完整LUT插值，不改变端点和归一化。类别和明确分级的色条仍保留离散色块，不用连续渐变混淆分界。

图面检查不仅看色表条：还看窄线、小点、浅填充、多个系列交叉与最终缩版。灰度可检验明暗层级，但不能单凭灰度通过就宣称所有色觉条件均已验证。来源中的可读性设计不等于任意组合都自动可读。

来源：[Scientific Colour Maps](https://www.fabiocrameri.ch/colourmaps/)、[Paul Tol](https://sronpersonalpages.nl/~pault/)、[cmocean](https://matplotlib.org/cmocean/)。来源版本和RGB文件哈希见`assets/palette_catalog.json`。
