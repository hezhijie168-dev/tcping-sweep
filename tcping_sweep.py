#!/usr/bin/env python3
"""全国 31 省三网 TCP-Ping 批量测试（节点：<省码>-<运营商码>-v4.ip.zstaticcdn.com:80）
用法: python3 tcping_sweep.py [省份代码...]   # 无参数=全部93节点; 例: gd bj sh
输出: 每节点 3 次 TCP 建连耗时中位数；末尾按运营商汇总平均值。
注意: 测的是到测试节点的 TCP 建连延迟，不是完整回程线路质量。"""
import socket, statistics, sys, time, concurrent.futures

PROVINCES = {
    "bj": "北京", "tj": "天津", "sh": "上海", "cq": "重庆", "he": "河北",
    "sx": "山西", "ln": "辽宁", "jl": "吉林", "hl": "黑龙江", "js": "江苏",
    "zj": "浙江", "ah": "安徽", "fj": "福建", "jx": "江西", "sd": "山东",
    "ha": "河南", "hb": "湖北", "hn": "湖南", "gd": "广东", "hi": "海南",
    "sc": "四川", "gz": "贵州", "yn": "云南", "sn": "陕西", "gs": "甘肃",
    "qh": "青海", "nm": "内蒙古", "gx": "广西", "xz": "西藏", "nx": "宁夏",
    "xj": "新疆",
}
CARRIERS = {"ct": "电信", "cu": "联通", "cm": "移动"}


def probe(code):
    p, c = code.split("-")
    host = f"{p}-{c}-v4.ip.zstaticcdn.com"
    times = []
    ip = None
    for _ in range(3):
        try:
            infos = socket.getaddrinfo(host, 80, socket.AF_INET, socket.SOCK_STREAM)
            ip = infos[0][4][0]
            t0 = time.perf_counter()
            s = socket.create_connection((host, 80), timeout=3)
            times.append((time.perf_counter() - t0) * 1000)
            s.close()
        except Exception:
            pass
    med = round(statistics.median(times), 1) if times else None
    return (PROVINCES[p], CARRIERS[c], host, ip, med, len(times))


def main():
    provs = sys.argv[1:] or list(PROVINCES)
    codes = [f"{p}-{c}" for p in provs for c in CARRIERS]
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
        rows = list(ex.map(probe, codes))
    rows.sort(key=lambda r: (r[4] is None, r[4]))
    for name, car, host, ip, med, ok in rows:
        print(f"{name:6} {car:4} {host:34} {str(ip):16} "
              f"{(str(med) + ' ms') if med is not None else '超时/不可达':10} ({ok}/3)")
    for car in CARRIERS.values():
        vals = [r[4] for r in rows if r[1] == car and r[4] is not None]
        if vals:
            print(f"汇总 {car}: 平均 {round(statistics.mean(vals), 1)} ms, "
                  f"最快 {min(vals)} ms, 最慢 {max(vals)} ms, 可达 {len(vals)}/{len(rows) // 3}")


if __name__ == "__main__":
    main()
