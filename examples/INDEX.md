# Example index

30 records. Each file is a full record: request + the human's response (+ the agent's ack when the loop closed).

Illustrative records: project names, numbers, and dates are invented.

| File | kind | category | Response shape | Title |
|---|---|---|---|---|
| [pricing/launch-model.json](pricing/launch-model.json) | decision | `pricing.launch` | option + conditions + standing rule | Launch pricing: paid upfront or subscription? |
| [pricing/reference-price.json](pricing/reference-price.json) | decision | `pricing.paywall-copy` | option only | Show a crossed-out "regular price" on the paywall? |
| [pricing/service-package.json](pricing/service-package.json) | decision | `pricing.service` | change direction | How should the data-audit service be priced? |
| [spend/measurement-budget.json](spend/measurement-budget.json) | decision | `spend.api-budget` | option + conditions | Approve a $240 API budget for the benchmark run? |
| [spend/ads-start.json](spend/ads-start.json) | decision | `spend.ads` | deferred | Start paid search ads this week? |
| [spend/tool-subscription.json](spend/tool-subscription.json) | decision | `spend.saas-subscription` | follow-up question | Pay $12/month for the error-tracking tool? |
| [release/store-submit.json](release/store-submit.json) | decision | `release.app-store-submit` | option only | Submit build 1.2.0 for review now? |
| [release/merge-deploy.json](release/merge-deploy.json) | decision | `release.web-deploy` | option + conditions | Merge and deploy both website changes together? |
| [outreach/public-post.json](outreach/public-post.json) | decision | `outreach.public-post` | follow-up question | Post a "Show HN" under your own name? |
| [outreach/public-claim.json](outreach/public-claim.json) | decision | `outreach.claim-wording` | refuse + standing rule | Can the services page say "we track 700+ sources daily"? |
| [outreach/first-batch.json](outreach/first-batch.json) | decision | `outreach.prospects` | free text | Who should get the first 10 outreach emails? |
| [outreach/creator-deal.json](outreach/creator-deal.json) | decision | `outreach.partnership` | option + conditions | How to pay creators who promote the app? |
| [ops/realign-branch.json](ops/realign-branch.json) | command | `ops.git-realign` | task done (command) | Reset the build server's checkout to origin/main |
| [ops/stop-service.json](ops/stop-service.json) | command | `ops.service-stop` | expired (no answer) | Stop the paused assistant service on the home server |
| [ops/authorize-scheduled-agent.json](ops/authorize-scheduled-agent.json) | decision | `security.scheduled-agent` | option only | Allow a weekly review agent to run on the home server? |
| [ops/alert-false-positive.json](ops/alert-false-positive.json) | decision | `ops.alerting` | not mine to decide | Fix the network alert that fires on "file not found" errors? |
| [review/research-report.json](review/research-report.json) | review | `review.research-report` | free text review | Review the competitor scan before it goes into the plan |
| [review/onboarding-diff.json](review/onboarding-diff.json) | decision | `product.onboarding` | option + conditions | Ship the shorter onboarding (3 screens instead of 5)? |
| [data/health-import.json](data/health-import.json) | decision | `data.import` | option + conditions | How should sleep and step data get into the weekly report? |
| [data/purge-raw-logs.json](data/purge-raw-logs.json) | decision | `data.purge-old-logs` | revoked | Delete raw request logs older than 90 days? |
| [legal/terms-template.json](legal/terms-template.json) | decision | `legal.terms-template` | not mine to decide | Which terms of use: the store's standard terms or our own? |
| [legal/contract-entity.json](legal/contract-entity.json) | decision | `legal.contract-entity` | follow-up question | Sign the first service contract as an individual or as the company? |
| [deps/minor-upgrade-rule.json](deps/minor-upgrade-rule.json) | decision | `deps.minor-upgrade` | decided by rule | Upgrade the charting library 4.2.1 → 4.3.0? |
| [deps/expiry-proceed.json](deps/expiry-proceed.json) | decision | `deps.patch-upgrade` | decided by expiry | Apply the static-site generator patch 2.8.3 → 2.8.4? |
| [brief/protocol-explainer.json](brief/protocol-explainer.json) | brief | `brief.concept` | read | Who runs an MCP server, and where? |
| [brief/weekly-digest.json](brief/weekly-digest.json) | brief | `brief.weekly` | question after reading | Week 41 in one screen |
| [access/console-record.json](access/console-record.json) | task | `access.console-login` | task done | Create the app record in the store console |
| [product/paywall-fallback.json](product/paywall-fallback.json) | decision | `product.paywall` | free text | What do users get after closing the out-of-credits paywall? |
| [product/scope-withdrawn.json](product/scope-withdrawn.json) | decision | `product.scope-cut` | withdrawn by agent | Cut the calendar sync from 1.3 to hit the date? |
| [research/go-no-go.json](research/go-no-go.json) | decision | `research.go-no-go` | option + conditions | Build version 1 now, or freeze and run cheap experiments first? |
