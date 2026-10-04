TOPIC_KEYWORDS = {
    "DP": ["dynamic programming", "dp", "memoization", "knapsack"],
    "Trees": ["tree", "binary tree", "bst", "trie"],
    "Graphs": ["graph", "bfs", "dfs", "dijkstra", "shortest path"],
    "Arrays": ["array", "subarray", "two pointer", "sliding window"],
    "SQL": ["sql", "query", "join", "database", "normalization"],
    "System Design": ["system design", "scalability", "load balancer", "microservice"],
    "OOP": ["oop", "object oriented", "inheritance", "polymorphism", "encapsulation"],
    "Behavioral": ["tell me about", "why do you want", "strength", "weakness", "conflict"],
}

def detect_topic(question_text):
    lowered = question_text.lower()

    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in lowered:
                return topic

    return "General"

if __name__ == "__main__":
    print(detect_topic("What is the time complexity of merge sort?"))
    print(detect_topic("Write a query to find the second highest salary"))
    print(detect_topic("Tell me about a time you disagreed with your manager"))
    print(detect_topic("Explain polymorphism with an example"))