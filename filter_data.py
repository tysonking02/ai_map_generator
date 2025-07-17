import pandas as pd
from request_response import request_response
import re
import json
import streamlit as st
import math

with open("system_info/safe_globals.json", encoding="utf-8") as f:
    config = json.load(f)

safe_globals = {
    "__builtins__": {name: __builtins__[name] for name in config["safe_builtins"]},
    "math": math,
}
for fn in config.get("math_functions", []):
    safe_globals[fn] = getattr(math, fn)

with open("system_info/haversine.txt", encoding="utf-8") as f:
    haversine_text = f.read()
haversine_ns = {}
exec(haversine_text, safe_globals, haversine_ns)
haversine = haversine_ns["haversine"]
safe_globals["haversine"] = haversine

def filter_data(asset_metrics, query):
    response = request_response(query)

    match = re.search(r"```(?:python)?\n([\s\S]*?)\n```", response)
    code_to_exec = match.group(1) if match else response

    ns = safe_globals.copy()
    ns["asset_metrics"] = asset_metrics
    ns["haversine"] = haversine

    exec(code_to_exec, ns)

    filtered_asset_metrics = ns.get("filtered_asset_metrics")
    return code_to_exec, filtered_asset_metrics
