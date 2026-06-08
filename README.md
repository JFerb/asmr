# ASMR

Personal workspace for the ASMR course. Course tutorial material lives in `tutorial/` as a [git subtree](https://git-scm.com/book/en/v2/Git-Tools-Subtree-Merging); own code belongs elsewhere in this repo.

## Tutorial subtree

| | |
|---|---|
| Remote | `tutorial` |
| Upstream | https://zivgitlab.uni-muenster.de/ai-systems/teaching/public/26-ss/asmr/tutorial |
| Branch | `main` |
| Path | `tutorial/` |

Treat `tutorial/` as read-only reference. Start with [`tutorial/README.md`](tutorial/README.md) and [`tutorial/setup/README.md`](tutorial/setup/README.md).

### Pull upstream updates

```bash
git fetch tutorial
git subtree pull --prefix=tutorial tutorial main --squash
```
