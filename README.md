# tcping-sweep — 全国 31 省三网 TCP-Ping 批量测速

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Python: 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)
![No dependencies](https://img.shields.io/badge/dependencies-none-green)

> **English summary:** A zero-dependency Python tool that TCP-pings test nodes
> in all 31 Chinese provinces across the three major carriers (China Telecom /
> China Unicom / China Mobile) — 93 endpoints in total — and reports the median
> TCP connect latency per node plus a per-carrier summary.

一个零依赖的 Python 小工具：对全国 31 省 × 三网（电信 / 联通 / 移动）共 93 个
测试节点做 TCP 建连测速，输出每节点的 3 次建连耗时中位数，末尾按运营商汇总。

## 用途 / What it does

- 快速摸清当前网络到各省三网节点的 TCP 建连延迟分布。
- 挑出口、挑节点、排障时，先拿一组可复现的延迟数字再做决定。
- 注意：测的是到测试节点的 **TCP 建连延迟**，不是完整回程线路质量，
  也不是带宽；延迟低不等于下载快。

## 安装 / Install

零依赖，只需 Python 3.8+，标准库即可运行：

```bash
git clone https://github.com/hezhijie168-dev/tcping-sweep.git
cd tcping-sweep
python3 tcping_sweep.py
```

## 用法 / Usage

```bash
# 全部 93 个节点（31 省 x 3 运营商）
python3 tcping_sweep.py

# 只测指定省份（省份代码见下表）
python3 tcping_sweep.py gd bj sh
```

省份代码：`bj` 北京、`tj` 天津、`sh` 上海、`cq` 重庆、`he` 河北、`sx` 山西、
`ln` 辽宁、`jl` 吉林、`hl` 黑龙江、`js` 江苏、`zj` 浙江、`ah` 安徽、`fj` 福建、
`jx` 江西、`sd` 山东、`ha` 河南、`hb` 湖北、`hn` 湖南、`gd` 广东、`hi` 海南、
`sc` 四川、`gz` 贵州、`yn` 云南、`sn` 陕西、`gs` 甘肃、`qh` 青海、`nm` 内蒙古、
`gx` 广西、`xz` 西藏、`nx` 宁夏、`xj` 新疆。

运营商代码：`ct` 电信、`cu` 联通、`cm` 移动。
节点地址格式：`<省码>-<运营商码>-v4.ip.zstaticcdn.com:80`。

## 示例输出 / Example output

```
广东     移动   gd-cm-v4.ip.zstaticcdn.com       123.45.67.89    12.3 ms    (3/3)
广东     电信   gd-ct-v4.ip.zstaticcdn.com       123.45.67.90    18.7 ms    (3/3)
广东     联通   gd-cu-v4.ip.zstaticcdn.com       123.45.67.91    超时/不可达  (0/3)
汇总 移动: 平均 24.1 ms, 最快 8.2 ms, 最慢 61.4 ms, 可达 29/31
汇总 电信: 平均 27.8 ms, 最快 9.1 ms, 最慢 73.0 ms, 可达 30/31
汇总 联通: 平均 26.5 ms, 最快 10.4 ms, 最慢 58.9 ms, 可达 30/31
```

（以上为格式示例，非实测数据；`(3/3)` 表示 3 次建连全部成功。）

## 许可 / License

MIT（见 LICENSE）。
