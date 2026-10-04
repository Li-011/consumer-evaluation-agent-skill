# 02消费者Agent-skill 1.5.0
接口A-D-2.0：A完整规范化输入、C style_guide、八组保护对象→消费者五维百分制、配对反馈、累计锁及回退记录。

```bash
python3 scripts/validate_input.py examples/a-to-d-input.json
python3 scripts/score_evaluation.py examples/nori-draft-result.json --context examples/nori-input.json --output consumer-result.json --details-output scoring-details.json
python3 scripts/run_evals.py
```

A调用组装器的用法和字段来源见references/integration.md。A 1.0保持Baseline；A 2.0需自行接入调用和重试逻辑。回归测试覆盖接口，未代替模型读图、真实重画或消费者实验。

模型提交25个子项档位和证据，程序自动计算五维和总分；不接受模型直接填写五维分数。明细留D内部，A-D-2.0正式输入输出不变。33项回归覆盖计算、输入错误和维度回退。examples/consumer-output-*.json为模拟接口示例，不是真实海报评测。
