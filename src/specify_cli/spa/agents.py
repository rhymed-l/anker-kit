# -*- coding: utf-8 -*-

"""Activity Agent definitions for AnkerSPA."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from rich.console import Console

from .simple_yaml import load_simple_yaml


@dataclass
class AgentConfig:
    """In-memory representation of ``metadata.yaml`` for an Activity Agent."""

    id: str
    name: str
    kind: str
    version: str
    description: str
    inputs: List[str]
    outputs: List[str]
    root: Path

    @property
    def metadata_path(self) -> Path:
        return self.root / "metadata.yaml"

    @property
    def prompt_path(self) -> Path:
        return self.root / "prompt-template.md"

    @property
    def checklist_path(self) -> Path:
        return self.root / "checklist.yaml"


def _coerce_list(raw: object, *, field: str, agent_id: str) -> List[str]:
    if raw is None:
        return []
    if isinstance(raw, list) and all(isinstance(item, str) for item in raw):
        return list(raw)
    raise ValueError(f"Agent {agent_id} metadata 字段 {field} 必须是字符串列表")


def load_agent_registry(spa_root: Path) -> Dict[str, AgentConfig]:
    registry: Dict[str, AgentConfig] = {}
    aa_root = spa_root / "AA"
    if not aa_root.is_dir():
        return registry

    for subdir in sorted(aa_root.iterdir()):
        if not subdir.is_dir():
            continue
        metadata_file = subdir / "metadata.yaml"
        if not metadata_file.exists():
            continue
        data = load_simple_yaml(metadata_file)
        try:
            agent_id = str(data["id"])
            name = str(data.get("name", agent_id))
            kind = str(data.get("kind", ""))
            version = str(data.get("version", "0.0.0"))
            description = str(data.get("description", ""))
            inputs = _coerce_list(data.get("inputs"), field="inputs", agent_id=agent_id)
            outputs = _coerce_list(data.get("outputs"), field="outputs", agent_id=agent_id)
        except KeyError as exc:
            raise ValueError(f"Agent metadata 缺少必要字段 {exc} at {metadata_file}") from exc

        registry[agent_id] = AgentConfig(
            id=agent_id,
            name=name,
            kind=kind,
            version=version,
            description=description,
            inputs=inputs,
            outputs=outputs,
            root=subdir,
        )

    return registry


class ActivityAgent:
    """Base class implementing generic helpers for Activity Agents."""

    def __init__(
        self,
        spa_root: Path,
        config: AgentConfig,
        *,
        console: Console | None = None,
    ) -> None:
        self.spa_root = spa_root
        self.config = config
        self.console = console

    @property
    def input_paths(self) -> List[Path]:
        return [self.spa_root / path for path in self.config.inputs]

    @property
    def output_paths(self) -> List[Path]:
        return [self.spa_root / path for path in self.config.outputs]

    def ensure_inputs(self) -> None:
        missing = [path for path in self.input_paths if not path.exists()]
        if missing:
            missing_text = ", ".join(str(path.relative_to(self.spa_root)) for path in missing)
            raise FileNotFoundError(f"{self.config.id} 依赖的输入缺失: {missing_text}")

    def prepare_output_directories(self) -> None:
        for path in self.output_paths:
            path.parent.mkdir(parents=True, exist_ok=True)

    def outputs_ready(self) -> bool:
        return all(path.exists() for path in self.output_paths)

    def log(self, message: str) -> None:
        if self.console:
            self.console.print(f"[cyan]{self.config.id}[/cyan] {message}")

    def execute(self, *, force: bool = False) -> None:  # pragma: no cover - abstract
        raise NotImplementedError


def _write_text(path: Path, content: str, *, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.write_text(content, encoding="utf-8")
    return True


def _write_json(path: Path, payload: dict, *, force: bool) -> bool:
    if path.exists() and not force:
        return False
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return True


class RequirementAnalyzer(ActivityAgent):
    def execute(self, *, force: bool = False) -> None:
        self.ensure_inputs()
        self.prepare_output_directories()

        spec_path = self.spa_root / "Output/requirement/requirement-spec.json"
        clar_path = self.spa_root / "Output/requirement/clarification-questions.md"

        spec_created = _write_json(
            spec_path,
            {
                "summary": "",
                "functional_requirements": [],
                "non_functional_requirements": [],
                "api_requirements": [],
                "data_requirements": [],
                "assumptions": [],
            },
            force=force,
        )

        clar_created = _write_text(
            clar_path,
            """# 澄清问题清单

- [ ] 问题 1：
- [ ] 问题 2：

