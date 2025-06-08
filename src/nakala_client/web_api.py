"""
NAKALA Web API Service

FastAPI-based REST API for web interface integration with O-Nakala Core.
Provides endpoints for all intelligence services and metadata management.
Part of Phase 4: Advanced UI & Integration Features.
"""

import json
import logging
import asyncio
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import tempfile
import shutil

try:
    from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends, BackgroundTasks
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse, FileResponse
    from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
    from pydantic import BaseModel, Field
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    
    # Mock classes for when FastAPI isn't available
    class BaseModel:
        pass
    class Field:
        def __init__(self, **kwargs): pass

from .curator import NakalaCuratorClient, CuratorConfig
from .common.config import NakalaConfig
from .common.exceptions import NakalaAPIError
from .common.utils import NakalaCommonUtils

logger = logging.getLogger(__name__)

# Pydantic models for API requests/responses
class APIKeyRequest(BaseModel):
    api_key: str = Field(..., description="NAKALA API key")
    api_url: str = Field(default="https://apitest.nakala.fr", description="NAKALA API URL")

class TemplateGenerationRequest(BaseModel):
    resource_type: str = Field(..., description="Type of resource (dataset, collection, etc.)")
    template_name: Optional[str] = Field(None, description="Custom template name")
    include_optional: bool = Field(default=True, description="Include optional fields")
    user_context: Optional[Dict[str, Any]] = Field(default=None, description="Additional user context")

class AutonomousGenerationRequest(BaseModel):
    resource_type: str = Field(..., description="Type of resource")
    user_context: Optional[Dict[str, Any]] = Field(default=None, description="Additional context")

class PredictiveAnalysisRequest(BaseModel):
    timeframes: Optional[List[str]] = Field(default=None, description="Prediction timeframes")
    include_quality: bool = Field(default=True, description="Include quality predictions")
    include_completeness: bool = Field(default=True, description="Include completeness predictions")
    include_usage: bool = Field(default=True, description="Include usage predictions")

class BatchModificationRequest(BaseModel):
    modifications: List[Dict[str, Any]] = Field(..., description="List of modifications to apply")
    dry_run: bool = Field(default=True, description="Perform dry run without actual changes")

class RelationshipDiscoveryRequest(BaseModel):
    metadata: Dict[str, Any] = Field(..., description="Source metadata for relationship discovery")
    resource_id: Optional[str] = Field(None, description="Resource identifier")
    max_suggestions: int = Field(default=5, description="Maximum relationship suggestions")

class FieldSuggestionsRequest(BaseModel):
    field_name: str = Field(..., description="Field name for suggestions")
    partial_value: str = Field(..., description="Partial value to complete")
    limit: int = Field(default=5, description="Maximum suggestions to return")

# Response models
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    processing_time: Optional[float] = None

class TemplateResponse(BaseModel):
    template: Dict[str, Any]
    field_count: int
    required_fields: int
    documentation: str

class AutonomousGenerationResponse(BaseModel):
    generated_metadata: Dict[str, str]
    quality_score: float
    completeness_score: float
    confidence_scores: Dict[str, float]
    content_analysis: Dict[str, Any]
    processing_time: float
    recommendations: List[str]

class PredictiveAnalysisResponse(BaseModel):
    health_score: float
    quality_predictions: List[Dict[str, Any]]
    completeness_predictions: List[Dict[str, Any]]
    usage_predictions: List[Dict[str, Any]]
    key_insights: List[str]
    strategic_recommendations: List[str]
    processing_time: float


