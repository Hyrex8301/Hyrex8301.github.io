Plain HTML and CSS only: no build step, no framework, no JavaScript unless I ask.
Keep index.html at the repo root, and use relative paths (style.css, never /style.css).
Ask before adding a dependency, a script tag, or a new file type.
Do not edit DECISIONS.md or anything in verification/; those are mine to write.
Never commit API keys, secrets, or personal information, and never add Claude or any AI as a commit co-author or contributor: no Co-Authored-By trailers, no AI mentions in commit messages, the README, or the history.

Coding practices:
- Keep main working at all times. Do not commit new features straight to main.
- For each new piece of work, create a branch off main first (git checkout main, git pull, git checkout -b short-feature-name), build there, then merge back to main once it works and open a pull request if I ask.
- Write small, focused commits with a message that says what changed and why.
- Document as you go: comment any non-obvious CSS or HTML, keep README.md current when behavior or structure changes, and record design choices in DECISIONS.md (I write that file, so tell me what to add).
- Before merging to main, check that index.html still opens correctly and links and styles work.
