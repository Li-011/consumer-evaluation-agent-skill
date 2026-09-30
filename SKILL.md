---
name: 02-consumer-agent-skill
description: >-
  Evaluate an e-commerce key-visual poster from upstream-locked consumer,
  purchase-motivation, and usage-scene tags. Return the fixed A-D JSON contract
  with a 0-10 score, pass decision, paired problems and revision instructions,
  protected content, and evaluation metadata. Do not generate posters,
  reclassify the target context, judge pure aesthetics, or control iterations.
license: MIT
metadata:
  author: xyu
  version: 1.1.0
  created: 2026-09-28
  last_reviewed: 2026-09-30
  review_interval_days: 90
---
# /02-consumer-agent-skill — 消费者海报评估

从主流程已经锁定的目标消费者视角，判断当前电商海报是否让该消费者看懂商品、理解利益、获得购买信息并愿意采取行动。只评估并返回一次 JSON；不生成海报，不控制重试，不调用美学 Agent。

## 外部合同

输入必须符合 `assets/schemas/input.schema.json`，仅包含：

```json
{
  "poster_image": "当前生成海报（图像）",
  "product_input": {
    "product_img": "原始商品图",
    "selling_points": ["卖点1", "卖点2"],
    "price_text": "价格文案",
    "marketing_target": "营销目标",
    "scene_tags": ["P人群", "M动机", "S场景"]
  }
}
```

`scene_tags` 必须正好三个元素，顺序固定为 P 人群、M 购买动机、S 使用场景。优先使用 `ID 名称`，例如 `P02 职场通勤人群`；同时兼容冻结字典中的完整名称。只解析并锁定标签，不重新分类。

输出必须是 `assets/schemas/output.schema.json` 定义的七字段 JSON。不要在 JSON 前后添加解释文字，也不要增加 `dimension_scores`、`failure_codes`、`CES`、`decision`、版本或上下文字段。

## 强制边界

1. 商品事实只来自 `product_img`、`selling_points`、`price_text` 和 `marketing_target`；不得补充未经输入支持的功效、参数或活动条件。
2. P-M-S 只改变判断视角，不改变五个维度和评分权重。读取 `references/evaluation-lenses.md`。
3. 纯配色、排版工艺、留白与字体协调交给美学 Agent；只有当它们影响消费者识别、理解或行动时才作为消费者问题。
4. A 主流程负责硬性合规、版本、日志、循环次数、重新生成和两个 Agent 的 `protected_content` 合并。
5. `problem_list[i]` 必须与 `modify_suggestion[i]` 一一对应，数组等长且最多三项。
6. `protected_content` 只包含与输入核对后已经正确的元素；错误、模糊或需要重做的内容不得保护。
7. 图片或必需输入无法解析时仍返回相同七字段 JSON，`score` 为 0、`pass` 为 false、`confidence` 为 0，不得输出 `INVALID_INPUT` 文本或伪造五维低分。

## 评估流程

### 1. 校验并锁定输入

运行 `scripts/validate_input.py` 或执行等价检查。确认海报、原始商品图、卖点、价格、营销目标与三个 P-M-S 标签可用。活动时间等要求只有明确写入 `marketing_target` 或其他输入字段时才可评估。

### 2. 先盲观察海报

在用商品信息补全理解前，仅记录海报实际可见内容：商品、品牌、核心利益、价格促销、使用情境和行动提示。不能把输入里有但海报未表达的信息当成已传达。

### 3. 对照事实与 P-M-S 视角

- P 人群主要决定信息接受习惯、关注点与表达门槛。
- M 动机决定什么利益和证据最有说服力。
- S 场景决定商品与使用环境是否建立真实联系。

案例库只作高、中、低表现的校准参考，不能因为画面风格相似就直接给高分。

### 4. 五维评分

读取 `references/rubric.md`。内部五维各取 0、1 或 2 分：

- `product_recognition`：商品与品牌识别；
- `benefit_clarity`：消费利益与卖点传达；
- `offer_visibility`：价格促销与活动信息；
- `population_scene_fit`：人群与场景适配；
- `purchase_drive`：购买信心与行动驱动。

```text
score = 五个维度之和
pass = score >= 7 且不存在关键问题
```

关键问题包括商品主体无法识别或与原图明显不一致、价格与输入冲突、出现未经输入支持的功效、核心卖点完全缺失，或营销目标明确要求的关键信息缺失。关键问题写入 `problem_list`，不增加新字段。

### 5. 形成可执行反馈

保留最影响购买判断的至多三个问题。每条建议必须说明具体改动，不得改变已核实的商品、价格、品牌和卖点事实。通过时允许保留轻微优化建议；若没有真实问题，两个数组均返回空数组。

### 6. 返回统一 JSON

使用 `scripts/score_evaluation.py` 对内部评分草稿进行确定性汇总。`meta` 只包含固定维度名称和置信度，供 A 记录实验日志，不参与流程判断。

## 异常结果

图片解析失败时返回：

```json
{
  "agent_name": "consumer_agent",
  "score": 0,
  "pass": false,
  "problem_list": ["海报图像解析失败"],
  "modify_suggestion": ["重新提供可读取的海报图像后再次评估"],
  "protected_content": [],
  "meta": {"judge_dimensions": [], "confidence": 0}
}
```

## 验证

```bash
python3 scripts/validate_input.py examples/nori-input.json
python3 scripts/score_evaluation.py examples/nori-draft-result.json
python3 scripts/run_evals.py
```
