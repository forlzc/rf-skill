# rf-skill 射频电路技能仓库

> A collection of reusable RF / 射频通信电路 skills for teaching, PPT figures, LearningTong(学习通) resources, and automated agents.

本仓库汇集用于《射频通信电路》课程教学的自动化技能（Skill）。每个子目录是一个独立、可复用、可跨设备安装的技能，供教师本人或其他贡献者通过 `git clone` 后在本地 WorkBuddy / Python 环境中调用、改进或提交 Pull Request。

## 已收录技能 Skills

| 技能 | 目录 | 说明 |
| --- | --- | --- |
| Smith Chart Engine | [`smith-chart-engine/`](smith-chart-engine/) | 可复用史密斯圆图绘制引擎：阻抗圆（实线）、导纳圆（虚线可开关）、刻度旋转标注、图片尺寸自适应网格密度、点/线/弧/驻波圆/波长移动操作，支持 PNG/SVG/PDF 输出。 |

## 快速开始 Quick Start

```bash
git clone https://github.com/forlzc/rf-skill.git
cd rf-skill/smith-chart-engine
pip install -e .
python examples/teaching_demo.py
```

## 贡献 Contributing

欢迎 Fork 后提交 Pull Request，新增射频相关的绘图、匹配、习题生成等技能。每个技能请保持独立目录与自身 `SKILL.md`、`README.md`、`tests/`，并在本文件“已收录技能”表格中登记。

## 许可 License

各技能目录内 `LICENSE` 文件为准（当前 Smith Chart Engine 采用 MIT License）。
