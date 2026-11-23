# C01 — 设计到实施规划的交接

`evidence_level: HISTORICAL-SOURCE-DERIVED`  
`snapshot_date: 2026-02-12`

某设计型 Skill 的工作流程如下：

1. 了解用户想做什么，逐步澄清约束和成功标准。
2. 按复杂度展示设计内容，并请用户逐节批准。
3. 将设计写入 `docs/plans/YYYY-MM-DD-<topic>-design.md` 并提交。
4. 然后立即调用另一个规划 Skill 编写详细实施计划。

流程图包含“用户是否批准设计？”这个判断，但位于“写入最终设计文件”之前。
下游规划 Skill 将新计划写在 `docs/plans/YYYY-MM-DD-<feature-name>.md`。

**任务：**从该流程本身判断它是否适合在用户无人干预时进行后续交接。不要假定它一定存在问题，也不要编写代码。
