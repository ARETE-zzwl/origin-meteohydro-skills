# 普通文字上划线的原生替代方法

## 适用条件与证据

本机OriginPro 2024 10.100178、originpro 1.1.15、OriginExt 1.2.5中，普通图形文字出现上划线，刻度正常。同一最小图内，散点的自定义数据标签正常。`@TO=0/1/2`及`label -fpp *`没有消除普通文字的异常，不重复这些尝试。

2026-09-30实测：在独立实例中，为四张论文图添加透明原生文字层；22、29、12、17个文字对象分别替代。原74张数据表和全部科学曲线绑定未变；另存OPJU、退出自己的实例、重开后导出，PNG、PDF、SVG实际渲染通过。未修改许可、注册表或用户未保存工程，未擦除图片线条或栅格覆盖文字。

## 坐标与文字

保留原对象的文字、字体、颜色、旋转和包围框。对已明确的外层`\f:Arial(...)`与`\b(...)`取纯文本和粗体标志；不要用一般正则盲删富文本、上下标或希腊字母。未处理的转义先做单标签试验。

包围框的left/top/width/height与page.width/height若为同一导出像素尺度，标签中心转换为页面毫米坐标：

```python
x = (left + width / 2) * 25.4 / graph.get_float('resX')
y = (page_height - top - height / 2) * 25.4 / graph.get_float('resY')
```

先读取实际单位，不能将对象的x1/y1一概当作页面包围框中心。位置是初始锚点，仍需检查对齐、长标题和旋转文字。

## 已实测的命令组合

以下片段使用已有`graph`和新的原生`worksheet`。每条记录含`text,x,y,size,color,bold,angle`，颜色使用Origin整数值。例子仅接收不含双引号、反斜线、换行的单行纯文本；其他文字需先验证转义。

```python
overlay = graph.add_layer()
overlay.name = 'NativeText'
overlay.lt_exec('layer.fixed=1; layer.factor=1; layer.unit=0; '
    'layer.left=0; layer.top=0; layer.width=100; layer.height=100; '
    'layer.color=0; layer.border=0; layer.clip=0; '
    'layer.x.showAxes=0; layer.y.showAxes=0; '
    'layer.x.showLabels=0; layer.y.showLabels=0; '
    'label -r legend; label -r xb; label -r yl;')
overlay.set_xlim(0, page_width_mm)
overlay.set_ylim(0, page_height_mm)
for j, record in enumerate(records):
    text = record['text']
    assert not any(c in text for c in ['"', '\\', '\n'])
    worksheet.from_list(2*j, [record['x']])
    worksheet.from_list(2*j+1, [record['y']])
    plot = overlay.add_plot(worksheet, colx=2*j, coly=2*j+1, type='s')
    plot.set_cmd('-k 1', '-z 0.01', '-c 0', '-q 1', '-qm 5',
        f'-qms "{text}"', '-qp 1', f'-qs {record["size"]}',
        '-qf font(Arial)', '-qu 0', '-qi 0', f'-qb {record["bold"]}',
        f'-qc {record["color"]}', f'-qr {record["angle"]}',
        '-qx 0', '-qy 0', '-qw 0')
```

**不能把`-k 1`改成`-k 0`来隐藏锚点。** 本机`-k 0`会连数据标签一起隐藏，尽管`-q 1`已设置。使用0.01大小、颜色0的微小透明符号，逐图检查无可见锚点。

垂直轴标题的已测旋转为90度。绘制成功后将原对象`label.show=False`，不删除，以保留内容与布局来源。文字记录另存Audit表，XY锚点放另一工作表，不混进科学数据表。

## 保存和编辑

- 保存新版本，退出自己的实例，独立重开后重新导出；逐格式验收，不能由PNG推定PDF或SVG通过。
- 用`DataPlots.GetCount()`与`GetItem(i)`核对所有原科学系列；仅额外增加文字层。不以一份短的迭代列表代替完整绑定核验。
- 文字仍是原生Origin对象：在NativeText层对应散点的Plot Details → Label → Custom Format中编辑；XY表控制锚点。Audit表是记录，修改它不会自动同步自定义标签。
- 旧普通文字仍隐藏，改旧文字也不会同步新标签。页面尺寸变化后重新计算锚点并检查位置。
- 方法不是Origin渲染器的根因修复，不宣称对所有字体、数学富文本或版本通用。单页替代仍异常时停止批量改写，保留原工程并报告具体失败格式。
