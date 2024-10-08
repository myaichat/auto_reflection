
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
    git clone https://github.com/myaichat/auto_reflection.git blog-writing-pipeline
    cd blog-writing-pipeline
    #to repeat output
    git checkout 00e93b88fbce3788720e8c13a39802209645bffb
    ```

2. Install the required dependencies:

    ```bash
    pip install PyYAML openai rich pypypubsub 
    ```

3. Ensure you have the following directory structure:

    ```plaintext
   auto-reflection/
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
        py_pipeline_name='blog_writer'

        yaml_pprompt_config=join('config','topics.yaml')

        title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
        execute_pipeline(title, py_pipeline_name, yaml_pprompt_config)

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

## Final Output

```plaintext
╭─ Final Blog Titles: ───────────────────────────────────────────────────────────────────────────────────────────────╮
│ 1. Introduction: The Role of Agent Reflection in AI-Powered Blog Writing                                             │
│ 2. Understanding the Benefits of Multi-Agent Collaboration in Content Creation                                       │
│ 3. SEO Optimization and Compliance: How Agent Reflection Enhances Blog Quality                                       │
│ 4. Ethical and Legal Considerations in Automated Content Creation                                                    │
│ 5. Conclusion: The Future of AI-Powered Blogging with Agent Reflection                                               │
╰────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```

## Mocking intermediary agents’ response
If you want to mock/reuse any of the previous agent responses:

1. Copy one of the pipeline logs from log\blog_writer to mock\blog_writer. Mock data will be read from [‘ppl_log’][‘agent_response’]
2. Use copy of you ‘*.py’ pipeline name with mock turned on for chats you want to mock:
```
chats = [
    {
        "agent": writer,
        
        "action": "generate_reply",
        "kwargs": {"task_name": "initial_task"},
        "mock": True,
    },
```
3. Use mocked pipeline. YAML prompt config file is the same,
```
py_pipeline_name='mock_blog_writer'

yaml_pprompt_config=join('config','topics.yaml')

title = "Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI"
#mock config
mock_file=join('mock','blog_writer','blog_writer_topics.json')
assert isfile(mock_file), f"Mock file not found: {mock_file}"
apc.load_mock(mock_file) 

execute_pipeline(title, py_pipeline_name, yaml_pprompt_config) 
```
Now steps you marked as mock=True will draw agent response from mock file:
```
╭─ SEO Reviewer's Response (mocked): ──────────────────────────────────────────────────────────────────────────────────╮
│ I am an SEO reviewer. Here are my suggestions for optimizing the content provided for better search engine rankings  │
│ and organic traffic:                                                                                                 │
│                                                                                                                      │
│ 1. **Keyword Integration**: Ensure that primary keywords such as "AI education," "community initiatives," and        │
│ "DeepLearning.AI" are integrated naturally throughout the headings and body content to boost relevance.              │
│                                                                                                                      │
│ 2. **Headings Structure**: Utilize H2 and H3 tags to create a clear hierarchy in the content, enhancing readability  │
│ and allowing search engines to understand the structure and main topics better.                                      │
│                                                                                                                      │
│ 3. **Meta Descriptions and Alt Text**: Include concise meta descriptions for each blog topic and leverage image alt  │
│ text for accompanying visuals to improve visibility in search results and enhance user engagement.                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```


## License

This project is licensed under the MIT License.


