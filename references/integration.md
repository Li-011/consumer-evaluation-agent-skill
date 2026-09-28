# Main Workflow Integration

## 调用条件

只有在硬性合规检查通过后调用消费者 Agent。若商品、Logo、价格、活动时间、文案或格式存在事实错误，先返回生成环节修复。

## 锁定字段

首次评价前冻结：

- taxonomy version；
- macro segment；
- purchase motivation；
- product facts；
- rubric version；
- pass threshold。

后续版本不得修改这些字段。若业务确实需要改变目标人群，建立新的测试轨道，不与旧版本计算 Delta。

## 路由

```text
合规通过
→ Consumer Evaluation
→ PASS: Aesthetic Evaluation
→ ITERATE: 按 failure code 返回指定设计步骤
→ 生成新版本
→ 使用相同锁定上下文再次 Consumer Evaluation
```

## 保护机制

每条修改动作必须包含 `protected_content`。下游不得为了修复一个低分维度而改变已经确认的商品外观、Logo、价格、活动时间或已经通过的关键信息。

## 日常开发与正式测评

- 日常开发：每个版本运行一次，快速定位 Failure Code。
- 正式测评：同一输入独立运行三次，保存原始结果，以维度中位数形成正式分数；若同一维度极差超过 40 分，标记 `REVIEW_REQUIRED`。

模型评分是模拟消费者判断，不是真实用户实验结果。报告中不得将 CES 表述为真实点击率或购买率。

