# Hi, I'm Rakesh

**SDET & AI Quality Engineer | Bengaluru, India**

I build automated testing frameworks, evaluation harnesses, and CI/CD quality gates for software systems and LLM-powered agents. Currently exploring AI agent testing with **Google ADK, Gemini API, and Vertex AI**.

### Technical Focus Areas
- **Agentic Workflow Testing:** Tool-call validation, multi-step workflow evaluation, and schema validation using `pytest` and `Pydantic`.
- **LLM Evaluation:** Prompt regression, hallucination detection, and response quality evaluation.
- **Test Infrastructure:** Mocking, synthetic test datasets, and GitHub Actions CI/CD automation.

### Featured Open-Source Work
- **[Gemini ADK Agent Testing](https://github.com/YOUR_USERNAME/gemini-adk-agent-testing)** — A Python testing framework for multi-tool AI agents built with Google ADK and the Gemini API.

### Connect
- **Location:** Bengaluru, India
- **LinkedIn:** (https://www.linkedin.com/in/rakesh-k-142ab483/)


## Architecture

```mermaid
flowchart TD
    A["GitHub Actions CI / Local Pytest"]

    A --> B["Fast PR Gate: Deterministic"]
    A --> C["Nightly / Release Gate: Live"]

    B --> D["Contract & Trajectory Tests"]
    D --> D1["Pydantic Schema Validation"]
    D --> D2["Recorded Tool-Call Mocks"]
    D --> D3["Max-Step & Loop Guards"]

    C --> E["Probabilistic LLM-as-Judge"]
    E --> E1["Golden Dataset (JSONL)"]
    E --> E2["Vertex AI / Gemini Judge"]
    E --> E3["Faithfulness & Tool-Use Rubric"]

    D --> F["Google ADK Multi-Tool Agent"]
    E --> F

    F --> G["Gemini Model + Structured Outputs"]
    F --> H["Custom Python Tools"]

    G --> I["JUnit XML + Markdown Evaluation Report"]
    H --> I
    I --> J["PR Comment / CI Artifacts"]
```
