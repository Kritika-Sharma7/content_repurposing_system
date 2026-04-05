"""
FastAPI server exposing the multi-agent pipeline to external clients.
Used by the React frontend for real end-to-end execution.

UPGRADE v2: Enhanced API with user preferences and URL input support.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional, List, Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from pipeline.orchestrator import PipelineOrchestrator
from utils.llm import LLMClient, LLMError
from utils.content_fetcher import resolve_input, ContentFetchError
from config.user_preferences import UserPreferences
from config.platform_config import PlatformConfig, DEFAULT_PLATFORM_CONFIG
from config.settings import SystemSettings, DEFAULT_SETTINGS


load_dotenv()


class UserPreferencesRequest(BaseModel):
    """User preferences for content generation."""
    tone: Literal["professional", "conversational", "casual", "analytical", "storytelling"] = Field(
        default="professional"
    )
    audience: str = Field(default="general professionals")
    goal: Literal["engagement", "education", "awareness", "conversion", "thought-leadership"] = Field(
        default="engagement"
    )
    platforms: List[Literal["linkedin", "twitter", "newsletter"]] = Field(
        default=["linkedin", "twitter", "newsletter"]
    )


class PipelineRunRequest(BaseModel):
    """Request body for pipeline execution."""
    input_type: Literal["text", "url"] = Field(
        default="text",
        description="Type of input: 'text' for raw content, 'url' for web page"
    )
    content: str = Field(min_length=10, description="Content text or URL to process")
    user_preferences: Optional[UserPreferencesRequest] = Field(
        default=None,
        description="User preferences for content generation"
    )
    model: str = Field(default="gpt-4o", description="OpenAI model")
    temperature: float = Field(default=0.7, ge=0.0, le=1.0)
    api_key: Optional[str] = Field(default=None, description="Optional API key override")
    save_output: bool = Field(default=True)
    output_dir: str = Field(default="outputs")
    max_iterations: int = Field(
        default=2,
        ge=1,
        le=5,
        description="Maximum refinement iterations"
    )


class IterationInfo(BaseModel):
    """Summary of a refinement iteration."""
    iteration: int
    issues_fixed: int


class PipelineRunResponse(BaseModel):
    """Response from pipeline execution."""
    status: str
    executed_at: str
    total_issues: int
    issues_fixed: int
    total_iterations: int
    iterations: List[IterationInfo]
    result: dict


app = FastAPI(
    title="Multi-Agent Content API",
    version="2.0.0",
    description="Constraint-driven, platform-aware multi-agent content repurposing system"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health() -> dict:
    """Health check endpoint."""
    return {
        "status": "ok",
        "service": "multi-agent-content-api",
        "version": "2.0.0"
    }


@app.get("/api/config/platforms")
def get_platform_config() -> dict:
    """Get default platform configuration."""
    return DEFAULT_PLATFORM_CONFIG.model_dump()


@app.get("/api/config/settings")
def get_system_settings() -> dict:
    """Get default system settings."""
    return DEFAULT_SETTINGS.model_dump()


@app.post("/api/pipeline-run", response_model=PipelineRunResponse)
def run_pipeline(payload: PipelineRunRequest) -> PipelineRunResponse:
    """
    Execute the multi-agent content repurposing pipeline.
    
    Supports both text input and URL fetching.
    """
    # Resolve content (fetch URL if needed)
    try:
        content = resolve_input(
            payload.input_type,
            payload.content.strip()
        )
    except ContentFetchError as exc:
        raise HTTPException(status_code=400, detail=f"Failed to fetch URL: {exc}")
    
    if len(content) < 100:
        raise HTTPException(
            status_code=400,
            detail="Content must be at least 100 characters after fetching"
        )

    # Build user preferences
    user_prefs = None
    if payload.user_preferences:
        user_prefs = UserPreferences(
            tone=payload.user_preferences.tone,
            audience=payload.user_preferences.audience,
            goal=payload.user_preferences.goal,
            platforms=payload.user_preferences.platforms
        )

    try:
        llm_client = LLMClient(
            model=payload.model,
            temperature=payload.temperature,
            api_key=payload.api_key,
        )

        orchestrator = PipelineOrchestrator(
            llm_client=llm_client,
            verbose=False,
            max_iterations=payload.max_iterations
        )
        result = orchestrator.run(content, user_prefs)

        if payload.save_output:
            Path(payload.output_dir).mkdir(parents=True, exist_ok=True)
            orchestrator.save_results(result, payload.output_dir)

        # Build iteration summaries
        iterations_info = [
            IterationInfo(
                iteration=it.iteration,
                issues_fixed=it.issues_fixed
            )
            for it in result.iterations
        ]

        return PipelineRunResponse(
            status="success",
            executed_at=datetime.now().isoformat(),
            total_issues=result.total_issues,
            issues_fixed=result.issues_fixed,
            total_iterations=len(result.iterations),
            iterations=iterations_info,
            result=result.model_dump(),
        )

    except LLMError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except Exception as exc:
        import traceback
        print(f"[ERROR] Pipeline execution failed: {exc}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline execution failed: {exc}"
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("api_server:app", host="0.0.0.0", port=8000, reload=False)
