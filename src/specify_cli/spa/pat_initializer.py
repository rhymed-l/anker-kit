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
        owner: "TODO-\u586b\u5165\u8d1f\u8d23\u4eba"
        description: "\u57fa\u4e8ePAT\u6807\u51c6\u7684\u8f6f\u4ef6\u7814\u53d1\u6d41\u7a0b\u667a\u80fd\u4f53"
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
        orchestration_notes: "\u4f9d\u636ePlan/workflow.yaml \u4e32\u884c\u6267\u884c"
        """
    ).strip()
    + "\n",
    "AnkerSPA/Input/requirement.md": dedent(
        """
        # \u539f\u59cb\u9700\u6c42

        \u8bf7\u5728\u6b64\u7c98\u8d34\u4ea7\u54c1\u6216\u4e1a\u52a1\u9700\u6c42\u3002\u4fdd\u6301\u6700\u65b0\u7248\u672c\uff0cAA1 \u4f1a\u57fa\u4e8e\u6b64\u751f\u6210\u7ed3\u6784\u5316\u9700\u6c42\u3002\u5efa\u8bae\u5305\u542b\uff1a\u4e1a\u52a1\u76ee\u6807\u3001\u6838\u5fc3\u6d41\u7a0b\u3001\u5173\u952e\u89d2\u8272\u3001\u7ea6\u675f\u6761\u4ef6\u3002
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
          human_review_prompt: "\u8bf7\u786e\u8ba4\u9700\u6c42\u89c4\u8303\u662f\u5426\u51c6\u786e"
        stage_2:
          label: "Technical Design"
          agent: "AA2"
          depends_on: ["stage_1"]
          outputs: ["Output/design/technical-design.md", "Output/design/api-spec.yaml", "Output/design/data-model.json"]
          human_review_enabled: true
          human_review_prompt: "\u8bf7\u786e\u8ba4\u6280\u672f\u65b9\u6848\u662f\u5426\u5408\u7406"
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
        checklist: ["\u4e1a\u52a1\u76ee\u6807\u660e\u786e", "\u89d2\u8272\u53ca\u573a\u666f\u8986\u76d6", "\u8fb9\u754c\u6761\u4ef6\u6e05\u6670", "\u975e\u529f\u80fd\u9700\u6c42\u8865\u5145"]
        score_weights: [30, 30, 20, 20]
        """
    ).strip()
    + "\n",
    "AnkerSPA/Checklist/design-checklist.yaml": dedent(
        """
        checklist: ["\u67b6\u6784\u5c42\u6b21\u5408\u7406", "\u63a5\u53e3\u5951\u7ea6\u5b8c\u6574", "\u6570\u636e\u6a21\u578b\u89c4\u8303", "\u98ce\u9669\u4e0e\u7f13\u89e3\u5efa\u8bae"]
        score_weights: [25, 30, 25, 20]
        """
    ).strip()
    + "\n",
    "AnkerSPA/Checklist/code-checklist.yaml": dedent(
        """
        checklist: ["\u76ee\u5f55\u7ed3\u6784\u7b26\u5408\u6807\u51c6", "\u4ee3\u7801\u6ce8\u91ca\u4e0e\u7c7b\u578b\u6807\u6ce8", "\u5f02\u5e38\u5904\u7406\u5145\u5206", "\u6d4b\u8bd5\u8986\u76d6\u7387\u8fbe\u6807"]
        score_weights: [20, 30, 25, 25]
        """
    ).strip()
    + "\n",
    "AnkerSPA/Reference/coding-standard.md": dedent(
        """
        # \u7f16\u7801\u89c4\u8303

        - \u7edf\u4e00\u4f7f\u7528 PEP8 \u98ce\u683c\uff08Python \u793a\u4f8b\uff09
        - \u4e25\u683c\u7684\u7c7b\u578b\u6ce8\u89e3
        - \u51fd\u6570\u6ce8\u91ca\u9075\u5faa Google \u98ce\u683c
        - \u91cd\u8981\u8def\u5f84\u589e\u52a0\u7ed3\u6784\u5316\u65e5\u5fd7
        - \u9519\u8bef\u5904\u7406\u9700\u8fd4\u56de\u53ef\u8ffd\u8e2a\u4e0a\u4e0b\u6587
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
        # API \u8bbe\u8ba1\u6307\u5357

        - \u9075\u5faa RESTful \u8bed\u4e49\uff0c\u4f7f\u7528 kebab-case \u8def\u5f84
        - \u4f7f\u7528 OpenAPI 3.0 \u63cf\u8ff0\u63a5\u53e3\uff0c\u5b57\u6bb5\u63d0\u4f9b example
        - \u4fdd\u6301\u5e42\u7b49\u64cd\u4f5c\u8bed\u4e49\uff0c\u5199\u64cd\u4f5c\u8fd4\u56de\u8d44\u6e90\u72b6\u6001
        - \u9519\u8bef\u54cd\u5e94\u4f7f\u7528\u7ed3\u6784\u5316 problem+json
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
        description: "\u5c06\u539f\u59cb\u9700\u6c42\u8f6c\u5316\u4e3a\u7ed3\u6784\u5316\u9700\u6c42\uff0c\u5e76\u5217\u51fa\u6f84\u6e05\u95ee\u9898"
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA1-RequirementAnalyzer/prompt-template.md": dedent(
        """
        # Requirement Analyzer Prompt

        \u89d2\u8272\uff1a10 \u5e74\u8d44\u6df1\u9700\u6c42\u5206\u6790\u5e08\uff0c\u805a\u7126\u4e1a\u52a1\u4e0a\u4e0b\u6587\u3001\u8fb9\u754c\u6761\u4ef6\u3001\u9690\u542b\u9700\u6c42\u3002

        ## \u8f93\u5165
        - \u539f\u59cb\u9700\u6c42\uff1aInput/requirement.md
        - \u9879\u76ee\u4e0a\u4e0b\u6587\uff1aInput/context.json

        ## \u8f93\u51fa\u4efb\u52a1
        1. \u751f\u6210\u7ed3\u6784\u5316\u9700\u6c42\uff08Output/requirement/requirement-spec.json\uff09
        2. \u8f93\u51fa\u6f84\u6e05\u95ee\u9898\uff08Output/requirement/clarification-questions.md\uff09

        ## \u8d28\u91cf\u8981\u6c42
        - \u529f\u80fd\u3001\u975e\u529f\u80fd\u3001\u6570\u636e\u3001\u63a5\u53e3\u56db\u4e2a\u7ef4\u5ea6\u5b8c\u6574
        - \u6240\u6709\u7591\u95ee\u9700\u8f6c\u5316\u4e3a\u6f84\u6e05\u95ee\u9898
        - JSON \u8f93\u51fa\u9700\u901a\u8fc7\u6821\u9a8c
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA1-RequirementAnalyzer/checklist.yaml": dedent(
        """
        checklist: ["\u9700\u6c42\u6458\u8981\u8986\u76d6\u573a\u666f", "\u529f\u80fd\u62c6\u89e3\u6e05\u6670", "\u975e\u529f\u80fd\u6307\u6807\u5177\u5907\u91cf\u5316", "\u6f84\u6e05\u95ee\u9898\u6307\u5411\u5177\u4f53\u98ce\u9669"]
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
        description: "\u5236\u5b9a\u6574\u4f53\u6280\u672f\u65b9\u6848\uff0c\u53c2\u8003\u5386\u53f2\u6848\u4f8b"
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA2-TechnicalDesigner/prompt-template.md": dedent(
        """
        # Technical Designer Prompt

        \u89d2\u8272\uff1a15 \u5e74\u6280\u672f\u67b6\u6784\u5e08\uff0c\u64c5\u957f\u5fae\u670d\u52a1\u4e0e DDD\u3002

        ## \u8f93\u5165
        - \u7ed3\u6784\u5316\u9700\u6c42\uff1aOutput/requirement/requirement-spec.json
        - \u6280\u672f\u6808\u7ea6\u675f\uff1aReference/tech-stack.yaml
        - \u7f16\u7801\u89c4\u8303\uff1aReference/coding-standard.md
        - \u5386\u53f2\u6848\u4f8b\uff1aPractice/*

        ## \u8f93\u51fa\u4efb\u52a1
        1. \u6280\u672f\u65b9\u6848\u6587\u6863\uff08Output/design/technical-design.md\uff09
        2. OpenAPI \u89c4\u683c\uff08Output/design/api-spec.yaml\uff09
        3. \u6570\u636e\u6a21\u578b\uff08Output/design/data-model.json\uff09

        ## \u8d28\u91cf\u8981\u6c42
        - \u6a21\u5757\u5212\u5206\u6e05\u6670\uff0c\u7b26\u5408 PAT
        - API \u5951\u7ea6\u5b8c\u6574\uff0c\u5b57\u6bb5\u542b\u4e49\u660e\u786e
        - \u6570\u636e\u6a21\u578b\u652f\u6301\u67e5\u8be2\u3001\u5199\u5165\u4e0e\u7ea6\u675f
        - \u5386\u53f2\u6848\u4f8b\u9700\u5f15\u7528\u53ef\u590d\u7528\u6a21\u5f0f
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA2-TechnicalDesigner/checklist.yaml": dedent(
        """
        checklist: ["\u67b6\u6784\u542b\u5206\u5c42\u4e0e\u7ec4\u4ef6\u804c\u8d23", "API \u5951\u7ea6\u9f50\u5907\u5e76\u542b\u9519\u8bef\u7801", "\u6570\u636e\u6a21\u578b\u542b\u7d22\u5f15\u4e0e\u7ea6\u675f", "\u7ed3\u5408 Practice \u6848\u4f8b"]
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
        description: "\u6839\u636e\u8bbe\u8ba1\u751f\u6210\u9879\u76ee\u9aa8\u67b6\u4e0e\u6d4b\u8bd5\u6a21\u677f"
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA3-CodeGenerator/prompt-template.md": dedent(
        """
        # Code Generator Prompt

        \u89d2\u8272\uff1a\u8d44\u6df1\u5de5\u7a0b\u5e08\uff0c\u9075\u5faa PEP8 \u4e0e\u5206\u5c42\u67b6\u6784\u3002

        ## \u8f93\u5165
        - \u6280\u672f\u65b9\u6848\uff1aOutput/design/technical-design.md
        - API \u89c4\u683c\uff1aOutput/design/api-spec.yaml
        - \u6570\u636e\u6a21\u578b\uff1aOutput/design/data-model.json

        ## \u8f93\u51fa\u4efb\u52a1
        - FastAPI \u4e09\u5c42\u76ee\u5f55\u7ed3\u6784
        - \u5173\u952e\u6a21\u5757\u9aa8\u67b6\u4e0e TODO \u6ce8\u91ca
        - \u5355\u5143\u6d4b\u8bd5\u6a21\u677f\u4e0e\u6d4b\u8bd5\u7528\u4f8b\u6e05\u5355

        ## \u8d28\u91cf\u8981\u6c42
        - \u4e25\u683c\u7c7b\u578b\u6ce8\u89e3
        - docstring \u8bf4\u660e
        - \u9519\u8bef\u5904\u7406\u4e0e\u65e5\u5fd7\u4f4d\u7f6e\u9884\u7559
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA3-CodeGenerator/checklist.yaml": dedent(
        """
        checklist: ["\u5e94\u7528\u5206\u5c42\u7ed3\u6784\u5b8c\u6574", "README \u8bf4\u660e\u8fd0\u884c\u65b9\u5f0f", "\u6d4b\u8bd5\u76ee\u5f55\u5305\u542b\u6837\u4f8b", "\u4ee3\u7801\u542b TODO \u6307\u5f15"]
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
        description: "\u8bc4\u4f30\u4ea7\u51fa\u8d28\u91cf\u5e76\u51b3\u5b9a\u77e5\u8bc6\u6c89\u6dc0"
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA4-QualityChecker/prompt-template.md": dedent(
        """
        # Quality Checker Prompt

        \u89d2\u8272\uff1a\u8d28\u91cf\u4fdd\u969c\u4e13\u5bb6\uff0c\u8d1f\u8d23\u8bc4\u5206\u4e0e\u77e5\u8bc6\u6c89\u6dc0\u3002

        ## \u8f93\u5165
        - \u5404\u9636\u6bb5\u4ea7\u51fa
        - \u9636\u6bb5\u68c0\u67e5\u6e05\u5355

        ## \u8f93\u51fa\u4efb\u52a1
        1. \u8d28\u91cf\u62a5\u544a\uff08Output/reports/quality-report.md\uff09
        2. \u6267\u884c\u6307\u6807\uff08Output/reports/execution-metrics.json\uff09

        ## \u8d28\u91cf\u8981\u6c42
        - \u5217\u51fa\u4eae\u70b9\u4e0e\u6539\u8fdb\u9879
        - \u6307\u6807\u7ed3\u6784\u5316\uff0c\u542b\u603b\u4f53\u5f97\u5206
        - \u5f53\u5f97\u5206 >= 80 \u89e6\u53d1\u77e5\u8bc6\u6c89\u6dc0
        """
    ).strip()
    + "\n",
    "AnkerSPA/AA/AA4-QualityChecker/checklist.yaml": dedent(
        """
        checklist: ["\u6309\u9636\u6bb5\u8bc4\u5206", "\u6307\u51fa\u4e3b\u8981\u98ce\u9669", "\u9644\u6267\u884c\u6307\u6807", "\u7ed9\u51fa\u6c89\u6dc0\u5efa\u8bae"]
        """
    ).strip()
    + "\n",
    "AnkerSPA/Output/code/README.md": dedent(
        """
        # \u4ee3\u7801\u9aa8\u67b6\u8bf4\u660e

        \u8be5\u76ee\u5f55\u7531 AA3 \u81ea\u52a8\u751f\u6210\uff0c\u5305\u542b FastAPI \u9879\u76ee\u7684\u5206\u5c42\u7ed3\u6784\u3002

        ## \u76ee\u5f55\u7ed3\u6784
        - app/api: \u8def\u7531\u4e0e\u63a7\u5236\u5668
        - app/models: ORM \u6a21\u578b
        - app/services: \u4e1a\u52a1\u670d\u52a1
        - app/repositories: \u6570\u636e\u8bbf\u95ee
        - tests: \u5355\u5143\u6d4b\u8bd5\u6a21\u677f

        ## \u4e0b\u4e00\u6b65
        - \u6839\u636e\u8bbe\u8ba1\u7ec6\u5316\u5b9e\u73b0
        - \u5b8c\u6210 TODO \u6807\u6ce8\u7684\u903b\u8f91
        - \u8865\u5145\u6d4b\u8bd5\u7528\u4f8b
        """
    ).strip()
    + "\n",
    "AnkerSPA/Output/code/test-cases.json": dedent(
        """
        {
          "scenarios": [
            {
              "id": "TC-001",
              "name": "\u793a\u4f8b\u6d4b\u8bd5\u7528\u4f8b",
              "description": "\u66ff\u6362\u4e3a\u5b9e\u9645\u4e1a\u52a1\u573a\u666f",
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
        # \u8d28\u91cf\u62a5\u544a

        - \u603b\u4f53\u8bc4\u5206\uff1a
        - \u4eae\u70b9\uff1a
        - \u6539\u8fdb\u5efa\u8bae\uff1a
        - \u98ce\u9669\u9884\u8b66\uff1a

        > \u7531 AA4 \u8f93\u51fa\uff0c\u4eba\u5de5\u5ba1\u6838\u540e\u53ef\u8865\u5145\u7ec6\u8282\u3002
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
          "notes": "\u5f85AA4\u586b\u5199"
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
            f"[cyan]AnkerSPA PAT \u6a21\u677f[/cyan] \u5df2\u540c\u6b65\u5230 [green]{spa_root}[/green] (\u6a21\u677f\u7248\u672c {SPA_TEMPLATE_VERSION})"
        )
        if created_files:
            console.print(f"  \u65b0\u5efa\u6587\u4ef6: {len(created_files)}")
        if skipped_files and not force:
            console.print(f"  \u8df3\u8fc7\u73b0\u6709\u6587\u4ef6: {len(skipped_files)} (\u4f7f\u7528 --force \u53ef\u8986\u76d6)")

    return InitializationResult(
        root=spa_root,
        created_directories=created_dirs,
        created_files=created_files,
        skipped_files=skipped_files,
    )


__all__ = ["SPA_TEMPLATE_VERSION", "InitializationResult", "initialize_spa_environment"]


