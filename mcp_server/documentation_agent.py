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

EXAMPLE_CONTENT = {
    'project_name': 'Multi-Agent MCP Server',
    'overview': 'A server for orchestrating multi-agent code reviews with strict compliance to open-source and enterprise standards.',
    'contact': 'maintainer@example.com',
    'api_version': 'v1.0.0',
    'architecture_diagram': '<svg><!-- Example SVG --></svg>',
    'license': 'MIT',
}

def load_template(path: str) -> str:
    if not os.path.exists(path):
        return f"# Template missing: {path}\n"
    with open(path, 'r') as f:
        return f.read()

def generate_documentation_files() -> Dict[str, str]:
    files = {}
    for filename, template_path in TEMPLATE_PATHS.items():
        content = load_template(template_path)
        # For demonstration, just fill in example content
        content = content.replace('{{project_name}}', EXAMPLE_CONTENT['project_name'])
        content = content.replace('{{overview}}', EXAMPLE_CONTENT['overview'])
        content = content.replace('{{contact}}', EXAMPLE_CONTENT['contact'])
        content = content.replace('{{api_version}}', EXAMPLE_CONTENT['api_version'])
        if filename == 'architecture.svg':
            content = EXAMPLE_CONTENT['architecture_diagram']
        if filename == 'LICENSE':
            content = EXAMPLE_CONTENT['license']
        files[filename] = content
    return files

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
    files = generate_documentation_files()
    review = review_documentation_with_gemini(files)
    try:
        doc_output = DocumentationOutput(files=files, review=review)
    except ValidationError as e:
        raise RuntimeError(f"Documentation output validation failed: {e}")
    return doc_output

if __name__ == "__main__":
    output = run_documentation_agent()
    for fname, content in output.files.items():
        print(f"--- {fname} ---\n{content[:200]}...\n")
    print("\nGemini Review:\n", output.review)

