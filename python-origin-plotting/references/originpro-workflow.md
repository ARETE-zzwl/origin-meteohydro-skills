# Origin原生工作流

Python外部`originpro`依赖Windows、Origin和可用许可。读取现有脚本，优先小改。先查进程，不关闭所有Origin；不要对已attach的用户工程调用`new()`或`exit()`。独立实例的初始化也放在try/finally内。外部默认实例与用户手动实例不能混淆。

## 已验证的基础写法

```python
import originpro as op
try:
    op.set_show(False)             # 独立外部实例，不先attach
    op.new()
    wb = op.new_book(lname='Source data')
    wb[0].from_df(data)
    gp = op.new_graph(template='Origin')
    gp.lt_exec('page.kar=0; page.width=180/25.4*page.resX; '
               'page.height=140/25.4*page.resY; page.color=1;')
    gl = gp[0]
    plot = gl.add_plot(wb[0], colx=0, coly=1, type='l')
    plot.color = '#296795'
    plot.set_cmd('-wp 1.2', '-d 0')
    gl.rescale()
    op.save(str(output / 'figure.opju'))
finally:
    op.exit()                     # 仅自己的实例
```

图页实际宽=page.width/page.resX英寸。默认锁纵横比时，先设宽再设高会改掉宽；关闭本图页kar后再设两维。独立实例的模板扩展名用小写`.otp/.otpu`（旧originpro对`.OTP`有大小写检查问题，Windows文件本身不区分）。

## 线与字

- `-wp 1.1`是点为单位的线宽；`-w`使用不同单位，不混用。`-d 0`实线，`-d 1`虚线。
- `symbol_kind=2`圆、1方、5菱形、3三角；`-kf 0`实心，1空心。不同版本应先验收小样。
- 本机10.100178中`layer.tickL=3`给出合理刻度；不要机械套用其他版本单位。
- `layer.x.showLabels=0`隐藏分类轴原数字。字号通常7–9pt，按最终尺寸检查；不把屏幕放大显示当印刷可读性。
- 可用单行`\f:Arial(text)`；本机跨换行富文本出现字体泄漏及尾括号，优先独立文字对象或简洁单行标签。上下标用Origin原生转义并检查输出。
- 文字附着`attach=2`后以`x1/y1`放在轴坐标。全页文字须显式换算，不能把未知的left/top单位当页百分比。

## 点区间图与森林图

保留lo、hi而不是只保留一个标准误。可使用原生误差棒；若API难稳定实现非对称区间，允许用原生XY端点曲线加点图。上下/左右端点分别取原lo/hi，用NaN分段，不连成错误折线。新增显示错位只改变display_x/display_y，不改事件lag或估计。跨0区间仍完整显示。

若Audit、Series、CI为复制表，必须说明不自动联动。保存后复开检查所有工作表的行数、值、样本/类别信息与图层绑定，不只看文件非空。

## 导出

本机独立COM曾出现文字上划线。用户正常启动的实例已经使两张演变图的PNG/PDF恢复，但另三张旧图仍异常；详见排障参考，不能把attach当作通用修复。

需要沿用正常实例时，先确认进程和现有页，直接`op.attach()`，不要先`op.new()`或用`op.open()`替换当前项目。只在确需载入且无同名页时，用`doc -a "完整工程路径";`追加已审查的工程；可能出现新文件夹确认框，不盲等或重复追加，也不为绕开弹窗修改全局偏好。读取追加后的真实页名，避免工作簿与图页重名自动改名。已有图页就直接导出；结束`op.detach()`，不调用`op.save()`保存整个用户项目。

```python
gp.activate()
gp.lt_exec('doc -uw;')
gp.lt_exec(f'expgraph -sw type:=png filename:="figure" path:="{output}" '
           'overwrite:=rename tr.Margin:=2 tr1.Unit:=2 tr1.Width:=2400;')
```

SVG宽高常用英寸，读属性乘25.4；容许像素/小数取整误差，示例容差0.2mm。PDF也核对MediaBox；PNG固定2400px不自动意味着目标DPI。按期刊调整；不覆盖未审查文件。中文路径失败时才采用已授权ASCII目录或副本，不默认创建全局盘符/连接。

官方参考：[page属性](https://docs.originlab.com/labtalk/ref/page-obj/)、[导出参数](https://docs.originlab.com/origin-help/settings-in-expgraph-dailog/)、[外部色标导入](https://docs.originlab.com/quick-help/use-external-color-palette/)。
