#!/usr/bin/env python
import sys
from crew import NewsletterAgentsCrew


# This main file is intended to be a way for your to run your
# crew locally, so refrain from adding necessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def run():
    """
    Run the crew.
    """

    return NewsletterAgentsCrew().crew().kickoff()

if __name__ == "__main__":



    print("## Welcome to Crew AI Template")
    print("-------------------------------")

    result = run()
    print("\n\n########################")
    print("## Here is you custom crew run result:")
    print("########################\n")
    print(result)
