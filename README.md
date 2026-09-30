# Origin 气象水文科研绘图技能 · 30篇文献增强版

本地增强日期：2026-09-30。技能入口为[python-origin-plotting/SKILL.md](python-origin-plotting/SKILL.md)。

本轮基于30篇新增期刊论文的方法、结果图与图注进行定向阅读；逐条记录论文观察、Origin应用建议与使用限制，不宣称完成论文复现或系统综述。文献来自HESS、GMD、BAMS、ESD、NHESS和NPG，覆盖2004—2026年；原技能已有的两篇色彩论文不计入30篇。

## 本轮增加

- 原12类基础图型加12类期刊诊断配方，覆盖技能ECDF、配对改进、portrait矩阵、概率校准、集合诊断、复合事件、干旱传播、圆形季节性、小波与故事线。
- [30篇文献证据索引](python-origin-plotting/references/literature-30.md)，含JSON及BibTeX。
- [Origin图型配方](python-origin-plotting/references/journal-figure-recipes.md)和[图件审查](python-origin-plotting/references/figure-review.md)。
- [四类只读表格检查与合成输入](python-origin-plotting/references/data-contracts.md)：可靠度、FDC、lag合成、技能矩阵。
- 保留25套色表、既有Origin点区间模板、原12面板Matplotlib教学图库、排障经验及第三方许可。

## 安装与使用

将完整`python-origin-plotting`目录复制到目标工具的skills目录；不要只复制SKILL.md。更新已有技能时先保留其副本，合并本地自定义修改。

Python输入检查沿用NumPy和pandas。原生绘图另需可用的Origin/OriginPro及`originpro`；现有Matplotlib示例图库与原生Origin工程有独立标识。

```powershell
cd python-origin-plotting
python -B -m unittest discover -s scripts -p "test_*.py"
python scripts/check_plot_table.py --kind reliability --csv assets/journal_examples/reliability.csv
```

## 验证边界

本轮执行离线代码、输入边界、文献完整性及资源链接检查。新增24类是图型知识与实施配方的总数；本轮没有批量启动Origin绘制24种原生图，也没有更新原图库的12面板图片。新增表格的区间都是合成演示，没有统计置信度声明。

论文全文和原图不随包分发。个人环境路径不属于发布内容。项目原创代码与文档采用 MIT 许可；第三方色表及许可文件按各自许可证使用，详见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
