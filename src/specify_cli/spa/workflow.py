# -*- coding: utf-8 -*-

"""Workflow definition loader for AnkerSPA."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List

from .simple_yaml import load_simple_yaml


@dataclass(frozen=True)
class StageDefinition:
    key: str
    label: str
    agent: str
    depends_on: List[str]
    outputs: List[str]
    human_review_enabled: bool
    human_review_prompt: str
    final_stage: bool


@dataclass
class WorkflowDefinition:
    stages: Dict[str, StageDefinition]

    def ordered_stages(self) -> List[StageDefinition]:
        indegree: Dict[str, int] = {key: 0 for key in self.stages}
        adjacency: Dict[str, List[str]] = {key: [] for key in self.stages}

        for key, stage in self.stages.items():
            for dep in stage.depends_on:
                if dep not in self.stages:
                    raise ValueError(f"Workflow 阶段 {key} 依赖未知阶段 {dep}")
                indegree[key] += 1
                adjacency[dep].append(key)

        queue: List[str] = [key for key, degree in indegree.items() if degree == 0]
        queue.sort()

        order: List[StageDefinition] = []
        while queue:
            current_key = queue.pop(0)
            order.append(self.stages[current_key])
            for neighbor in sorted(adjacency[current_key]):
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        if len(order) != len(self.stages):
            raise ValueError("Workflow 存在循环依赖，无法拓扑排序")

        return order


def _parse_list(value: object, *, field: str, stage_key: str) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list) and all(isinstance(item, str) for item in value):
        return list(value)
    raise ValueError(f"Workflow 阶段 {stage_key} 字段 {field} 必须是字符串列表")


def load_workflow_definition(path: Path) -> WorkflowDefinition:
    data = load_simple_yaml(path)
    stages: Dict[str, StageDefinition] = {}

    for key, value in data.items():
        if not isinstance(value, dict):
            raise ValueError(f"Workflow 配置阶段 {key} 需要映射结构")
        label = str(value.get("label", key))
        agent = str(value.get("agent", ""))
        depends_on = _parse_list(value.get("depends_on"), field="depends_on", stage_key=key)
        outputs = _parse_list(value.get("outputs"), field="outputs", stage_key=key)
        human_review_enabled = bool(value.get("human_review_enabled", False))
        human_review_prompt = str(value.get("human_review_prompt", ""))
        final_stage = bool(value.get("final_stage", False))

        stages[key] = StageDefinition(
            key=key,
            label=label,
            agent=agent,
            depends_on=depends_on,
            outputs=outputs,
            human_review_enabled=human_review_enabled,
            human_review_prompt=human_review_prompt,
            final_stage=final_stage,
        )

    if not stages:
        raise ValueError("Workflow 配置为空")

    return WorkflowDefinition(stages=stages)


__all__ = ["StageDefinition", "WorkflowDefinition", "load_workflow_definition"]


