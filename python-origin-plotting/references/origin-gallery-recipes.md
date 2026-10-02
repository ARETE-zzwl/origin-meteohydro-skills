# Origin图型参考与数据要求

以下为官方绘图参考，不作为科学结论的依据。结合[配色方法](scientific-color-recipes.md)选用；不要把图型丰富等同于增加装饰。模板只能决定画法，不能补出原数据不存在的分布、配对关系或误差范围。

| 官方实例 | 适合的证据 | 色彩与绘制 |
| --- | --- | --- |
| [嵌套条形](https://www.originlab.com/www/products/GraphGallery.aspx?GID=551) | 总体及其明确子集 | 同色浅底、深色内条，共同零点；子集不可再与总体堆叠求和。 |
| [经验累积分布](https://www.originlab.com/www/products/GraphGallery.aspx?GID=1637) | 完整事件或格点分布 | 颜色分组、线型辅助区分。注明是否加权，不改成平滑拟合分布。 |
| [雨云图](https://www.originlab.com/fileexchange/details.aspx?fid=773&v=0) | 有逐样本记录的分布比较 | 半小提琴加点；软件版本与负值分箱需检查。仅有均值与区间时不可使用。 |
| [半小提琴/分裂小提琴](https://docs.originlab.com/origin-help/create-violin-plot/) | 同变量的两组或多组样本 | 同一密度规则和可比较带宽；对称宽度并不表示样本量相同。 |
| [山脊图](https://www.originlab.com/www/products/GraphGallery.aspx?GID=632) | 一变量在多时段/类别中的分布 | 固定横轴与密度尺度。类别色与有序序列色分开选择。 |
| [棒棒糖/两端点组合](https://www.originlab.com/www/products/GraphGallery.aspx?GID=563) | 以零为基准的幅度或两个配对值 | 细连接、清楚点形；置信区间来自原结果，不用连接长度代替不确定性。 |
| [曲线间填色](https://www.originlab.com/www/products/GraphGallery.aspx?GID=609) | 合成轨迹、区间带、分量 | 主线深、填充浅；置信带、分位范围与物理组成分别说明。 |
| [分组箱线图](https://www.originlab.com/www/products/GraphGallery.aspx?GID=1621) | 原始样本的组间分布 | 箱体、须及异常值定义写图注；样本小的组显示实际点。 |
| [分面散点](https://www.originlab.com/www/products/GraphGallery.aspx?GID=436) | 个体配对值及组内关系 | 共用尺度优先；散点和摘要层分明，不能只有组均值却画出个体关系。 |
| [分裂单元热图](https://www.originlab.com/www/products/GraphGallery.aspx?GID=604) | 两组对齐的二维矩阵 | 两半单元格共享单位、色标、中心和范围；只在维度足够时使用。 |
| [风矢量时间条](https://www.originlab.com/www/products/GraphGallery.aspx?GID=1624) | 逐时或逐日风向风速 | 配参考箭头及方向约定；不代替有地理投影的地图矢量场。 |
| [多面板合并](https://www.originlab.com/www/products/GraphGallery.aspx?GID=1610) | 不同证据共同回答一个问题 | 统一字重、边距和分类色；按照阅读顺序布局，不强制每格等大。 |

## 本机可用与未验证的区别

2026-10-02在本机Origin安装目录确认存在HalfViolin.otpu、ViolinSplit.otpu、ViolinBox.otpu、ViolinData.otpu、ViolinStick.otpu、Ridgeline.otpu、Lollipop.otpu、Bullet.otpu等模板。其他机器先查实际安装目录。文件存在不等于已经对目标数据验证。

官方教学附件在本次网络环境返回403，因此仅保存网页入口；不要说这些ZIP已下载或已安装。随skill提供的四页参考册及OPJU是本地重新制作的合成示例，不含官方模板截图，也不含研究数据。

## 已实测的成品细节

- 保存后复开核对表格与完整DataPlots绑定；`plot_list()`在某些跨表系列组合中不完整，可用`layer.obj.DataPlots.GetCount()/GetItem()`核对。
- 极窄置信区间可能被空心符号的白色填充遮住；先画点，再将真实区间线放在上层，不能人为拓宽区间。
- 多组分堆叠仅在分量可相加且单位一致时使用。总量置信区间应来自总量估计，不能直接相加分量区间。
- 原生SVG与PDF在本机曾出现系列显示不一致，必须各自渲染检查。必要时保留原生SVG供追溯，以完整Origin PDF转换最终SVG；设置显式pt单位，检查图页尺寸与无栅格嵌入。
- PDF补嵌字体时保留原绘图内容流；缺少Unicode文本提取不代表字形丢失，仍检查实际渲染。字体需满足本机授权及嵌入限制。
