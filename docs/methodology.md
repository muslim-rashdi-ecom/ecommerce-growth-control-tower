# Methodology

## Campaign metrics

The pipeline aggregates rows by platform and campaign. CTR is `link_clicks / impressions`. CPC is `spend / link_clicks`. ROAS is `revenue / spend` when the sample contains revenue.

## Funnel rates

The control tower keeps the stage order explicit: landing-page views, view item, add to cart, begin checkout, and purchases. A stage rate is the current stage divided by the immediately preceding stage. The result is a diagnostic signal, not a causal explanation.

## Reconciliation

Platform and site counts are compared as a diagnostic. A discrepancy of at least 15% is flagged for investigation. The threshold is not a universal standard; it is a visible demo guardrail that can be changed per business and attribution window.

## Fatigue

Creative fatigue compares the first and last observed daily CTR for each creative. A decline of at least one percentage point is marked `watch`. Production analysis should use a longer time window and minimum-delivery thresholds.

## Recommendations

Recommendations are deterministic and explainable. They are prompts for the next investigation, not autonomous budget changes.
