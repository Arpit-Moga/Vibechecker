"""
Production-ready documentation generator using DSPy and Pydantic.

This module provides a robust documentation generation system that:
- Analyzes code files and generates appropriate documentation
- Uses templates for consistent documentation structure
- Provides validation and error handling
- Supports multiple LLM providers with fallback
"""

import logging
import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union

import dspy
from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_settings import BaseSettings


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


from multiagent_mcp_server.agent_utils import SupportedFileType, Settings, CodeFile, FileProcessor

class DocumentationType(str, Enum):
    """Types of documentation that can be generated."""
    README = "README.md"
    CONTRIBUTING = "CONTRIBUTING.md"
    ONBOARDING = "ONBOARDING.md"
    RUNBOOK = "RUNBOOK.md"
    TESTING = "TESTING.md"
    DEPENDENCY = "DEPENDENCY.md"
    LICENSE = "LICENSE"

class TemplateFile(BaseModel):
    """Represents a documentation template."""
    
    name: str = Field(..., description="Template name")
    content: str = Field(..., description="Template content")
    doc_type: DocumentationType = Field(..., description="Documentation type")


class DocumentationFile(BaseModel):
    """Represents a generated documentation file."""
    
    name: str = Field(..., description="Documentation file name")
    content: str = Field(..., description="Generated content")
    doc_type: DocumentationType = Field(..., description="Documentation type")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        if len(v.strip()) < 10:
            raise ValueError("Documentation content is too short")
        return v


class DocumentationOutput(BaseModel):
    """Complete documentation generation output."""
    
    files: Dict[str, DocumentationFile] = Field(..., description="Generated documentation files")
    review: str = Field(..., description="Review and quality assessment")
    metadata: Dict[str, Union[str, int, float]] = Field(default_factory=dict)
    
    @field_validator('files')
    @classmethod
    def validate_files(cls, v):
        if not v:
            raise ValueError("At least one documentation file must be generated")
        return v


class DocumentationGenerationError(Exception):
    """Custom exception for documentation generation errors."""
    pass




class DocumentationGeneratorSignature(dspy.Signature):
    """DSPy signature for documentation generation."""
    
    code_summary: str = dspy.InputField(
        desc="Comprehensive summary of the codebase including structure, functionality, and key components"
    )
    template_examples: str = dspy.InputField(
        desc="Documentation templates showing the expected format and structure"
    )
    doc_type: str = dspy.InputField(
        desc="Type of documentation to generate (e.g., README.md, CONTRIBUTING.md)"
    )
    documentation: str = dspy.OutputField(
        desc="Complete, well-structured documentation content following the template format"
    )


class DocumentationReviewSignature(dspy.Signature):
    """DSPy signature for documentation review."""
    
    documentation_files: str = dspy.InputField(
        desc="All generated documentation files with their content"
    )
    code_summary: str = dspy.InputField(
        desc="Summary of the original codebase"
    )
    review_report: str = dspy.OutputField(
        desc="Detailed review report with quality assessment, completeness check, and improvement suggestions"
    )


class DocumentationGenerator(dspy.Module):
    """DSPy module for generating documentation."""
    
    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(DocumentationGeneratorSignature)
    
    def forward(self, code_summary: str, template_examples: str, doc_type: str) -> str:
        """Generate documentation for a specific type."""
        try:
            result = self.generate(
                code_summary=code_summary,
                template_examples=template_examples,
                doc_type=doc_type
            )
            return result.documentation
        except Exception as e:
            logger.error(f"Error generating documentation for {doc_type}: {e}")
            return f"# {doc_type}\n\nError generating documentation: {e}\n"


class DocumentationReviewer(dspy.Module):
    """DSPy module for reviewing generated documentation."""
    
    def __init__(self):
        super().__init__()
        self.review = dspy.ChainOfThought(DocumentationReviewSignature)
    
    def forward(self, documentation_files: str, code_summary: str) -> str:
        """Review all generated documentation."""
        try:
            result = self.review(
                documentation_files=documentation_files,
                code_summary=code_summary
            )
            return result.review_report
        except Exception as e:
            logger.error(f"Error reviewing documentation: {e}")
            return f"Review failed: {e}"


