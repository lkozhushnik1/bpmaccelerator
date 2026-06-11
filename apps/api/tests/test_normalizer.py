"""Tests for the process normalizer service."""

import pytest

from app.models.intake import IntakeMode, ProcessIntake
from app.models.normalized_process import NormalizedProcess, StepType
from app.services.normalizer import normalize


class TestNormalizeStructured:
    def test_returns_normalized_process(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert isinstance(result, NormalizedProcess)

    def test_metadata_name_matches_intake(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert result.metadata.name == structured_intake.process_name

    def test_metadata_industry_preserved(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert result.metadata.industry == structured_intake.industry

    def test_departments_preserved(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert result.metadata.departments == structured_intake.departments

    def test_steps_generated_for_each_key_step(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert len(result.steps) == len(structured_intake.key_steps)

    def test_steps_have_sequential_numbers(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        sequences = [s.sequence for s in result.steps]
        assert sequences == list(range(1, len(result.steps) + 1))

    def test_approval_step_type_inferred(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        approval_steps = [s for s in result.steps if s.step_type == StepType.approval]
        # "Request approvals" should be classified as approval
        assert len(approval_steps) >= 1

    def test_systems_normalized(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        system_names = [s.name for s in result.systems]
        for sys_name in structured_intake.systems:
            assert sys_name in system_names

    def test_pain_points_preserved(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert len(result.pain_points) == len(structured_intake.pain_points)

    def test_automation_goals_preserved(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert result.automation_goals == structured_intake.automation_goals

    def test_kpis_from_success_metrics(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert len(result.kpis) == len(structured_intake.success_metrics)

    def test_result_has_id(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert result.id and len(result.id) > 0

    def test_overview_description_set(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        assert result.overview.description == structured_intake.overview

    def test_actors_created_from_departments(self, structured_intake: ProcessIntake) -> None:
        result = normalize(structured_intake)
        actor_names = [a.name for a in result.actors]
        for dept in structured_intake.departments:
            assert dept in actor_names


class TestNormalizeFreeform:
    def test_returns_normalized_process(self, freeform_intake: ProcessIntake) -> None:
        result = normalize(freeform_intake)
        assert isinstance(result, NormalizedProcess)

    def test_steps_extracted_from_prompt(self, freeform_intake: ProcessIntake) -> None:
        result = normalize(freeform_intake)
        assert len(result.steps) > 0

    def test_steps_have_sequential_numbers(self, freeform_intake: ProcessIntake) -> None:
        result = normalize(freeform_intake)
        sequences = [s.sequence for s in result.steps]
        assert sequences == list(range(1, len(result.steps) + 1))

    def test_overview_description_is_prompt(self, freeform_intake: ProcessIntake) -> None:
        result = normalize(freeform_intake)
        assert result.overview.description == freeform_intake.prompt[:500]


class TestIntakeValidation:
    def test_freeform_requires_prompt(self) -> None:
        with pytest.raises(Exception):
            ProcessIntake(mode=IntakeMode.freeform)

    def test_structured_requires_process_name(self) -> None:
        with pytest.raises(Exception):
            ProcessIntake(mode=IntakeMode.structured, overview="Some overview")

    def test_structured_requires_overview(self) -> None:
        with pytest.raises(Exception):
            ProcessIntake(mode=IntakeMode.structured, process_name="Test")
