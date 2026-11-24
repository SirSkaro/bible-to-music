# Set up PyCharm and Codex

Use PyCharm as the workbench for editing, debugging, and running tests. Use Codex in the same project to implement small changes against the checked-in guidance. The model you use to develop the application and the models the application auditions are independent choices.

## Open the project

1. Extract the bundle. Open the `bible-music` folder containing `AGENTS.md` and `README.md` as the PyCharm project. If you already have a repository, copy the contents into its root. For a new repository, use **VCS → Enable Version Control Integration → Git**, or run `git init` in that folder.
2. Give the project a local `.venv`. My suggested starting interpreter is Python 3.12. Check compatibility when choosing your first local audio model. In PyCharm, open the interpreter selector, choose **Add Interpreter → Add Local Interpreter**, and create a **Virtualenv** in `.venv`. If you use `uv`, `uv venv --python 3.12` from the root creates it. In PyCharm’s existing-interpreter picker, select `.venv/bin/python` on macOS or Linux, or `.venv\Scripts\python.exe` on Windows. Both routes give the IDE and the terminal the same interpreter once the terminal uses that environment. [PyCharm interpreters](https://www.jetbrains.com/help/pycharm/configuring-python-interpreter.html) · [uv environments](https://docs.astral.sh/uv/pip/environments/)
3. In **Settings → Plugins → Marketplace**, install **AI Assistant**. Open **AI Chat**, select **Codex**, choose **Install and Continue** if prompted, then select **ChatGPT** and sign in with the account you use for Codex. JetBrains also offers device-code sign-in. The provider-account option works independently of a JetBrains AI subscription. [Plugin installation](https://www.jetbrains.com/help/ai-assistant/installation-guide-ai-assistant.html) · [Agent activation](https://www.jetbrains.com/help/ai-assistant/activate-agents.html)

If you prefer a terminal session, install the Codex CLI, open PyCharm’s terminal at the project root, and run `codex`. Both routes work against the files in that checkout. [Codex CLI](https://developers.openai.com/codex/cli/)

## Locate the applicable engineering decisions

Start a fresh project chat and send the following. **Plan** mode is useful for this first exchange. [Codex in JetBrains](https://www.jetbrains.com/help/ai-assistant/codex-agent.html)

> Read the root AGENTS.md and follow its links for take review. Which instructions apply to an experiment? Explain where the expected lyrics enter the workflow, what a replay fixture proves, and which decisions the producer can delegate. Cite repository paths. This is a read-only orientation.

A grounded answer places the expected text in the comparison step, identifies the experiment guidance, and distinguishes producer choices from provider settings. Codex discovers project instructions along the path from the repository root to its working directory when a session starts. For a task that starts at the root, the explicit link in `AGENTS.md` also directs the agent to the nested experiment rules. Start a fresh session after revising standing instructions. [Codex instruction discovery](https://developers.openai.com/codex/guides/agents-md/)

## Give Codex its first implementation task

The [skill selection](skills.md) gives the coding agent its starting tools. This prompt is the first implementation task in the producer’s checkout.

> Implement the smallest offline take-review use case. Given an arrangement and a replayed, timestamped listener observation, flag one omitted word and return the phrase window a producer should audition. Drive the use case through a public entry point. Show a passing case for an authorized repeat. Use synthetic lyrics for the fixtures. Set up only the packaging and tests this slice needs, run them, and record the exact verification command in this README. Live providers and UI work belong to later tasks.

My starting tooling choice would be `uv` for dependency management and `pytest` for the acceptance examples. Once that first change creates a project and a lockfile, commit the lockfile. Point PyCharm’s test runner at the same `.venv`. Open a test in the debugger, run it from the gutter, and run the documented command in the terminal. Those two runs should exercise the same behavior. [uv project workflow](https://docs.astral.sh/uv/guides/projects/) · [PyCharm pytest support](https://www.jetbrains.com/help/pycharm/pytest.html)

## When you reach the review screen

PySide6 is the selected desktop driving adapter. A concrete UI experiment is to click a lyric finding and hear the surrounding phrase. Qt’s `QMediaPlayer` exposes playback position in milliseconds and can seek when the media supports it. A playback prototype using one local WAV can validate that interaction before you commit to a full GUI. [Qt media player](https://doc.qt.io/qtforpython-6/PySide6/QtMultimedia/QMediaPlayer.html)

## Next offline slice

> Implement the song-boundary preview through the application API. Use the [boundary cases](../examples/boundary-cases.json) and the conflict policy in [ADR 0004](../decisions/0004-song-passages-and-creative-authority.md). Drive manual, pinned and artist-proposed cuts through the same validator. Return the legal positions, derived passages and actionable conflicts. Verify the selected ending of the final song. Run the acceptance cases without a model, provider credential or audio file.