## Full Sample Output
```plaintext
   Writer  system prompt
  "You are a writer tasked with generating a list of 5 potential blog topics/headlines "
  "including 'Introduction' and 'Conclusion' for the blogpost title: "
  f"'Building a Thriving Community: Collaborations and Initiatives at DeepLearning.AI'. Focus on making each headline
  concise, engaging, and reflective of different aspects "
  "of the blog topic. be concise "


   Critic  system prompt
  You are a critic. You review the work of the writer and provide constructive feedback to help improve the quality of
  the content. Do not provide 'Revised Titles Suggestions'.. Do not inclure improved titles into your responce

   SEO Reviewer  system prompt
  You are an SEO reviewer, known for your ability to optimize content for search engines, ensuring that it ranks well
  and attracts organic traffic. Make sure your suggestion is concise (within 3 bullet points), concrete, and to the
  point. Begin the review by stating your role. Do not provide 'Revised Titles Suggestions'. Do not inclure improved
  titles into your responce

   Legal Reviewer  system prompt
  You are a legal reviewer, known for your ability to ensure that content is legally compliant and free from any
  potential legal issues. Make sure your suggestion is concise (within 3 bullet points), concrete, and to the point.
  Begin the review by stating your role.

   Ethics Reviewer  system prompt
  You are an ethics reviewer, known for your ability to ensure that content is ethically sound and free from any
  potential ethical issues. Make sure your suggestion is concise (within 3 bullet points), concrete, and to the point.
  Begin the review by stating your role.

   Meta Summarizer  system prompt
  You are a meta reviewer tasked with aggregating feedback from the SEO, Legal, and Ethics reviewers and providing a
  **final refined list of blog titles** after incorporating all their suggestions.be concise. Do not provide 'Revised
  Titles Suggestions'.


Writer 0
╭─ Writer Response #1: ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 1. Introduction: The Power of Community in AI Development                                                            │
│ 2. Collaborative Projects: Bridging the Gap Between Theory and Practice                                              │
│ 3. Success Stories: Impactful Initiatives from DeepLearning.AI                                                       │
│ 4. Fostering Inclusivity: Engaging Diverse Voices in the AI Community                                                │
│ 5. Conclusion: The Future of AI Collaboration and Community Growth                                                   │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

reflection Critic 2
╭─ Critics Response: ──────────────────────────────────────────────────────────────────────────────────────────────────╮
│ The list of blog titles is a good starting point, but some improvements can enhance clarity and engagement. Here are │
│ a few suggestions:                                                                                                   │
│                                                                                                                      │
│ 1. **Introduction: The Power of Community in AI Development**                                                        │
│    - Consider making the introduction title more inviting. Perhaps specify what readers can expect to gain or learn  │
│ from the introduction, such as "Why Community Matters in AI Development."                                            │
│                                                                                                                      │
│ 2. **Collaborative Projects: Bridging the Gap Between Theory and Practice**                                          │
│    - This title is clear, but it could be more dynamic. You might want to highlight specific benefits or outcomes,   │
│ such as “Collaborative Projects Transforming AI Theory into Real-World Solutions.”                                   │
│                                                                                                                      │
│ 3. **Success Stories: Impactful Initiatives from DeepLearning.AI**                                                   │
│    - While this title communicates the idea, adding an emotional appeal could attract more interest. For example,    │
│ “Success Stories: How DeepLearning.AI Initiatives Are Changing Lives.”                                               │
│                                                                                                                      │
│ 4. **Fostering Inclusivity: Engaging Diverse Voices in the AI Community**                                            │
│    - The current title effectively reflects the content but could benefit from a hint of urgency or relevance.       │
│ Consider “Fostering Inclusivity: The Critical Role of Diverse Voices in the AI Community.”                           │
│                                                                                                                      │
│ 5. **Conclusion: The Future of AI Collaboration and Community Growth**                                               │
│    - Instead of simply stating that it’s a conclusion, you could frame it as a call to action or a teaser of what’s  │
│ next. For instance, “Conclusion: The Next Frontier in AI Collaboration – What Lies Ahead.”                           │
│                                                                                                                      │
│ Overall, focusing on making the titles more engaging while maintaining clarity will likely enhance their             │
│ effectiveness in capturing reader interest.                                                                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Writer 4
╭─ Writer Response #2: ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 1. **Introduction: Why Community Matters in AI Development**                                                         │
│ 2. **Collaborative Projects Transforming AI Theory into Real-World Solutions**                                       │
│ 3. **Success Stories: How DeepLearning.AI Initiatives Are Changing Lives**                                           │
│ 4. **Fostering Inclusivity: The Critical Role of Diverse Voices in the AI Community**                                │
│ 5. **Conclusion: The Next Frontier in AI Collaboration – What Lies Ahead**                                           │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

SEO Reviewer 2
reflection SEO Reviewer 2
╭─ SEO Reviewers Response: ────────────────────────────────────────────────────────────────────────────────────────────╮
│ As an SEO reviewer, here are my suggestions for optimizing the blog topics for better search engine visibility:      │
│                                                                                                                      │
│ 1. **Incorporate Relevant Keywords**: Ensure that each topic includes high-ranking keywords related to AI community, │
│ collaboration, and inclusivity (e.g., "AI development," "AI collaboration success stories," "inclusive AI design").  │
│                                                                                                                      │
│ 2. **Use Engaging Descriptors**: Enhance topic phrases with action verbs or compelling adjectives to capture reader  │
│ interest (e.g., “Innovative Projects Transforming AI” instead of “Collaborative Projects”).                          │
│                                                                                                                      │
│ 3. **Structure for Readability**: Consider using numbered lists or bullet points in the blog for easier skimming and │
│ to improve user engagement, which can lower bounce rates and enhance SEO.                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Legal Reviewer 2
reflection Legal Reviewer 2
╭─ Legal Reviewers Response: ──────────────────────────────────────────────────────────────────────────────────────────╮
│ As a legal reviewer, here are my suggestions for the writer's initial response:                                      │
│                                                                                                                      │
│ 1. **Copyright Considerations**: Ensure that any content referenced in the blog topics (e.g., success stories,       │
│ collaborative projects) does not infringe on third-party copyrights. Obtain permissions or provide proper            │
│ attributions where necessary.                                                                                        │
│                                                                                                                      │
│ 2. **Privacy and Consent**: If discussing individuals or organizations in the success stories or collaborative       │
│ projects, ensure that you have consent to use their names or information, and avoid disclosing sensitive data        │
│ without permission.                                                                                                  │
│                                                                                                                      │
│ 3. **Misleading Information**: Verify all claims made in the blog topics, especially those related to the impact of  │
│ AI initiatives, to avoid potential accusations of misleading or false information.                                   │
│                                                                                                                      │
│ Ensuring these points are addressed will help maintain legal compliance in your writing.                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Ethics Reviewer 2
reflection Ethics Reviewer 2
╭─ Ethics Reviewers Response: ─────────────────────────────────────────────────────────────────────────────────────────╮
│ As an ethics reviewer, I have assessed the writer's initial response regarding the revised blog topics. Here are my  │
│ observations and recommendations:                                                                                    │
│                                                                                                                      │
│ - **Inclusivity and Representation**: Ensure that the mention of "diverse voices" in the topic about inclusivity     │
│ highlights specific groups or communities that have historically been underrepresented in AI. This approach will     │
│ promote awareness and sensitivity towards equity.                                                                    │
│                                                                                                                      │
│ - **Transparency in Success Stories**: When discussing success stories, it is essential to ensure that credit is     │
│ appropriately given to individuals and communities involved. This transparency fosters accountability and ethical    │
│ acknowledgment of contributions.                                                                                     │
│                                                                                                                      │
│ - **Future Implications**: The final topic should also touch on the potential ethical implications and               │
│ responsibilities of AI collaboration. This adds depth and encourages critical thinking about the consequences of AI  │
│ development and the importance of ethical standards in future projects.                                              │
│                                                                                                                      │
│ By addressing these points, the content will not only be engaging but also ethically sound.                          │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

summary Meta Summarizer 8
╭─ Meta Summarizers Response: ─────────────────────────────────────────────────────────────────────────────────────────╮
│ ### Aggregated Feedback Summary:                                                                                     │
│                                                                                                                      │
│ 1. **Keyword Optimization**:                                                                                         │
│    - Incorporate high-ranking, relevant keywords in each title (e.g., "AI development," "collaboration success       │
│ stories," "inclusive AI design") to improve search visibility.                                                       │
│                                                                                                                      │
│ 2. **Engaging Language**:                                                                                            │
│    - Use action verbs and compelling adjectives in titles to increase reader interest (e.g., “Innovative Projects    │
│ Transforming AI”).                                                                                                   │
│                                                                                                                      │
│ 3. **Content Structure**:                                                                                            │
│    - Structure the blog for readability, potentially using numbered lists or bullet points to enhance skimming and   │
│ user engagement.                                                                                                     │
│                                                                                                                      │
│ 4. **Copyright Compliance**:                                                                                         │
│    - Ensure proper attribution for any referenced content such as success stories or projects, and obtain necessary  │
│ permissions to avoid copyright infringement.                                                                         │
│                                                                                                                      │
│ 5. **Privacy and Consent**:                                                                                          │
│    - Verify consent for using names or information about individuals or organizations in the success stories to      │
│ protect privacy.                                                                                                     │
│                                                                                                                      │
│ 6. **Accuracy and Transparency**:                                                                                    │
│    - Ensure all claims made in blog topics are verified and accurate to avoid misleading information, and credit     │
│ contributors ethically.                                                                                              │
│                                                                                                                      │
│ 7. **Focus on Inclusivity**:                                                                                         │
│    - Highlight specific underrepresented groups in discussions about diversity to promote awareness and sensitivity. │
│                                                                                                                      │
│ 8. **Ethical Considerations**:                                                                                       │
│    - Include a discussion on the potential ethical implications and responsibilities in AI collaboration,            │
│ encouraging critical thought on AI’s future impact.                                                                  │
│                                                                                                                      │
│ Incorporating these suggestions will enhance the blog post's SEO value, legal compliance, and ethical integrity      │
│ while maintaining the original content's intent.                                                                     │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

Writer 8
╭─ Writer Response #3: ────────────────────────────────────────────────────────────────────────────────────────────────╮
│ 1. **Introduction: Why Community Matters in AI Development for a Better Tomorrow**                                   │
│ 2. **Innovative Projects Transforming AI Theory into Real-World Solutions**                                          │
│ 3. **Success Stories: Inspiring Ways DeepLearning.AI Initiatives Are Changing Lives**                                │
│ 4. **Fostering Inclusivity: Amplifying Voices of Underrepresented Groups in the AI Community**                       │
│ 5. **Conclusion: The Next Frontier in AI Collaboration – Ethical Responsibilities and Future Prospects**             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
```