class NakalaWebAPI:
    """Main Web API service for O-Nakala Core."""
    
    def __init__(self):
        if not FASTAPI_AVAILABLE:
            raise ImportError("FastAPI is required for web API functionality. Install with: pip install fastapi uvicorn")
        
        self.app = FastAPI(
            title="O-Nakala Core Web API",
            description="Advanced AI-driven metadata management for NAKALA repositories",
            version="4.0.0",
            docs_url="/docs",
            redoc_url="/redoc"
        )
        
        # Configure CORS for web interface
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Configure appropriately for production
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        # Security
        self.security = HTTPBearer()
        
        # Temporary file management
        self.temp_dir = Path(tempfile.gettempdir()) / "nakala_api"
        self.temp_dir.mkdir(exist_ok=True)
        
        # Setup routes
        self._setup_routes()
        
        logger.info("O-Nakala Core Web API initialized")
    
    def _setup_routes(self):
        """Setup all API routes."""
        
        # Health check
        @self.app.get("/", response_model=APIResponse)
        async def health_check():
            return APIResponse(
                success=True,
                message="O-Nakala Core Web API is running",
                data={
                    "version": "4.0.0",
                    "features": ["autonomous_generation", "predictive_analytics", "intelligent_templates"],
                    "status": "operational"
                }
            )
        
        # Authentication helper
        async def get_curator(credentials: HTTPAuthorizationCredentials = Depends(self.security)) -> NakalaCuratorClient:
            """Get curator client with API key from authorization header."""
            api_key = credentials.credentials
            try:
                config = CuratorConfig(
                    api_url="https://apitest.nakala.fr",  # Default to test API
                    api_key=api_key
                )
                return NakalaCuratorClient(config)
            except Exception as e:
                raise HTTPException(status_code=401, detail=f"Invalid API key: {str(e)}")
        
        # Template generation endpoints
        @self.app.post("/api/v1/templates/generate", response_model=TemplateResponse)
        async def generate_template(
            request: TemplateGenerationRequest,
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Generate intelligent metadata template."""
            try:
                start_time = datetime.now()
                
                template = await curator.generate_metadata_template(
                    resource_type=request.resource_type,
                    template_name=request.template_name,
                    user_context=request.user_context,
                    include_optional=request.include_optional
                )
                
                if not template:
                    raise HTTPException(status_code=500, detail="Template generation failed")
                
                processing_time = (datetime.now() - start_time).total_seconds()
                documentation = curator.generate_template_documentation(template)
                
                return TemplateResponse(
                    template={
                        "name": template.name,
                        "description": template.description,
                        "resource_type": template.resource_type,
                        "fields": [
                            {
                                "name": field.name,
                                "property_uri": field.property_uri,
                                "required": field.required,
                                "multilingual": field.multilingual,
                                "data_type": field.data_type,
                                "examples": field.examples,
                                "help_text": field.help_text,
                                "default_value": field.default_value
                            }
                            for field in template.fields
                        ]
                    },
                    field_count=len(template.fields),
                    required_fields=len(template.get_required_fields()),
                    documentation=documentation
                )
                
            except Exception as e:
                logger.error(f"Template generation failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Autonomous generation endpoints
        @self.app.post("/api/v1/autonomous/generate", response_model=AutonomousGenerationResponse)
        async def generate_autonomous_metadata(
            request: AutonomousGenerationRequest,
            file: UploadFile = File(...),
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Generate metadata autonomously from file analysis."""
            temp_file_path = None
            try:
                # Save uploaded file temporarily
                temp_file_path = self.temp_dir / f"upload_{datetime.now().timestamp()}_{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Generate autonomous metadata
                result = await curator.generate_autonomous_metadata(
                    file_path=str(temp_file_path),
                    resource_type=request.resource_type,
                    user_context=request.user_context
                )
                
                if not result:
                    raise HTTPException(status_code=500, detail="Autonomous generation failed")
                
                return AutonomousGenerationResponse(
                    generated_metadata=result.generated_metadata,
                    quality_score=result.quality_score,
                    completeness_score=result.completeness_score,
                    confidence_scores=result.confidence_scores,
                    content_analysis={
                        "content_type": result.content_analysis.content_type,
                        "detected_language": result.content_analysis.detected_language,
                        "confidence_score": result.content_analysis.confidence_score,
                        "extracted_features": result.content_analysis.extracted_features,
                        "processing_notes": result.content_analysis.processing_notes
                    },
                    processing_time=result.processing_time,
                    recommendations=result.recommendations
                )
                
            except Exception as e:
                logger.error(f"Autonomous generation failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
            finally:
                # Cleanup temporary file
                if temp_file_path and temp_file_path.exists():
                    temp_file_path.unlink()
        
        # Predictive analytics endpoints
        @self.app.post("/api/v1/analytics/predict", response_model=PredictiveAnalysisResponse)
        async def generate_predictive_analysis(
            request: PredictiveAnalysisRequest,
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Generate predictive analysis report."""
            try:
                result = await curator.generate_predictive_analysis_report(
                    custom_timeframes=request.timeframes,
                    include_quality=request.include_quality,
                    include_completeness=request.include_completeness,
                    include_usage=request.include_usage
                )
                
                if not result:
                    raise HTTPException(status_code=500, detail="Predictive analysis failed")
                
                return PredictiveAnalysisResponse(
                    health_score=result.overall_health_score,
                    quality_predictions=[
                        {
                            "metric_name": pred.metric_name,
                            "current_value": pred.current_value,
                            "predicted_value": pred.predicted_value,
                            "timeframe": pred.prediction_timeframe,
                            "confidence": pred.confidence,
                            "trend": pred.trend_direction,
                            "recommendations": pred.recommendations
                        }
                        for pred in result.quality_predictions
                    ],
                    completeness_predictions=[
                        {
                            "field_name": pred.field_name,
                            "current_rate": pred.current_completion_rate,
                            "predicted_rate": pred.predicted_completion_rate,
                            "timeframe": pred.prediction_timeframe,
                            "confidence": pred.confidence,
                            "priority": pred.priority_level,
                            "actions": pred.suggested_actions
                        }
                        for pred in result.completeness_predictions
                    ],
                    usage_predictions=[
                        {
                            "metric": pred.usage_metric,
                            "current_value": pred.current_value,
                            "predicted_value": pred.predicted_value,
                            "timeframe": pred.prediction_timeframe,
                            "confidence": pred.confidence,
                            "growth_indicators": pred.growth_indicators,
                            "capacity_recommendations": pred.capacity_recommendations
                        }
                        for pred in result.usage_predictions
                    ],
                    key_insights=result.key_insights,
                    strategic_recommendations=result.strategic_recommendations,
                    processing_time=result.processing_time
                )
                
            except Exception as e:
                logger.error(f"Predictive analysis failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Relationship discovery endpoints
        @self.app.post("/api/v1/relationships/discover", response_model=APIResponse)
        async def discover_relationships(
            request: RelationshipDiscoveryRequest,
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Discover relationships for metadata."""
            try:
                analysis = await curator.discover_relationships_for_metadata(
                    metadata=request.metadata,
                    resource_id=request.resource_id,
                    max_suggestions=request.max_suggestions
                )
                
                if analysis:
                    return APIResponse(
                        success=True,
                        message=f"Found {len(analysis.suggestions)} relationship suggestions",
                        data={
                            "suggestions": [
                                {
                                    "target_id": sugg.target_id,
                                    "target_title": sugg.target_title,
                                    "relationship_type": sugg.relationship_type,
                                    "confidence": sugg.confidence,
                                    "reason": sugg.reason
                                }
                                for sugg in analysis.suggestions
                            ],
                            "processing_time": analysis.processing_time,
                            "analysis_notes": analysis.analysis_notes
                        }
                    )
                else:
                    return APIResponse(
                        success=True,
                        message="No relationships discovered",
                        data={"suggestions": []}
                    )
                
            except Exception as e:
                logger.error(f"Relationship discovery failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Field suggestions endpoints
        @self.app.post("/api/v1/suggestions/field", response_model=APIResponse)
        async def get_field_suggestions(
            request: FieldSuggestionsRequest,
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Get vocabulary suggestions for a field."""
            try:
                suggestions = await curator.get_field_suggestions(
                    field_name=request.field_name,
                    partial_value=request.partial_value,
                    limit=request.limit
                )
                
                return APIResponse(
                    success=True,
                    message=f"Found {len(suggestions)} suggestions",
                    data={"suggestions": suggestions}
                )
                
            except Exception as e:
                logger.error(f"Field suggestions failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Batch processing endpoints
        @self.app.post("/api/v1/batch/modify", response_model=APIResponse)
        async def batch_modify_metadata(
            request: BatchModificationRequest,
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Apply batch metadata modifications."""
            try:
                result = curator.batch_modify_metadata(
                    modifications=request.modifications,
                    dry_run=request.dry_run
                )
                
                summary = result.get_summary()
                
                return APIResponse(
                    success=True,
                    message=f"Batch modification {'simulation' if request.dry_run else 'completed'}",
                    data={
                        "summary": summary,
                        "successful": len(result.successful),
                        "failed": len(result.failed),
                        "skipped": len(result.skipped),
                        "warnings": result.warnings,
                        "details": {
                            "successful": result.successful,
                            "failed": result.failed,
                            "skipped": result.skipped
                        }
                    }
                )
                
            except Exception as e:
                logger.error(f"Batch modification failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # CSV processing endpoints
        @self.app.post("/api/v1/csv/parse", response_model=APIResponse)
        async def parse_csv_modifications(
            file: UploadFile = File(...),
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Parse CSV file for modifications."""
            temp_file_path = None
            try:
                # Save uploaded CSV temporarily
                temp_file_path = self.temp_dir / f"csv_{datetime.now().timestamp()}_{file.filename}"
                with open(temp_file_path, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Parse CSV
                modifications, unsupported_fields = curator.parse_csv_modifications(str(temp_file_path))
                
                return APIResponse(
                    success=True,
                    message=f"Parsed {len(modifications)} modifications from CSV",
                    data={
                        "modifications": modifications,
                        "unsupported_fields": list(unsupported_fields),
                        "supported_count": len(modifications),
                        "unsupported_count": len(unsupported_fields)
                    }
                )
                
            except Exception as e:
                logger.error(f"CSV parsing failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
            finally:
                # Cleanup temporary file
                if temp_file_path and temp_file_path.exists():
                    temp_file_path.unlink()
        
        # Template export endpoints
        @self.app.post("/api/v1/templates/export/csv")
        async def export_template_csv(
            request: TemplateGenerationRequest,
            mode: str = Form(default="create"),
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Export template as CSV file."""
            try:
                # Generate template
                template = await curator.generate_metadata_template(
                    resource_type=request.resource_type,
                    template_name=request.template_name,
                    include_optional=request.include_optional
                )
                
                if not template:
                    raise HTTPException(status_code=500, detail="Template generation failed")
                
                # Export to temporary CSV
                csv_path = self.temp_dir / f"template_{datetime.now().timestamp()}.csv"
                curator.export_template_to_csv(template, str(csv_path), mode=mode)
                
                return FileResponse(
                    path=str(csv_path),
                    filename=f"{template.name}_{mode}.csv",
                    media_type="text/csv"
                )
                
            except Exception as e:
                logger.error(f"Template CSV export failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        # Quality analysis endpoints
        @self.app.get("/api/v1/quality/report", response_model=APIResponse)
        async def generate_quality_report(
            scope: str = "all",
            curator: NakalaCuratorClient = Depends(get_curator)
        ):
            """Generate quality report for user's data."""
            try:
                report = curator.generate_quality_report(scope=scope)
                
                return APIResponse(
                    success=True,
                    message="Quality report generated successfully",
                    data=report
                )
                
            except Exception as e:
                logger.error(f"Quality report generation failed: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    def run(self, host: str = "0.0.0.0", port: int = 8000, debug: bool = False):
        """Run the web API server."""
        try:
            import uvicorn
            uvicorn.run(self.app, host=host, port=port, debug=debug)
        except ImportError:
            raise ImportError("uvicorn is required to run the web API. Install with: pip install uvicorn")


# Factory function
def create_web_api() -> NakalaWebAPI:
    """Create web API instance."""
    return NakalaWebAPI()


# CLI entry point for running the API server
def main():
    """Main entry point for running the web API server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="O-Nakala Core Web API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    try:
        api = create_web_api()
        print(f"🚀 Starting O-Nakala Core Web API on http://{args.host}:{args.port}")
        print(f"📚 API Documentation: http://{args.host}:{args.port}/docs")
        api.run(host=args.host, port=args.port, debug=args.debug)
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Install with: pip install fastapi uvicorn")
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")


if __name__ == "__main__":
    main()