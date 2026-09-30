# 02消费者Agent-skill 1.1

面向电商商品营销主视觉的消费者评估 Agent。它接收 A 主流程统一输入和 C 分类库输出的 P 人群、M 购买动机、S 使用场景标签，返回与美学 Agent 完全一致的七字段 JSON。

## 职责

- 评价目标消费者能否识别商品、理解卖点和交易信息并产生行动；
- 输出 0–10 分、通过判断、问题、修改建议和保护内容；
- 不重新分类 P-M-S，不生成海报，不评价纯美学，不控制迭代。

## 接口

输入结构见 `assets/schemas/input.schema.json`，输出结构见 `assets/schemas/output.schema.json`。`scene_tags` 固定为 `[P人群, M动机, S场景]`。

内部五维各 0–2 分，总分为五项之和。`score >= 7` 且没有关键问题时通过。

## 验证

```bash
python3 scripts/validate_input.py examples/nori-input.json
python3 scripts/score_evaluation.py examples/nori-draft-result.json
python3 scripts/run_evals.py
```

## 主流程边界

A 负责硬性合规、版本、日志、循环、重新生成和消费者/美学 Agent 保护内容的合并。详细规则见 `references/integration.md`。

## License

MIT