class DocumentationAgent:
    """Main documentation generation agent."""
    
    def __init__(self, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.file_processor = FileProcessor(self.settings)
        self._setup_dspy()
        
        self.generator = DocumentationGenerator()
        self.reviewer = DocumentationReviewer()
    
    def _setup_dspy(self):
        """Configure DSPy with appropriate LLM."""
        try:
            if self.settings.google_api_key:
                dspy.configure(lm=dspy.LM(
                    model="gemini/gemini-2.5-flash",
                    api_key=self.settings.google_api_key
                ))
                logger.info("Configured DSPy with Gemini")
            elif self.settings.openai_api_key:
                dspy.configure(lm=dspy.LM(
                    model="openai/gpt-3.5-turbo",
                    api_key=self.settings.openai_api_key
                ))
                logger.info("Configured DSPy with OpenAI")
            else:
                logger.warning("No API keys found, using default DSPy configuration")
        except Exception as e:
            logger.error(f"Failed to configure DSPy: {e}")
            raise DocumentationGenerationError(f"LLM configuration failed: {e}")
    
    def _create_code_summary(self, code_files: Dict[str, CodeFile]) -> str:
        """Create a comprehensive summary of the codebase."""
        summary_parts = []
        
        # Project overview
        summary_parts.append("## Project Structure Overview")
        summary_parts.append(f"Total files analyzed: {len(code_files)}")
        
        # File type distribution
        file_types = {}
        for code_file in code_files.values():
            file_type = code_file.file_type.value
            file_types[file_type] = file_types.get(file_type, 0) + 1
        
        summary_parts.append("\n### File Distribution:")
        for file_type, count in file_types.items():
            summary_parts.append(f"- {file_type}: {count} files")
        
        # Individual file summaries
        summary_parts.append("\n## File Contents Summary:")
        for code_file in code_files.values():
            lines = code_file.content.splitlines()
            preview_lines = lines[:10] if len(lines) > 10 else lines
            
            summary_parts.append(f"\n### {code_file.name} ({code_file.file_type.value})")
            summary_parts.append(f"Path: {code_file.path}")
            summary_parts.append(f"Size: {code_file.size_bytes} bytes")
            summary_parts.append("Content preview:")
            summary_parts.extend(f"  {line}" for line in preview_lines)
            if len(lines) > 10:
                summary_parts.append(f"  ... ({len(lines) - 10} more lines)")
        
        return "\n".join(summary_parts)
    
    def generate_documentation(self) -> DocumentationOutput:
        """Generate complete documentation for the project."""
        try:
            # Load code files and templates
            code_dir = Path(self.settings.code_directory)
            if not code_dir.exists():
                raise DocumentationGenerationError(f"Code directory not found: {code_dir}")
            
            code_files = self.file_processor.get_code_files(code_dir)
            template_files = self.file_processor.get_template_files()
            
            # Create code summary
            code_summary = self._create_code_summary(code_files)
            
            # Prepare template examples
            template_examples = "\n\n".join([
                f"--- {template.doc_type.value} Template ---\n{template.content}"
                for template in template_files.values()
            ])
            
            # Generate documentation files
            generated_files = {}
            for doc_type in DocumentationType:
                logger.info(f"Generating {doc_type.value}")
                
                content = self.generator.forward(
                    code_summary=code_summary,
                    template_examples=template_examples,
                    doc_type=doc_type.value
                )
                
                try:
                    doc_file = DocumentationFile(
                        name=doc_type.value,
                        content=content,
                        doc_type=doc_type
                    )
                    generated_files[doc_type.value] = doc_file
                except ValidationError as e:
                    logger.error(f"Validation failed for {doc_type.value}: {e}")
                    # Create minimal valid content
                    doc_file = DocumentationFile(
                        name=doc_type.value,
                        content=f"# {doc_type.value}\n\nContent generation failed: {e}",
                        doc_type=doc_type
                    )
                    generated_files[doc_type.value] = doc_file
            
            # Review generated documentation
            docs_for_review = "\n\n".join([
                f"--- {doc_file.name} ---\n{doc_file.content}"
                for doc_file in generated_files.values()
            ])
            
            review = self.reviewer.forward(
                documentation_files=docs_for_review,
                code_summary=code_summary
            )
            
            # Create metadata
            metadata = {
                "total_files_processed": len(code_files),
                "documentation_files_generated": len(generated_files),
                "code_directory": str(code_dir),
                "template_directory": self.settings.template_directory,
            }
            
            return DocumentationOutput(
                files=generated_files,
                review=review,
                metadata=metadata
            )
            
        except Exception as e:
            logger.error(f"Documentation generation failed: {e}")
            raise DocumentationGenerationError(f"Failed to generate documentation: {e}")


def main():
    """Main entry point for the documentation generator."""
    try:
        settings = Settings()
        agent = DocumentationAgent(settings)
        
        logger.info("Starting documentation generation...")
        output = agent.generate_documentation()
        
        # Display results
        print("\n" + "="*80)
        print("DOCUMENTATION GENERATION COMPLETE")
        print("="*80)
        
        for file_name, doc_file in output.files.items():
            print(f"\n--- {file_name} ---")
            preview = doc_file.content[:3000] + "..." if len(doc_file.content) > 3000 else doc_file.content
            print(preview)
        
        print(f"\n--- REVIEW REPORT ---")
        print(output.review)
        
        print(f"\n--- METADATA ---")
        for key, value in output.metadata.items():
            print(f"{key}: {value}")
        
        logger.info("Documentation generation completed successfully")
        return output
        
    except Exception as e:
        logger.error(f"Application failed: {e}")
        raise


if __name__ == "__main__":
    main()