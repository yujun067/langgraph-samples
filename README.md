# langgraph-samples

A curated collection of practical notebooks, guides, and code samples for building advanced LLM (Large Language Model) applications using the LangChain and LangGraph ecosystems.

## Project Overview

This repository demonstrates how to leverage the modular, composable frameworks of [LangChain](https://github.com/langchain-ai/langchain) and [LangGraph](https://github.com/langchain-ai/langgraph) to build production-ready AI agents, chatbots, RAG (Retrieval-Augmented Generation) systems, and more. It includes hands-on examples, best practices, and real-world use cases, with a focus on both foundational concepts and advanced workflows.

## Directory Structure

- **langchain/**: Modular examples covering core concepts, memory, model I/O, data connections, and classic agent/chain patterns.
- **langgraph/**: Tutorials and advanced guides for building agent graphs, multi-agent collaboration, reflection/reflexion agents, and chatbots using LangGraph.
- **langchain-usecase/**: Real-world use cases, e.g., a sales chatbot for real estate.
- **langchian-models/**: Model-specific demos, e.g., ChatGLM integration.
- **openai_api-2024/**: Quickstart guides and notebooks for using the OpenAI API, including embeddings, TTS, assistants, and more.
- **langchain_lcel_intro.md**: Beginner-friendly introduction to LangChain and LCEL (LangChain Expression Language).

## Key Features

- **LangChain Core**: Learn about prompt templates, LLM chains, output parsers, memory, and RAG patterns.
- **LCEL (LangChain Expression Language)**: Unified, composable interface for building and chaining LLM components.
- **LangGraph**: High-level framework for building complex, stateful agent workflows as graphs, supporting multi-agent collaboration, reflection, and tool integration.
- **LangSmith**: Tools for debugging, monitoring, and evaluating LLM applications.
- **OpenAI API Demos**: End-to-end guides for using OpenAI's latest models and features.

## Example Notebooks

- **Chatbot with LangGraph**: Step-by-step guide to building a multi-turn, tool-augmented chatbot with memory and human-in-the-loop capabilities.
- **Multi-Agent Collaboration**: Implementing workflows where multiple specialized agents collaborate to solve complex tasks.
- **Reflection/Reflexion Agents**: Agents that iteratively improve their outputs via self-critique and feedback loops.
- **SQL Agent**: Querying and reasoning over SQL databases using LLMs and LangGraph.
- **Sales Chatbot Use Case**: Real estate sales assistant using RAG and custom data.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone <this-repo-url>
   cd langgraph-samples
   ```

2. **Install dependencies:**
   Most notebooks specify their own requirements. For general exploration:
   ```bash
   pip install langchain langgraph openai jupyterlab
   ```

3. **Set up API keys:**
   - For OpenAI: `export OPENAI_API_KEY='your-api-key'`
   - For Anthropic, LangSmith, etc., see individual notebook instructions.

4. **Launch Jupyter Lab:**
   ```bash
   jupyter lab
   ```
   Open any notebook of interest and follow the instructions inside.

## References

- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [LangSmith Platform](https://smith.langchain.com/)

## License

This project is for educational purposes. Please check individual files and notebooks for additional licensing or usage notes.
