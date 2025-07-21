import json
import pandas as pd
from datetime import datetime

def build_filter_generator_prompt():
    # Load template
    with open("prompts/system/filter_generator_template.txt", encoding="utf-8") as f:
        template = f.read()

    # Load safe globals
    with open("system_info/safe_globals.json", encoding="utf-8") as f:
        safe_globals = json.load(f)["safe_builtins"]
    safe_globals_str = ", ".join(sorted(safe_globals))

    # Load sample data
    sample_df = pd.read_csv("data/processed/asset_metrics.csv").head(5)
    asset_metrics_sample = sample_df.to_string(index=False)

    # Load internal assets
    internal_assets = pd.read_csv("data/processed/internal_props.csv")["property_name"].tolist()
    internal_assets_str = ", ".join(internal_assets)

    # Load valid markets
    market_names = pd.read_csv("data/processed/market_names.csv")["market"].dropna().unique().tolist()
    market_names_str = ", ".join(market_names)

    # Replace placeholders
    prompt = (
        template
        .replace("{{today}}", datetime.today().strftime("%Y-%m-%d"))
        .replace("{{safe_globals}}", safe_globals_str)
        .replace("{{asset_metrics_sample}}", asset_metrics_sample)
        .replace("{{internal_assets}}", internal_assets_str)
        .replace("{{market_names}}", market_names_str)
    )

    return prompt
