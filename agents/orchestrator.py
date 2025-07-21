import json
import pandas as pd
from datetime import datetime

from prompts.system.generate_prompt import build_filter_generator_prompt
from logic.llm_client import call_openai_with_functions
from functions.function_specs import function_specs
from logic.filter_dataframe import apply_filter

def load_query_examples(path="prompts/examples/query_examples.json"):
    with open(path, "r") as f:
        return json.load(f)
    
def orchestrate_filtering(user_query, full_df):
    system_prompt = build_filter_generator_prompt()

    # 2. Load few-shot examples
    examples = load_query_examples()

    # 3. Construct messages
    messages = [{"role": "system", "content": system_prompt}]
    for ex in examples:
        messages.append({"role": "user", "content": ex["user"]})
        messages.append({
            "role": "assistant",
            "content": None,
            "function_call": {
                "name": ex["function_call"]["name"],
                "arguments": json.dumps(ex["function_call"]["arguments"])  # ✅ convert to JSON string
            }
        })
    messages.append({"role": "user", "content": user_query})

    # 4. Call OpenAI with function schema
    response = call_openai_with_functions(
        function_specs=function_specs,
        messages=messages
    )

    # 5. Parse function call arguments
    try:
        tool_call = response.choices[0].message.tool_calls[0]
        if tool_call.function.name != "filter_dataframe":
            raise ValueError("Unexpected function call returned")

        tool_args = json.loads(tool_call.function.arguments)
    except Exception as e:
        raise RuntimeError(f"Failed to extract tool arguments: {e}")

    # 6. Apply filters
    filtered_df = apply_filter(full_df, tool_args)
    return tool_args, filtered_df