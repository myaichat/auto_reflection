
# Blog Writing Pipeline with Agent Reflection

This repository contains a custom Python-based pipeline that automates the process of generating, reflecting, and refining blog content. The pipeline leverages multiple agents (Writer, Critic, SEO Reviewer, Legal Reviewer, Ethics Reviewer, Meta Summarizer) to create high-quality content, optimized for SEO, legally compliant, and ethically sound.

## Features
- **Dynamic Agent-Based Reflection**: Each agent (Writer, Critic, Reviewers) plays a role in generating and improving the blog topics.
- **YAML-Based Configuration**: Flexible task and agent definitions using a simple YAML file.
- **Custom Python Implementation**: Tailored for blog content creation with detailed agent orchestration.
- **Extensible Pipeline**: Easily add or modify agents and tasks as needed.

## Table of Contents
1. [Installation](#installation)
2. [Usage](#usage)
3. [Pipeline Overview](#pipeline-overview)
4. [Sample Output](#sample-output)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/blog-writing-pipeline.git
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Ensure you have the following directory structure:

    ```plaintext
    blog-writing-pipeline/
    ├── config/
    │   └── topics.yaml
    ├── include/
    │   └── agents/
    ├── pipeline/
    │   └── blog_writer.py
    └── main.py
    ```

## Usage

1. Define the blog title and execute the pipeline:

    ```python
    if __name__ == '__main__':
        title = "Using Agent Reflection for Writing a Blog"
        execute_pipeline(title, "blog_writer", "config/topics.yaml")
    ```

2. Run the Python script:

    ```bash
    python main.py
    ```

3. The pipeline will generate blog titles and pass them through various agents for refinement. The final output will be printed to the console.

## Pipeline Overview

The pipeline uses the following agents:
- **Writer**: Generates the initial blog titles.
- **Critic**: Reviews the titles and suggests improvements.
- **SEO Reviewer**: Optimizes the content for search engines.
- **Legal Reviewer**: Ensures the content complies with copyright and privacy laws.
- **Ethics Reviewer**: Checks for ethical concerns.
- **Meta Summarizer**: Aggregates feedback and provides the final refined output.

## Sample Output

```plaintext
╭─ Final Blog Titles: ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ 1. Introduction: The Role of Agent Reflection in AI-Powered Blog Writing                                             │
│ 2. Understanding the Benefits of Multi-Agent Collaboration in Content Creation                                       │
│ 3. SEO Optimization and Compliance: How Agent Reflection Enhances Blog Quality                                       │
│ 4. Ethical and Legal Considerations in Automated Content Creation                                                    │
│ 5. Conclusion: The Future of AI-Powered Blogging with Agent Reflection                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## License

This project is licensed under the MIT License.
