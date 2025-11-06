# -*- coding: utf-8 -*-

"""High-level orchestration for the AnkerSPA workflow."""

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Sequence

from rich.console import Console

from .agents import AgentConfig, instantiate_agent, load_agent_registry
from .simple_yaml import load_simple_yaml
from .workflow import StageDefinition, load_workflow_definition


class AnkerSPA:
    """Runtime orchestrator that executes Activity Agents sequentially."""

    def __init__(
        self,
        project_root: Path | None = None,
        *,
        console: Console | None = None,
    ) -> None:
        self.project_root = project_root or Path.cwd()
        self.console = console or Console()
        self.spa_root = self._resolve_spa_root(self.project_root)
        self.workflow = load_workflow_definition(self.spa_root / "Plan/workflow.yaml")
        self.agent_registry = load_agent_registry(self.spa_root)
        self.orchestration_config = self._load_orchestration_config()

    def _resolve_spa_root(self, project_root: Path) -> Path:
        if (project_root / "MetaData").exists():
            return project_root
        spa_candidate = project_root / "AnkerSPA"
        if not spa_candidate.exists():
            raise FileNotFoundError(f"AnkerSPA directory not found: {spa_candidate}")
        return spa_candidate

    def _load_orchestration_config(self) -> dict:
        config_file = self.spa_root / "Plan/aa-orchestration.yaml"
        if not config_file.exists():
            return {}
        return load_simple_yaml(config_file)

    def list_stages(self) -> List[StageDefinition]:
        return self.workflow.ordered_stages()

    def run(
        self,
        *,
        force: bool = False,
        stages: Sequence[str] | None = None,
    ) -> List[str]:
        stage_queue = self.workflow.ordered_stages()
        if stages:
            allowed = set(stages)
            stage_queue = [
                stage for stage in stage_queue if stage.key in allowed or stage.agent in allowed
            ]

        executed: List[str] = []
        for stage in stage_queue:
            agent_config = self.agent_registry.get(stage.agent)
            if not agent_config:
                raise ValueError(f"Agent for stage {stage.key} not found: {stage.agent}")
            agent = instantiate_agent(self.spa_root, agent_config, console=self.console)
            self.console.print(
                f"[bold cyan]Stage {stage.key}[/bold cyan] -> {stage.label} ({agent_config.name})"
            )
            agent.execute(force=force)
            executed.append(stage.key)

            if stage.human_review_enabled:
                prompt = stage.human_review_prompt or "Manual review required"
                self.console.print(f"[yellow]Manual review[/yellow]: {prompt}")

        return executed

    def promote_practice(self) -> Path | None:
        if not bool(self.orchestration_config.get("auto_promote_practice", True)):
            self.console.print("[bright_black]Auto practice promotion disabled; skipping.[/bright_black]")
            return None

        metrics_rel = self.orchestration_config.get(
            "metrics_file", "Output/reports/execution-metrics.json"
        )
        metrics_path = self.spa_root / metrics_rel
        if not metrics_path.exists():
            return None

        try:
            metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            self.console.print(
                f"[red]Failed to parse metrics file[/red]: {metrics_path.relative_to(self.spa_root)}"
            )
            return None

        threshold = int(self.orchestration_config.get("knowledge_threshold", 80))
        if metrics.get("overall_score", 0) < threshold:
            self.console.print(
                f"[bright_black]Overall score {metrics.get('overall_score', 0)} below threshold {threshold}; skipping promotion.[/bright_black]"
            )
            return None

        practice_dir = self.spa_root / "Practice"
        practice_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        counter = 0
        case_path: Path
        while True:
            suffix = f"-{counter:02d}" if counter else ""
            candidate = practice_dir / f"case-{timestamp}{suffix}"
            if not candidate.exists():
                case_path = candidate
                break
            counter += 1

        case_path.mkdir(parents=True)

        practice_files = self.orchestration_config.get("practice_files", [])
        for rel in practice_files:
            src = self.spa_root / rel
            if not src.exists() or not src.is_file():
                continue
            dest = case_path / Path(rel).name
            dest.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")

        code_root_rel = self.orchestration_config.get("practice_code_root", "Output/code")
        code_root = self.spa_root / code_root_rel
        if code_root.exists():
            dest_code = case_path / "code-samples"
            if dest_code.exists():
                shutil.rmtree(dest_code)
            shutil.copytree(code_root, dest_code)

        readme_path = case_path / "README.md"
        readme_content = self._render_practice_readme(case_path.name, metrics)
        readme_path.write_text(readme_content, encoding="utf-8")

        self.console.print(
            f"[green]Practice case created[/green]: {case_path.relative_to(self.spa_root)}"
        )
        return case_path

    def _render_practice_readme(self, case_name: str, metrics: dict) -> str:
        lines = [
            f"# {case_name}",
            "",
            "## Overall Scores",
            f"- Total Score: {metrics.get('overall_score', 'n/a')}",
            f"- Requirement: {metrics.get('requirement_score', 'n/a')}",
            f"- Design: {metrics.get('design_score', 'n/a')}",
            f"- Code: {metrics.get('code_score', 'n/a')}",
            f"- Quality: {metrics.get('quality_score', 'n/a')}",
            "",
            "## Execution Metrics",
            f"- Cycle Time (minutes): {metrics.get('cycle_time_minutes', 'unknown')}",
            "",
            "## Notes",
            metrics.get("notes", "None provided"),
        ]
        return "\n".join(lines) + "\n"


__all__ = ["AnkerSPA"]


