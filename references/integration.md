# A-D 主流程接口

## 统一输入

消费者 Agent 和美学 Agent 接收相同的两个顶层字段：`poster_image` 与 `product_input`。消费者 Agent 不要求版本、轮次或上一轮结果。

`scene_tags` 固定为三项：

```text
0: P 人群
1: M 购买动机
2: S 使用场景
```

推荐传入 `ID 名称`。A 在后续迭代中必须重复传入完全相同的 P-M-S 标签；若营销目标改变，应建立新的评估轨道。

## 统一输出

消费者 Agent 与美学 Agent 使用相同七字段结构。A 只用 `score` 和 `pass` 控制流程；记录 `meta` 但不以它改变路由。

`problem_list` 和 `modify_suggestion` 按下标一一对应。A 将对应项组合成给生成模块的修改指令。

## 保护内容

A 应维护保护内容累积集合：

```text
protected_union = unique(
  consumer_agent.protected_content
  + aesthetic_agent.protected_content
)
```

统一 Agent 输入没有上一 Agent 的保护内容字段，因此不要要求美学 Agent自动继承消费者 Agent 的输出。A 在调用生成模块时传入合并后的列表。

## 流程边界

```text
硬性合规检查
→ Consumer Agent
→ pass=false: A 组织修改并重新生成
→ pass=true: 进入 Aesthetic Agent
→ A 合并保护内容并决定后续流程
```

每次重新生成后，A 重新执行硬性合规检查。消费者 Agent 不生成海报、不控制循环、不保存版本、不比较版本。

## 异常

任何异常仍返回统一 JSON。输入或图片不可评估时使用 `score: 0`、`pass: false`、空保护列表与 `confidence: 0`，不要把技术失败伪装成正常的消费者低分。
