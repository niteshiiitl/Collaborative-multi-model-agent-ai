"""CLI entry point for the multi-agent system."""
import argparse
from orchestrator import Orchestrator


def main():
    parser = argparse.ArgumentParser(description="Multi-Agent System CLI")
    parser.add_argument("task", type=str, help="Task description")
    parser.add_argument("--llm", type=str, default="gemini", choices=["gemini", "groq", "openai"])
    parser.add_argument("--source", type=str, help="Video URL or file path")
    parser.add_argument("--csv", type=str, help="CSV file path for data analysis")
    args = parser.parse_args()

    kwargs = {}
    if args.source:
        kwargs["source"] = args.source
    if args.csv:
        kwargs["csv_path"] = args.csv

    orchestrator = Orchestrator(llm_provider=args.llm)
    print(f"\n🤖 Processing: {args.task}\n")

    results = orchestrator.run(args.task, **kwargs)
    for result in results:
        print(f"\n✅ {result['agent']}: {result['message']}")
        if result.get("file_path"):
            print(f"   📁 File: {result['file_path']}")


if __name__ == "__main__":
    main()
