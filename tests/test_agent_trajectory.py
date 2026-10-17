import json
from pathlib import Path
import pytest
from pydantic import BaseModel, Field
from google import genai
from google.genai import types


class TrajectoryVerdict(BaseModel):
    passed: bool = Field(description="True if the agent response is grounded in tool outputs.")
    score: float = Field(ge=0.0, le=1.0, description="Groundedness score from 0.0 to 1.0.")
    reasoning: str = Field(description="Concise explanation of any hallucination or omission.")


def load_golden_cases() -> list[dict]:
    dataset_path = Path(__file__).parent.parent / "datasets" / "golden_trajectories.jsonl"
    with dataset_path.open("r", encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


@pytest.mark.parametrize("case", load_golden_cases(), ids=lambda c: c["test_id"])
def test_expected_tool_trajectory(case: dict, run_triage_agent):
    """Verifies that the agent invokes the required tool sequence without forbidden tools."""
    execution_trace = run_triage_agent(prompt=case["user_prompt"])

    called_tools = [step.tool_name for step in execution_trace.tool_calls]
    assert called_tools == case["expected_tool_sequence"], (
        f"Trajectory mismatch for {case['test_id']}: "
        f"expected {case['expected_tool_sequence']}, got {called_tools}"
    )

    for forbidden in case.get("forbidden_tools", []):
        assert forbidden not in called_tools, f"Agent invoked forbidden tool: {forbidden}"


@pytest.mark.live_eval
def test_response_groundedness_with_gemini_judge(run_triage_agent):
    """Evaluates whether the agent's final synthesis stays strictly grounded in tool data."""
    client = genai.Client()
    trace = run_triage_agent(prompt="Check error spikes for service auth-api in the last hour.")

    judge_prompt = f"""
    You are an AI Quality Judge. Evaluate whether the Agent Response relies strictly
    on the Tool Output without fabricating metrics or root causes.

    Tool Output: {json.dumps(trace.raw_tool_outputs)}
    Agent Response: {trace.final_answer}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=judge_prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TrajectoryVerdict,
            temperature=0.0,
        ),
    )
    verdict = TrajectoryVerdict.model_validate_json(response.text)
    assert verdict.passed and verdict.score >= 0.85, f"Groundedness failed: {verdict.reasoning}"