> AA1 运行后请更新每个问题的状态与答案。
""",
            force=force,
        )

        if self.console:
            if spec_created or clar_created:
                self.log("已生成结构化需求骨架与澄清问题模版")
            else:
                self.log("输出已存在，使用 --force 可重新生成")


class TechnicalDesigner(ActivityAgent):
    def execute(self, *, force: bool = False) -> None:
        self.ensure_inputs()
        self.prepare_output_directories()

        design_md = self.spa_root / "Output/design/technical-design.md"
        api_spec = self.spa_root / "Output/design/api-spec.yaml"
        data_model = self.spa_root / "Output/design/data-model.json"

        design_created = _write_text(
            design_md,
            """# 技术方案

## 架构概览
TODO: 描述整体架构、关键组件与交互模式。

## 模块职责
- 模块一：
- 模块二：

## 技术选型
- 后端：
- 数据库：

## 风险与缓解
- 风险：
- 缓解：
""",
            force=force,
        )

        api_created = _write_text(
            api_spec,
            """openapi: 3.0.3
info:
  title: TBD
  version: 0.1.0
servers:
  - url: http://localhost:8000
paths: {}
components:
  schemas: {}
""",
            force=force,
        )

        data_created = _write_json(
            data_model,
            {
                "entities": [],
                "relationships": [],
                "indexes": [],
            },
            force=force,
        )

        if self.console:
            if design_created or api_created or data_created:
                self.log("技术方案骨架已生成，等待细化")
            else:
                self.log("设计相关输出已存在，使用 --force 可覆盖")


class CodeGeneratorAgent(ActivityAgent):
    def execute(self, *, force: bool = False) -> None:
        self.ensure_inputs()
        self.prepare_output_directories()

        code_root = self.spa_root / "Output/code"
        files_to_generate = {
            code_root / "app" / "__init__.py": "\n",
            code_root / "app" / "api" / "__init__.py": "\n",
            code_root / "app" / "api" / "routes.py": """from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="健康检查")
async def read_health():
    """基础健康检查端点。"""
    return {"status": "ok"}
""",
            code_root / "app" / "services" / "__init__.py": "\n",
            code_root / "app" / "repositories" / "__init__.py": "\n",
            code_root / "app" / "models" / "__init__.py": "\n",
            code_root / "tests" / "__init__.py": "\n",
            code_root / "tests" / "test_placeholder.py": """def test_placeholder():
    assert True
""",
            code_root / "docs" / "README.md": """# 代码说明

根据业务场景补充使用范例与设计决策记录。
""",
        }

        created_any = False
        for path, content in files_to_generate.items():
            path.parent.mkdir(parents=True, exist_ok=True)
            if _write_text(path, content, force=force):
                created_any = True

        if self.console:
            if created_any:
                self.log("代码骨架文件已准备完毕")
            else:
                self.log("代码骨架已存在，使用 --force 可重新生成")


class QualityCheckerAgent(ActivityAgent):
    def execute(self, *, force: bool = False) -> None:
        self.ensure_inputs()
        self.prepare_output_directories()

        report = self.spa_root / "Output/reports/quality-report.md"
        metrics = self.spa_root / "Output/reports/execution-metrics.json"

        report_created = _write_text(
            report,
            """# 质量报告

## 综合评价
- 得分：
- 结论：

## 亮点
- 

## 改进建议
- 

## 风险预警
- 
""",
            force=force,
        )

        metrics_created = _write_json(
            metrics,
            {
                "overall_score": 0,
                "requirement_score": 0,
                "design_score": 0,
                "code_score": 0,
                "quality_score": 0,
                "cycle_time_minutes": 0,
                "notes": "人工评审后更新得分并记录沉淀依据",
            },
            force=force,
        )

        if self.console:
            if report_created or metrics_created:
                self.log("质量报告与指标模板已就位")
            else:
                self.log("质量报告已存在，使用 --force 可重新生成")


AGENT_KIND_REGISTRY = {
    "requirement": RequirementAnalyzer,
    "technical-design": TechnicalDesigner,
    "code-generation": CodeGeneratorAgent,
    "quality": QualityCheckerAgent,
}


def instantiate_agent(
    spa_root: Path,
    config: AgentConfig,
    *,
    console: Console | None = None,
) -> ActivityAgent:
    agent_cls = AGENT_KIND_REGISTRY.get(config.kind)
    if agent_cls is None:
        raise ValueError(f"未知的 agent kind: {config.kind} (agent: {config.id})")
    return agent_cls(spa_root, config, console=console)


__all__ = [
    "AgentConfig",
    "ActivityAgent",
    "load_agent_registry",
    "instantiate_agent",
]


