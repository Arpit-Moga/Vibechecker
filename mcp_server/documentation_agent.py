import os
from typing import Dict
from pydantic import ValidationError
from mcp_server.models import DocumentationOutput
from langchain_google_genai import ChatGoogleGenerativeAI

TEMPLATE_PATHS = {
    'README.md': '/home/arpit/coding/multi-agent/docs/templates/README_template.md',
    'CONTRIBUTING.md': '/home/arpit/coding/multi-agent/docs/templates/CONTRIBUTING_template.md',
    'CODE_OF_CONDUCT.md': '/home/arpit/coding/multi-agent/docs/templates/CODE_OF_CONDUCT_template.md',
    'swagger.yaml': '/home/arpit/coding/multi-agent/docs/templates/API_template.md',
    'schema.graphql': '/home/arpit/coding/multi-agent/docs/templates/API_template.md',
    'architecture.svg': '/home/arpit/coding/multi-agent/docs/templates/ARCHITECTURE_template.md',
    'ONBOARDING.md': '/home/arpit/coding/multi-agent/docs/templates/ONBOARDING_template.md',
    'RUNBOOK.md': '/home/arpit/coding/multi-agent/docs/templates/RUNBOOK_template.md',
    'SECURITY.md': '/home/arpit/coding/multi-agent/docs/templates/SECURITY_template.md',
    'CHANGELOG.md': '/home/arpit/coding/multi-agent/docs/templates/CHANGELOG_template.md',
    'TESTING.md': '/home/arpit/coding/multi-agent/docs/templates/TESTING_template.md',
    'DEPENDENCY.md': '/home/arpit/coding/multi-agent/docs/templates/DEPENDENCY_template.md',
    'LICENSE': '/home/arpit/coding/multi-agent/docs/templates/LICENSE_template.md',
}


def load_template(path: str) -> str:
    if not os.path.exists(path):
        return f"# Template missing: {path}\n"
    with open(path, 'r') as f:
        return f.read()

def get_code_files(code_dir: str) -> Dict[str, str]:
    files = {}
    for fname in os.listdir(code_dir):
        if fname.endswith('.py'):
            with open(os.path.join(code_dir, fname), "r") as f:
                files[fname] = f.read()
    return files


def get_template_examples() -> Dict[str, str]:
    examples = {}
    for doc_name, template_path in TEMPLATE_PATHS.items():
        examples[doc_name] = load_template(template_path)
    return examples

def summarize_code_files(files: Dict[str, str]) -> str:
    summary = ""
    for fname, content in files.items():
        if fname.endswith('.py'):
            # Simple summary: filename and first 5 lines
            lines = content.splitlines()
            summary += f"\n--- {fname} ---\n" + "\n".join(lines[:5]) + "\n...\n"
    return summary


def generate_documentation_with_llm(code_files: Dict[str, str], template_examples: Dict[str, str]) -> Dict[str, str]:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = "You are an expert documentation generator. Given the following code files, and example documentation templates, create documentation files (README.md, CONTRIBUTING.md, etc.) for this codebase. Do NOT review or output the templates. Only generate new documentation files for the codebase, following the style and structure of the templates.\n\n"
    prompt += "## Code files\n"
    for fname, content in code_files.items():
        prompt += f"--- {fname} ---\n{content}\n\n"
    prompt += "## Documentation template examples\n"
    for doc_name, template in template_examples.items():
        prompt += f"--- {doc_name} (template example) ---\n{template}\n\n"
    prompt += "\nGenerate the following documentation files for the codebase: " + ", ".join(template_examples.keys()) + ". Output each file as: --- filename ---\n<content>\n"
    result = llm.invoke(prompt)
    # Parse output into files
    output_files = {}
    for doc_name in template_examples.keys():
        marker = f"--- {doc_name} ---"
        if marker in result.content:
            start = result.content.index(marker) + len(marker)
            end = result.content.find("---", start)
            if end == -1:
                end = len(result.content)
            output_files[doc_name] = result.content[start:end].strip()
        else:
            output_files[doc_name] = ""
    return output_files

def review_documentation_with_gemini(files: Dict[str, str]) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set.")
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    prompt = "You are an expert documentation reviewer. Review the following documentation files for completeness, clarity, and compliance with open-source and enterprise standards. Provide a detailed review and suggestions for improvement.\n\n"
    for fname, content in files.items():
        prompt += f"--- {fname} ---\n{content}\n\n"
    result = llm.invoke(prompt)
    return result.content

def run_documentation_agent() -> DocumentationOutput:
    code_dir = "/home/arpit/coding/multi-agent/Example-project"
    code_files = get_code_files(code_dir)
    template_examples = get_template_examples()
    documentation_files = generate_documentation_with_llm(code_files, template_examples)
    # Optionally, review the generated documentation files
    review = "Documentation files generated for codebase."
    try:
        doc_output = DocumentationOutput(files=documentation_files, review=review)
    except ValidationError as e:
        raise RuntimeError(f"Documentation output validation failed: {e}")
    return doc_output

if __name__ == "__main__":
    output = run_documentation_agent()
    for fname, content in output.files.items():
        print(f"--- {fname} ---\n{content[:200]}...\n")
    print("\nDocumentation Agent Status:\n", output.review)

