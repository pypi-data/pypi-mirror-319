from hyperpocket.tool import from_git

SLACK = [
    from_git("https://github.com/vessl-ai/tool-calling", "main", "examples/slack-get-message"),
    from_git("https://github.com/vessl-ai/tool-calling", "main", "examples/slack-post-message")
]

LINEAR = [
    from_git("https://github.com/vessl-ai/tool-calling", "main", "examples/linear-get-issues"),
]
