# 来源、版本与许可

本地整理于2026-09-29。`assets/palette_catalog.json`记录色表来源URL、固定提交、文件名及SHA256；`assets/manifest.json`记录原始色表、转换资产、许可等文件哈希。图集为本地合成数据，不能作为科研结果引用。

## 色表来源

|来源|本包收录|版本/提交|许可文件|
|---|---|---|---|
|[Matplotlib](https://matplotlib.org/stable/users/explain/colors/colormaps.html)|viridis、cividis、magma、Blues、YlGnBu、YlOrRd、RdBu_r、BrBG、PuOr、twilight、okabe_ito、tab10|本机3.11.0|`assets/licenses/matplotlib.txt`（含随发行版附带的第三方声明）|
|[cmocean](https://matplotlib.org/cmocean/)|rain、thermal、speed、balance、delta、phase|`59c35002c3aa5296b65d9646e52604c627441eb6`|`assets/licenses/cmocean.txt`，MIT；Kristen M. Thyng|
|[Scientific Colour Maps / cmcrameri](https://github.com/callumrollo/cmcrameri)|batlow、vik|`78f02a088fa3c4fb4cb8aa92bd8e52389ab9d09a`；此包装库标为SCM 8.0，不冒称官网更新版|`assets/licenses/cmcrameri.txt`，MIT；Fabio Crameri / Callum Rollo|
|[NCAR NCL](https://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml)|precip_11lev、precip_diff_12lev、BlueWhiteOrangeRed、WhiteBlueGreenYellowRed|`8f9e9476281cc6f6d9d12eaa78729c7003ca24b7`|`assets/licenses/ncl.txt`及`Apache-2.0.txt`；UCAR。原RGB文件的MeteoSwiss等来源注释完整保留|
|本地固定组别色|heat_rain_roles|本次选定的5个RGB值|这些本地色值按CC0-1.0提供；不是WMO/CMA或领域标准|

转换说明：源RGB不修改；浮点色表按`round(255×RGB)`量化为8-bit RGB；Matplotlib连续色表取256个位置、类别表保留原色数；NCL整数色表原样转换。CSV、JASC PAL是衍生格式，原始下载文件在`assets/raw/`。不对传统离散色表悄悄增加颜色或插值。打包内容不包含cmocean/cmcrameri/NCL可执行代码。

NCL根LICENSE是Apache许可声明，因此另附Apache 2.0全文。各第三方许可独立适用，不把整个合集重新宣称为同一个许可证。若将色标再分发，保留这些许可、来源和转换说明。`matplotlib.txt`是本机发行版完整声明，包含未被本包使用的附带组件声明；不因此声称本包含有这些组件。

## 学术参考

- Thyng et al. (2016), *True Colors of Oceanography: Guidelines for Effective and Accurate Colormap Selection*. [DOI](https://doi.org/10.5670/oceanog.2016.66)。用于cmocean及感知友好配色方法的引用。
- Crameri, Shephard & Heron (2020), *The misuse of colour in science communication*. [DOI](https://doi.org/10.1038/s41467-020-19160-7)。用于科学色标选择原则；使用SCM数据时按[作者官网](https://www.fabiocrameri.ch/colourmaps/)引用实际版本。
- [Matplotlib归一化说明](https://matplotlib.org/stable/users/explain/colors/colormapnorms.html)：色表与Normalize、TwoSlopeNorm、BoundaryNorm不是一回事。

## Origin官方参考

- [外部色标导入](https://docs.originlab.com/quick-help/use-external-color-palette/)：支持JASC ASCII PAL。
- [Color Manager](https://docs.originlab.com/origin-help/color-manager/)：短色表可作为Color List导入。
- [page属性](https://docs.originlab.com/labtalk/ref/page-obj/)与[导出设置](https://docs.originlab.com/origin-help/settings-in-expgraph-dailog/)：尺寸、纵横比与页边界导出。

## 本机经验的适用范围

旧skill已单独备份；本次入口和脚本为重新组织的版本，保留Python驱动Origin的用途，增加气象水文资产及验证。工程案例只整理操作经验，不携带Heat→Rain研究数据。已知独立COM导出上划线问题归入本机版本经验；用户手动打开对照工程显示正常，不能据此推断许可问题或所有Origin版本存在同一故障。

## 本次验证

### 2026-09-30：新增30篇期刊论文学习

新增[文献索引](literature-30.md)、[机器可读元数据](literature-30.json)和[BibTeX](literature-30.bib)。30个唯一DOI经过出版方/Crossref核验，包含方法、结果图与图注的定向阅读定位；不重复计入原来两篇色彩论文。论文观察与本技能的应用推断分别记录。

不附论文全文或论文原图，新增CSV均为手写合成教学输入。原25套色表、原始来源和第三方许可不变。新增配方为操作指南，未声称24类图型均已做Origin原生自动化。

### 既有验证记录（保留其日期与限制）

2026-09-29：13项离线测试通过，覆盖RGB/PAL往返、25套CSV/PAL一致性和哈希、离散边界、区间端点、资源链接及许可文件。Origin 10.100178原生模板完成7行合成数据、2条图形对象的保存与复开核对；自动预览仍复现本机上划线现象，未将其作为合格投稿图片。25套色标总览和12面板合成图集由Matplotlib生成，已目视检查。skill入口通过官方`quick_validate.py`；Windows中文环境使用`python -X utf8`运行该验证器。
