# Origin输入检查与合成示例

用途：在导入Origin前发现会改变科学含义的数据编码错误。脚本只读，不重算指标、不插值、不排序、不删行、不选显著结果。通过表示规定的表结构检查通过，不代表统计正确、样本独立或图件已验证。

## 四类输入表

| `--kind` | 必需字段 | 关键边界 | 对应配方 |
|---|---|---|---|
| `reliability` | `bin_left, bin_right, mean_probability, event_frequency, n` | 概率[0,1]；箱不重叠；n为非负整数；空箱的两种概率必须留空 | R16 |
| `fdc` | `exceedance_pct, discharge` | 概率严格递增且位于(0,100)；非负流量单调不增；0保留并报告不能用普通log Y | 基础FDC、R24 |
| `composite` | `lag, estimate, lo, hi, n` | 单系列lag递增；有支持时端点有限且lo≤hi；n=0时估计/端点留空 | R20 |
| `portrait` | `model, metric, reference, value, better, status` | 单元键不重复；方向一致；缺失单元的值留空；负技能允许 | R15 |

规则适用于本页定义的交换格式。其他合法统计格式（例如采用0/100端点的理论FDC）应显式转换或使用另一个经核对的格式，不能为通过检查私自删改数据。

`portrait`的`better`为`higher`或`lower`，`status`为`available`或`missing`。一个CSV可包含多个指标，但不同原始单位不能直接共用色标；上游完成标准化时另给公式。缺失单元不能取0；重复单元不能交给热图工具自动求平均。

`composite`不会强迫`lo ≤ estimate ≤ hi`，因为某些区间估计可不包含点估计。若需要进一步核验，应核对上游方法，不能移动点或对称化端点。该表中的空行统计量不能直接送入只接受完整点区间的旧Origin模板；应选择支持缺测断线的原生图层或明确分段。

## 使用

在本skill目录执行，依赖沿用NumPy与pandas：

```powershell
python scripts/check_plot_table.py --kind reliability --csv assets/journal_examples/reliability.csv
python scripts/check_plot_table.py --kind fdc --csv assets/journal_examples/fdc.csv
python scripts/check_plot_table.py --kind composite --csv assets/journal_examples/composite.csv
python scripts/check_plot_table.py --kind portrait --csv assets/journal_examples/portrait.csv
python -B -m unittest discover -s scripts -p "test_*.py"
```

成功返回JSON与退出码0；检查失败返回非0退出码。CSV空字段表示缺失；标识列中的字面量`NA`仍是合法名称。每个数值字段必须能转换为数字；无限值不作为可绘制值接受。

## 示例不是研究结果

[示例元数据](../assets/journal_examples/metadata.json)及[reliability](../assets/journal_examples/reliability.csv)、[FDC](../assets/journal_examples/fdc.csv)、[composite](../assets/journal_examples/composite.csv)、[portrait](../assets/journal_examples/portrait.csv)均为本地手写合成演示，没有从论文提取数据。

特意保留四种边界：空概率箱、零流量、缺少支持的lag、负NSE及缺失参考单元。制作示例图时应让这些边界正确显示，不能为了“图更完整”自动填补。图注标“SYNTHETIC / 仅演示”，并说明区间没有统计覆盖率含义。

## 仍需人工核对的元数据

脚本不验证：观测/模拟是否正确配对、独立样本定义、率定与检验是否泄漏、单位、时间区间、事件阈值、分箱边界包含规则、置信水平、标准化基准、时空权重、地理投影和论文统计方法。使用这些表前，仍需完成[图件审查](figure-review.md)。
