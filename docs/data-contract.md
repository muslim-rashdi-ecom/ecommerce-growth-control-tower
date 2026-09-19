# Data contract

`campaign_daily.csv` represents one daily observation for a platform/campaign/ad-set/creative combination. Counts are sanitized integers; `spend` and `revenue` use the same currency within the sample.

`reconciliation.csv` compares an attributed platform count with a site-side count for the same event label and date. The `scope` column must describe the comparison boundary.

Production ingestion should additionally standardize timezone, currency, refunds, attribution window, consent state, event deduplication, and data freshness.
