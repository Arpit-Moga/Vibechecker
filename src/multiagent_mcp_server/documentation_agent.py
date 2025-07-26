"""
Production-ready documentation generator using DSPy and Pydantic.

This module provides a robust documentation generation system that:
- Analyzes code files and generates appropriate documentation
- Uses templates for consistent documentation structure
- Provides validation and error handling
- Supports multiple LLM providers with fallback
- Writes documentation files to DOCUMENTATION folder
"""

from src.multiagent_mcp_server.error_utils import get_logger, handle_errors
import os
import json
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Union
from datetime import datetime

import dspy
from pydantic import BaseModel, Field, ValidationError, field_validator
from pydantic_settings import BaseSettings

from .config import Settings
from .agent_utils import SupportedFileType, CodeFile, FileProcessor

logger = get_logger("multiagent_mcp_server.documentation_agent")

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
        summary_parts.append("## Project Structure Overview")
        summary_parts.append(f"Total files analyzed: {len(code_files)}")
        file_types = {}
        for code_file in code_files.values():
            file_type = code_file.file_type.value
            file_types[file_type] = file_types.get(file_type, 0) + 1
        summary_parts.append("\n### File Distribution:")
        for file_type, count in file_types.items():
            summary_parts.append(f"- {file_type}: {count} files")
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
    def _write_documentation_files(self, output: DocumentationOutput, output_dir: Path) -> dict:
        """Write documentation files to the filesystem."""
        output_dir.mkdir(parents=True, exist_ok=True)
        written_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for filename, doc_file in output.files.items():
            file_path = output_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(doc_file.content)
            written_files.append(str(file_path))
            logger.info(f"Documentation file written: {file_path}")
        summary_file = output_dir / f"documentation_summary_{timestamp}.md"
        summary_content = self._generate_summary_report(output, timestamp)
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary_content)
        written_files.append(str(summary_file))
        metadata_file = output_dir / f"documentation_metadata_{timestamp}.json"
        metadata = {
            "timestamp": datetime.now().isoformat(),
            "agent_type": "documentation",
            "files_generated": len(output.files),
            "file_list": list(output.files.keys()),
            "review": output.review,
            "metadata": output.metadata
        }
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        written_files.append(str(metadata_file))
        logger.info(f"Documentation generation complete. {len(written_files)} files written.")
        return {
            "written_files": written_files,
            "total_files": len(written_files),
            "documentation_files": len(output.files),
            "output_directory": str(output_dir)
        }
    def _generate_summary_report(self, output: DocumentationOutput, timestamp: str) -> str:
        """Generate a summary report of the documentation generation."""
        md_lines = [
            "# Documentation Generation Summary",
            f"",
            f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"**Agent:** Documentation Generator",
            f"**Files Generated:** {len(output.files)}",
            f"",
            "## Files Created",
            f""
        ]
        for filename, doc_file in output.files.items():
            file_size = len(doc_file.content)
            md_lines.append(f"- **{filename}** ({file_size:,} characters)")
        md_lines.extend([
            f"",
            "## Quality Review",
            f"",
            output.review,
            f"",
            "## Metadata",
            f""
        ])
        for key, value in output.metadata.items():
            md_lines.append(f"- **{key}:** {value}")
        md_lines.extend([
            f"",
            "## Next Steps",
            f"",
            "1. **Review Generated Documentation:** Verify all documentation meets project requirements",
            "2. **Customize Content:** Update any placeholder content or project-specific details", 
            "3. **Integration:** Integrate documentation into your project repository",
            "4. **Maintenance:** Establish a process for keeping documentation up-to-date",
            "",
            "---",
            f"*Report generated by Multi-Agent MCP Server - Documentation Generator*"
        ])
        return "\n".join(md_lines)
    def generate_documentation(self, output_dir: Optional[str] = None) -> DocumentationOutput:
        """Generate complete documentation for the project."""
        try:
            code_dir = Path(self.settings.code_directory)
            if not code_dir.exists():
                raise DocumentationGenerationError(f"Code directory not found: {code_dir}")
            code_files = self.file_processor.get_code_files(code_dir)
            template_files = self.file_processor.get_template_files()
            code_summary = self._create_code_summary(code_files)
            template_examples = "\n\n".join([
                f"--- {template.doc_type.value} Template ---\n{template.content}"
                for template in template_files.values()
            ])
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
                    doc_file = DocumentationFile(
                        name=doc_type.value,
                        content=f"# {doc_type.value}\n\nContent generation failed: {e}",
                        doc_type=doc_type
                    )
                    generated_files[doc_type.value] = doc_file
            docs_for_review = "\n\n".join([
                f"--- {doc_file.name} ---\n{doc_file.content}"
                for doc_file in generated_files.values()
            ])
            review = self.reviewer.forward(
                documentation_files=docs_for_review,
                code_summary=code_summary
            )
            metadata = {
                "total_files_processed": len(code_files),
                "documentation_files_generated": len(generated_files),
                "code_directory": str(code_dir),
                "template_directory": self.settings.template_directory,
            }
            output = DocumentationOutput(
                files=generated_files,
                review=review,
                metadata=metadata
            )
            if output_dir:
                doc_dir = Path(output_dir) / "DOCUMENTATION"
            else:
                doc_dir = Path(self.settings.code_directory) / "DOCUMENTATION"
            file_info = self._write_documentation_files(output, doc_dir)
            logger.info(f"Documentation generation complete. Files written: {file_info}")
            return output
        except Exception as e:
            logger.error(f"Documentation generation failed: {e}")
            raise DocumentationGenerationError(f"Failed to generate documentation: {e}")

@handle_errors(logger=logger, context="DocumentationAgent.main")
def main(output_dir: Optional[str] = None):
    """Main entry point for the documentation generator."""
    settings = Settings()
    agent = DocumentationAgent(settings)
    logger.info("Starting documentation generation...")
    output = agent.generate_documentation(output_dir=output_dir)
    logger.info("Documentation generation completed successfully")
    return output

if __name__ == "__main__":
    main()