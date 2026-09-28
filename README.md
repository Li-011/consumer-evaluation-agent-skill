# Consumer Evaluation Agent Skill 1.0

面向电商商品营销主视觉的消费者评估 Agent。它接收上游锁定的“宏观人群 × 购买动机”，用固定 A–E 量表评价海报，并向主流程返回 `PASS` 或可执行的 `ITERATE` 指令。

## 1.0 核心协议

- 8 类宏观人群 × 6 类购买动机，共 48 种消费者上下文；
- 统一评价 Attention、Relevance、Clarity、Value、Desire；
- 五项固定等权，购买动机只改变评价 lens；
- 先选 1–5 Anchor，再转换为 20/40/60/80/100；
- `CES >= 80` 且所有单项 `>= 65` 才能 PASS；
- 未通过时返回 Failure Code、诊断、修改动作、回退步骤和保护内容；
- 消费者评价通过后再进入美学 Agent。

## 仓库结构

```text
SKILL.md                         Agent 主协议
AGENTS.md                        跨工具入口
assets/taxonomy.json             8 × 6 taxonomy
assets/rubric.json               固定 A–E 评分规则
assets/failure-codes.json        失败代码与回退路由
assets/schemas/                  输入输出 JSON Schema
references/                     评价 lens、rubric 和主流程接口
scripts/                         校验、计分、版本比较和回归测试
examples/                        NORI 保温杯示例
evals/                           1.0 黄金测试定义
```

## 快速开始

```bash
python3 scripts/validate_input.py examples/nori-input.json
python3 scripts/score_evaluation.py examples/nori-draft-result.json --output /tmp/nori-final.json
python3 scripts/compare_versions.py examples/nori-v1-result.json examples/nori-v2-result.json
python3 scripts/run_evals.py
```

## 接入主流程

```text
用户与场景分类
→ 海报生成
→ 硬性合规检查
→ Consumer Evaluation Agent
→ PASS: Aesthetic Agent
→ ITERATE: Failure Code 路由回设计流程
```

完整接口见 `references/integration.md`。

## 安装

把仓库克隆到支持 Agent Skills 标准的技能目录，或运行：

```bash
./install.sh
```

安装后使用 `/consumer-evaluation-agent` 调用。

## 版本演进

1.0 的 taxonomy、等权量表和阈值是 Benchmark 基线。后续版本如需修改，必须保留旧配置和回归结果，不能覆盖后再比较。

## License

MIT

