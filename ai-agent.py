#!/usr/bin/env python3
"""
AI Agent for EKS Operations — Fitness Tracker Capstone
Uses Groq API (free) to provide intelligent Kubernetes troubleshooting assistance.
"""

import os
import subprocess
from groq import Groq

GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE")

client = Groq(api_key=GROQ_API_KEY)

SYSTEM_PROMPT = """You are a senior DevOps engineer and SRE specialist with deep expertise in:
- Amazon EKS and Kubernetes
- Docker containers
- Helm charts
- ArgoCD GitOps
- CI/CD pipelines
- Datadog monitoring

When asked about issues, you:
1. Diagnose the problem clearly
2. Provide exact kubectl/shell commands to investigate
3. Provide exact kubectl/shell commands to fix it
4. Explain what caused the issue
5. Suggest how to prevent it

Always provide copy-paste ready commands. Be concise but thorough.
Current app: Fitness Tracker Node.js + MongoDB on EKS cluster named capstone-cluster."""


def get_cluster_context():
    """Get current cluster state for context."""
    try:
        pods = subprocess.run(
            ["kubectl", "get", "pods", "-n", "fitness-tracker", "--no-headers"],
            capture_output=True, text=True, timeout=10
        )
        return pods.stdout if pods.returncode == 0 else "Could not reach cluster"
    except Exception:
        return "kubectl not available"


def chat_with_agent(question, history):
    """Send question to AI Agent and get response."""
    cluster_info = get_cluster_context()

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Current cluster pods:\n{cluster_info}\n\nQuestion: {question}"}
    ] + history

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.3,
        max_tokens=1024
    )
    return response.choices[0].message.content


def main():
    print("=" * 60)
    print("  🤖 AI Agent for EKS Operations — Fitness Tracker")
    print("=" * 60)
    print("Ask any Kubernetes/DevOps question. Type 'exit' to quit.\n")

    history = []

    while True:
        try:
            question = input("You > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting AI Agent.")
            break

        if not question:
            continue
        if question.lower() in ("exit", "quit", "q"):
            print("Goodbye!")
            break

        print("\n🔍 Analyzing...\n")
        try:
            answer = chat_with_agent(question, history)
            print(f"Agent > {answer}\n")
            print("-" * 60)

            # Add to history for context
            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": answer})

            # Keep history to last 6 exchanges
            if len(history) > 12:
                history = history[-12:]

        except Exception as e:
            print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
