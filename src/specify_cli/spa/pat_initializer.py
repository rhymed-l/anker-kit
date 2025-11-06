# -*- coding: utf-8 -*-

"""Bootstrap helpers for the AnkerSPA PAT directory structure."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
from typing import Iterable

from rich.console import Console

SPA_TEMPLATE_VERSION = "2025.11.06"


SPA_DIRECTORIES: tuple[str, ...] = (
    "AnkerSPA",
    "AnkerSPA/MetaData",
    "AnkerSPA/Input",
    "AnkerSPA/Output",
    "AnkerSPA/Output/requirement",
    "AnkerSPA/Output/design",
    "AnkerSPA/Output/code",
    "AnkerSPA/Output/reports",
    "AnkerSPA/Practice",
    "AnkerSPA/Plan",
    "AnkerSPA/Checklist",
    "AnkerSPA/Reference",
    "AnkerSPA/Tool",
    "AnkerSPA/Objective",
    "AnkerSPA/AA",
    "AnkerSPA/AA/AA1-RequirementAnalyzer",
    "AnkerSPA/AA/AA2-TechnicalDesigner",
    "AnkerSPA/AA/AA3-CodeGenerator",
    "AnkerSPA/AA/AA4-QualityChecker",
    "AnkerSPA/Output/code/app/api",
    "AnkerSPA/Output/code/app/models",
    "AnkerSPA/Output/code/app/services",
    "AnkerSPA/Output/code/app/repositories",
    "AnkerSPA/Output/code/tests",
    "AnkerSPA/Output/code/docs",
    "AnkerSPA/Practice/.staging",
)


SPA_TEMPLATE_FILES: dict[str, str] = {
    "AnkerSPA/MetaData/spa-info.yaml": dedent(
        """
        version: "1.0.0"
        name: "AnkerSPA"
        owner: "TODO-填入负责人"
        description: "基于PAT标准的软件研发流程智能体"
        tags: ["PAT", "SPA", "Anker" ]
        template_version: "2025.11.06"
        """
    ).strip()
    + "\n",
    "AnkerSPA/MetaData/dependencies.yaml": dedent(
        """
        upstream_agents: []
        downstream_agents: []
        external_systems: []
        orchestration_notes: "依据Plan/workflow.yaml 串行执行"
        """
    ).strip()
    + "\n",
    "AnkerSPA/Input/requirement.md": dedent(
        """
        # 原始需求

        请在此粘贴产品或业务需求。保持最新版本，AA1 会基于此生成结构化需求。建议包含：业务目标、核心流程、关键角色、约束条件。
        """
    ).strip()
    + "\n",
    "AnkerSPA/Input/context.json": dedent(
        """
        {
          "project_name": "",
          "domain": "",
          "stakeholders": [],
          "non_functional": {
            "performance": "",
            "security": "",
            "compliance": ""
          }
        }
        """
    ).strip()
    + "\n",
    "AnkerSPA/Output/requirement/.gitkeep": "\n",
    "AnkerSPA/Output/design/.gitkeep": "\n",
    "AnkerSPA/Output/code/.gitkeep": "\n",
    "AnkerSPA/Output/reports/.gitkeep": "\n",
    "AnkerSPA/Plan/workflow.yaml": dedent(
        """
        stage_1:
          label: "Requirement Analysis"
          agent: "AA1"
          depends_on: []
          outputs: ["Output/requirement/requirement-spec.json", "Output/requirement/clarification-questions.md"]
          human_review_enabled: true
          human_review_prompt: "请确认需求规范是否准确"
        stage_2:
          label: "Technical Design"
          agent: "AA2"
          depends_on: ["stage_1"]
          outputs: ["Output/design/technical-design.md", "Output/design/api-spec.yaml", "Output/design/data-model.json"]
          human_review_enabled: true
          human_review_prompt: "请确认技术方案是否合理"
        stage_3:
          label: "Code Generation"
          agent: "AA3"
          depends_on: ["stage_2"]
          outputs: ["Output/code/README.md", "Output/code/test-cases.json"]
          human_review_enabled: false
          human_review_prompt: ""
        stage_4:
          label: "Quality Check"
          agent: "AA4"
          depends_on: ["stage_1", "stage_2", "stage_3"]
          outputs: ["Output/reports/quality-report.md", "Output/reports/execution-metrics.json"]
          human_review_enabled: false
          human_review_prompt: ""
          final_stage: true
        """
    ).strip()
    + "\n",
    "AnkerSPA/Plan/aa-orchestration.yaml": dedent(
        """
        version: "1.0.0"
        knowledge_threshold: 80
        auto_promote_practice: true
        practice_files: ["Input/requirement.md", "Output/requirement/requirement-spec.json", "Output/design/technical-design.md", "Output/design/api-spec.yaml", "Output/design/data-model.json"]
        practice_code_root: "Output/code"
        metrics_file: "Output/reports/execution-metrics.json"
        """
    ).strip()
    + "\n",
    "AnkerSPA/Checklist/requirement-checklist.yaml": dedent(
        """
        checklist: ["业务目标明确", "角色及场景覆盖", "边界条件清晰", "非功能需求补充"]
        score_weights: [30, 30, 20, 20]
        """
    ).strip()
    + "\n",
    "AnkerSPA/Checklist/design-checklist.yaml": dedent(
        """
        checklist: ["架构层次合理", "接口契约完整", "数据模型规范", "风险与缓解建议"]
        score_weights: [25, 30, 25, 20]
        """
    ).strip()
    + "\n",
    "AnkerSPA/Checklist/code-checklist.yaml": dedent(
        """
        checklist: ["目录结构符合标准", "代码注释与类型标注", "异常处理充分", "测试覆盖率达标"]
        score_weights: [20, 30, 25, 25]
        """
    ).strip()
    + "\n",
    "AnkerSPA/Reference/coding-standard.md": dedent(
        """
        # 编码规范

        - 统一使用 PEP8 风格（Python 示例）
        - 严格的类型注解
        - 函数注释遵循 Google 风格
        - 重要路径增加结构化日志
        - 错误处理需返回可追踪上下文
        """
    ).strip()
    + "\n",
    "AnkerSPA/Reference/tech-stack.yaml": dedent(
        """
        backend: "FastAPI"
        database: "PostgreSQL"
        orm: "SQLAlchemy"
        messaging: ""
        observability: ""
        """
    ).strip()
    + "\n",
    "AnkerSPA/Reference/api-design-guide.md": dedent(
        """
        # API 设计指南

        - 遵循 RESTful 语义，使用 kebab-case 路径
        - 使用 OpenAPI 3.0 描述接口，字段提供 example
        - 保持幂等操作语义，写操作返回资源状态
        - 错误响应使用结构化 problem+json
        """
    ).strip()
    + "\n",
    "AnkerSPA/Practice/.gitkeep": "\n",
    "AnkerSPA/Tool/claude-api.yaml": dedent(
        """
        provider: "claude"
        model: "claude-3-sonnet"
        endpoint: "https://api.anthropic.com"
        api_key_var: "ANTHROPIC_API_KEY"
        retry: 3
        timeout_seconds: 60
        """
    ).strip()
    + "\n",
    "AnkerSPA/Objective/success-criteria.yaml": dedent(
        """
        scoring:
          efficiency: 35
          quality: 35
          knowledge: 20
          demo: 10
        minimum_acceptance: 80
        demo_expectation_minutes: 15
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA1-RequirementAnalyzer/metadata.yaml": dedent(
        """
        id: "AA1"
        name: "RequirementAnalyzer"
        kind: "requirement"
        version: "1.0.0"
        inputs: ["Input/requirement.md", "Input/context.json"]
        outputs: ["Output/requirement/requirement-spec.json", "Output/requirement/clarification-questions.md"]
        description: "将原始需求转化为结构化需求，并列出澄清问题"
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA1-RequirementAnalyzer/prompt-template.md": dedent(
        """
        # Requirement Analyzer Prompt

        角色：10 年资深需求分析师，聚焦业务上下文、边界条件、隐含需求。

        ## 输入
        - 原始需求：Input/requirement.md
        - 项目上下文：Input/context.json

        ## 输出任务
        1. 生成结构化需求（Output/requirement/requirement-spec.json）
        2. 输出澄清问题（Output/requirement/clarification-questions.md）

        ## 质量要求
        - 功能、非功能、数据、接口四个维度完整
        - 所有疑问需转化为澄清问题
        - JSON 输出需通过校验
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA1-RequirementAnalyzer/checklist.yaml": dedent(
        """
        checklist: ["需求摘要覆盖场景", "功能拆解清晰", "非功能指标具备量化", "澄清问题指向具体风险"]
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA2-TechnicalDesigner/metadata.yaml": dedent(
        """
        id: "AA2"
        name: "TechnicalDesigner"
        kind: "technical-design"
        version: "1.0.0"
        inputs: ["Output/requirement/requirement-spec.json", "Reference/tech-stack.yaml", "Reference/coding-standard.md"]
        outputs: ["Output/design/technical-design.md", "Output/design/api-spec.yaml", "Output/design/data-model.json"]
        description: "制定整体技术方案，参考历史案例"
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA2-TechnicalDesigner/prompt-template.md": dedent(
        """
        # Technical Designer Prompt

        角色：15 年技术架构师，擅长微服务与 DDD。

        ## 输入
        - 结构化需求：Output/requirement/requirement-spec.json
        - 技术栈约束：Reference/tech-stack.yaml
        - 编码规范：Reference/coding-standard.md
        - 历史案例：Practice/*

        ## 输出任务
        1. 技术方案文档（Output/design/technical-design.md）
        2. OpenAPI 规格（Output/design/api-spec.yaml）
        3. 数据模型（Output/design/data-model.json）

        ## 质量要求
        - 模块划分清晰，符合 PAT
        - API 契约完整，字段含义明确
        - 数据模型支持查询、写入与约束
        - 历史案例需引用可复用模式
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA2-TechnicalDesigner/checklist.yaml": dedent(
        """
        checklist: ["架构含分层与组件职责", "API 契约齐备并含错误码", "数据模型含索引与约束", "结合 Practice 案例"]
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA3-CodeGenerator/metadata.yaml": dedent(
        """
        id: "AA3"
        name: "CodeGenerator"
        kind: "code-generation"
        version: "1.0.0"
        inputs: ["Output/design/technical-design.md", "Output/design/api-spec.yaml", "Output/design/data-model.json"]
        outputs: ["Output/code/README.md", "Output/code/test-cases.json"]
        description: "根据设计生成项目骨架与测试模板"
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA3-CodeGenerator/prompt-template.md": dedent(
        """
        # Code Generator Prompt

        角色：资深工程师，遵循 PEP8 与分层架构。

        ## 输入
        - 技术方案：Output/design/technical-design.md
        - API 规格：Output/design/api-spec.yaml
        - 数据模型：Output/design/data-model.json

        ## 输出任务
        - FastAPI 三层目录结构
        - 关键模块骨架与 TODO 注释
        - 单元测试模板与测试用例清单

        ## 质量要求
        - 严格类型注解
        - docstring 说明
        - 错误处理与日志位置预留
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA3-CodeGenerator/checklist.yaml": dedent(
        """
        checklist: ["应用分层结构完整", "README 说明运行方式", "测试目录包含样例", "代码含 TODO 指引"]
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA4-QualityChecker/metadata.yaml": dedent(
        """
        id: "AA4"
        name: "QualityChecker"
        kind: "quality"
        version: "1.0.0"
        inputs: ["Output/requirement/requirement-spec.json", "Output/design/technical-design.md", "Output/code/README.md", "Checklist/requirement-checklist.yaml", "Checklist/design-checklist.yaml", "Checklist/code-checklist.yaml"]
        outputs: ["Output/reports/quality-report.md", "Output/reports/execution-metrics.json"]
        description: "评估产出质量并决定知识沉淀"
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA4-QualityChecker/prompt-template.md": dedent(
        """
        # Quality Checker Prompt

        角色：质量保障专家，负责评分与知识沉淀。

        ## 输入
        - 各阶段产出
        - 阶段检查清单

        ## 输出任务
        1. 质量报告（Output/reports/quality-report.md）
        2. 执行指标（Output/reports/execution-metrics.json）

        ## 质量要求
        - 列出亮点与改进项
        - 指标结构化，含总体得分
        - 当得分 >= 80 触发知识沉淀
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA4-QualityChecker/checklist.yaml": dedent(
        """
        checklist: ["按阶段评分", "指出主要风险", "附执行指标", "给出沉淀建议"]
        """
    ).strip()
    + "\n",
    "AnkerSPA/Output/code/README.md": dedent(
        """
        # 代码骨架说明

        该目录由 AA3 自动生成，包含 FastAPI 项目的分层结构。

        ## 目录结构
        - app/api: 路由与控制器
        - app/models: ORM 模型
        - app/services: 业务服务
        - app/repositories: 数据访问
        - tests: 单元测试模板

        ## 下一步
        - 根据设计细化实现
        - 完成 TODO 标注的逻辑
        - 补充测试用例
        """
    ).strip()
    + "\n",
    "AnkerSPA/Output/code/test-cases.json": dedent(
        """
        {
          "scenarios": [
            {
              "id": "TC-001",
              "name": "示例测试用例",
              "description": "替换为实际业务场景",
              "preconditions": [],
              "steps": [],
              "expected_result": ""
            }
          ]
        }
        """
    ).strip()
    + "\n",
    "AnkerSPA/Output/reports/quality-report.md": dedent(
        """
        # 质量报告

        - 总体评分：
        - 亮点：
        - 改进建议：
        - 风险预警：

        > 由 AA4 输出，人工审核后可补充细节。
        """
    ).strip()
    + "\n",
    "AnkerSPA/Output/reports/execution-metrics.json": dedent(
        """
        {
          "overall_score": 0,
          "requirement_score": 0,
          "design_score": 0,
          "code_score": 0,
          "quality_score": 0,
          "cycle_time_minutes": 0,
          "notes": "待AA4填写"
        }
        """
    ).strip()
    + "\n",
    "AnkerSPA/Practice/.staging/.gitkeep": "\n",
}


@dataclass
class InitializationResult:
    root: Path
    created_directories: list[Path]
    created_files: list[Path]
    skipped_files: list[Path]


def _normalize(path: Path) -> Path:
    return Path(*path.parts)


def initialize_spa_environment(
    project_path: Path,
    *,
    console: Console | None = None,
    force: bool = False,
) -> InitializationResult:
    """Ensure the AnkerSPA PAT structure exists within ``project_path``."""

    spa_root = project_path / "AnkerSPA"

    created_dirs: list[Path] = []
    created_files: list[Path] = []
    skipped_files: list[Path] = []

    for relative in SPA_DIRECTORIES:
        target_dir = spa_root.parent / relative
        if not target_dir.exists():
            target_dir.mkdir(parents=True, exist_ok=True)
            created_dirs.append(_normalize(target_dir.relative_to(project_path)))

    for relative, content in SPA_TEMPLATE_FILES.items():
        target_file = spa_root.parent / relative
        target_file.parent.mkdir(parents=True, exist_ok=True)
        if target_file.exists() and not force:
            skipped_files.append(_normalize(target_file.relative_to(project_path)))
            continue
        target_file.write_text(content, encoding="utf-8")
        created_files.append(_normalize(target_file.relative_to(project_path)))

    if console:
        console.print(
            f"[cyan]AnkerSPA PAT 模板[/cyan] 已同步到 [green]{spa_root}[/green] (模板版本 {SPA_TEMPLATE_VERSION})"
        )
        if created_files:
            console.print(f"  新建文件: {len(created_files)}")
        if skipped_files and not force:
            console.print(f"  跳过现有文件: {len(skipped_files)} (使用 --force 可覆盖)")

    return InitializationResult(
        root=spa_root,
        created_directories=created_dirs,
        created_files=created_files,
        skipped_files=skipped_files,
    )


__all__ = ["SPA_TEMPLATE_VERSION", "InitializationResult", "initialize_spa_environment"]


