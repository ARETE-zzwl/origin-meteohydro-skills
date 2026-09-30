---
name: python-origin-plotting
description: >-
  Create and refine native OriginPro scientific figures with Python, especially
  meteorology and hydrology plots, editable OPJU projects, scientific colorbars,
  RGB/PAL palettes, event composites, uncertainty plots and hydrographs.
  Includes literature-grounded model diagnostics, ensemble calibration,
  compound-event, seasonality and time-frequency figure recipes.
  Use for Origin automation, 气象水文科研绘图、色标选择、Origin作图与图件精修.
metadata:
  short-description: Origin气象水文科研绘图、色标与可编辑图件
---

# Origin气象水文科研绘图

把用户的数据或已审查结果做成可编辑、可复现的科研图。原生Origin工程、导出图片和统计正确性分别验收；不把一种工具的输出冒称另一种。

## 先选最短路径

- **现有Origin图/CSV/Excel重绘**：读[Origin操作](references/originpro-workflow.md)，复用现有脚本；原生工作表、曲线、图层与OPJU是主要交付。
- **色标选择或下载**：读[色标指南](references/meteorology-hydrology-colors.md)，查`assets/palette_catalog.json`及[色标预览](assets/palette_atlas.png)。已附离线CSV和JASC PAL，不必重复联网。
- **常用图型**：读[图型配方](references/common-plots.md)；[合成示例图集](assets/common_plot_gallery.png)仅展示画法，不是观测结果。
- **模型诊断、概率集合、复合极端、季节性/小波**：按问题读取[新增12类期刊图型配方](references/journal-figure-recipes.md)。这是结合30篇新增论文整理的决策与Origin实现指南，不代表全部图型已有自动化模板。
- **导入前检查**：预计算的可靠度、FDC、lag合成和技能矩阵，先按[输入约定](references/data-contracts.md)运行只读检查；不自动修补缺失数据。
- **需要解释图型依据**：查[30篇文献索引](references/literature-30.md)，区分论文观察与本技能的实施选择，不把单篇论文的阈值、配色或坐标截断当作规范。
- **导出、字体、尺寸异常**：读[排障与本机经验](references/troubleshooting.md)，先做有界最小对照。若普通文字出现上划线、刻度正常，可用已验证的[原生数据标签替代法](references/native-text-workaround.md)；不盲改系统设置。
- **来源/再分发**：读[来源和许可](references/sources-and-licenses.md)，资产实际URL、版本/提交和SHA256在catalog及manifest中。

用户指定Origin时，统计图使用真实Origin后端。经纬度投影、复杂地理底图、矢量场若适合Cartopy/NCL等，说明选择并遵守用户指定后端；不强制把所有地图迁入Origin。Python示例图库的后端明确标为Matplotlib，不冒充Origin。

## 本轮工作契约

作图前用几句话明确：图要回答的问题；数据和变量/单位；比较对象和样本支持；区间/显著性含义；面板顺序；输出尺寸与格式。已有约定优先，不为了视觉或显著性改阈值、区域、时窗、样本或模型。

绘图只读已提供数据。核验键、缺失、单位、上下限和来源；不静默删行、补值或对称化区间。分类和颜色映射留表。原始效应、边界与模型拟合不随排版重算。需要新统计时另行说明，遵守用户计算位置与授权。

模型对比先确认配对样本与检验期；ECDF保留整体分布，配对差值说明谁改善。NSE/KGE的定义和基准单独标注；总分之外按研究问题检查高低流、时序或概率校准。区间、样本数和显著性掩膜直接读取上游结果，不在绘图时重新选择。

## Origin关键动作

1. 检查已有脚本/工程与Origin进程。通常创建独立实例；若本机已复现普通文字上划线，先读排障参考，在副本上对照普通文字与原生数据点标签。数据标签正常时可用原生文字层替代，不重复批量生成异常图。对自己的实例才可`op.new()`、`op.exit()`；连接用户实例退出用`op.detach()`，不清空、整体另存或关闭用户项目。正常手动实例只解决过部分图，不能保证所有旧工程正常。
2. 源表写入Audit表；绘图系列、单位和CI端点可追溯。若工作表没有联动公式，交付时说明修改Audit不会自动更新所有曲线。
3. 精确尺寸：**先`page.kar=0`，再设置`page.width/height`**；导出使用`tr.Margin:=2`，读取SVG/PDF成品尺寸核对。180mm只是常用双栏示例，不覆盖期刊要求。
4. 使用新目录/版本名，避免覆盖旧图；保存OPJU，再复开核对关键数值、元数据和实际曲线。
5. 同时检查原生图页和导出：字体、单位、正负号、零线、区间、图例、显著性、裁切和最终缩版可读性。保存成功不代表视觉完成。

## 色标与图形原则

- 非负量用顺序色标；有物理中点的距平/差值用发散色标；角度用循环色标；类别用离散色表。
- 色标、数值范围、分级边界、中心值和`extend`是不同选择。同变量可比较面板共用尺度；不各自自动拉伸制造差异。
- 单位和符号先于颜色：原始omega正值为下沉，若展示上升则显式用−omega；降水累计和速率不能混写；水汽辐合的正号要交代。
- 把缺测与零值区分。不得把NaN画成“无雨”、陆地或白色零距平。
- 现成NCL业务/传统多色表可用于复现既有风格，不宣传其全部感知均匀或适合灰度印刷。
- 固定组别颜色并辅助线型/符号。避免用彩虹编码无序类别或不必要的双Y轴、3D柱图。
- 点状覆盖可能表示p值、模式符号一致性或超出基准集合，必须明确命名；集合分位带不是均值置信区间，空概率箱不是0，Q95必须说明分位/超越约定。

## 可运行资源

在本skill目录运行，Python依赖按需要使用，不自动安装：

色表工具需NumPy；图集另需Matplotlib；Origin模板另需pandas、originpro及本机Origin。查看打包的PNG/PDF/PAL无需这些Python包。`build_palette_assets.py`按Matplotlib 3.11.0完成过构建；旧版本若没有`okabe_ito`，直接使用已打包色表，不为此自动升级环境。

```powershell
python scripts/palette_tools.py list
python scripts/palette_tools.py export --name cmocean_rain --levels 0 1 5 10 25 50 100 --out C:/work/rain_colors
python scripts/make_gallery.py --out C:/work/plot_gallery
python scripts/originpro_plot_template.py --out C:/work/origin_demo --synthetic
python scripts/check_plot_table.py --kind reliability --csv assets/journal_examples/reliability.csv
python -m unittest discover -s scripts -p "test_*.py"
```

示例分级不是WMO/CMA降水等级标准。`palette_tools`导出区间颜色表与PAL，但不自动修改Origin全局色库。图集全为固定种子的合成演示；实际论文必须替换为真实输入。Origin示例可以不导出图片，先验收原生项目；`--export-preview`才附自动化预览。

资产已离线打包。仅更新色标来源时用`build_palette_assets.py --allow-network --out <新资产目录>`；只取固定提交的数据/许可文本，不运行下载代码、不上传用户数据。

## 交付

导出前按[图件审查](references/figure-review.md)核对科学语义、样本支持、最终尺寸与原生工程。按任务交付OPJU、原图/源表、PNG及PDF/SVG、颜色/单位/区间说明。说明实际做了什么、哪些验证通过及是否还有渲染问题，不罗列无关工程日志。未经验证的因果箭头、显著性或预测技巧不能由美化补出。
