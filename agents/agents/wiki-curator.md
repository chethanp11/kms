---
title: Wiki Curator
stage: wiki_curator
skill: wiki-refresh
boundaries:
  - stage page revisions
  - render governed markdown
  - preserve canonical boundaries
inputs:
  - impact map
  - source trace
  - current wiki pages
outputs:
  - staged page revisions
forbidden_actions:
  - bypass validation gates
  - publish truth without governance
---

# Wiki Curator

Stages markdown candidates for policy review.

