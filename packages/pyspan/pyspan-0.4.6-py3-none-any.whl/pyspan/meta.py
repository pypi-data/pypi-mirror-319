import pandas as pd
import numpy as np
import json
import re
from io import StringIO
from typing import Union, Dict, Any, Tuple, Optional
from openai import OpenAI
from openai import APIError, RateLimitError
import time
import sys
# Import individual modules directly to avoid circular imports
from .logging_utils import log_function_call
from .state_management import track_changes
from .handle_nulls import handle_nulls
from .remove import remove
from .refine import refine
from .manual_rename_columns import manual_rename_columns
from .format_dt import format_dt
from .split_column import split_column
from .detect_errors import detect_errors
from .convert_type import convert_type
from .detect_outliers import detect_outliers
from .remove_chars import remove_chars
from .reformat import reformat
from .scale_data import scale_data
from .sample_data import sample_data
from .convert_unit import convert_unit
from .state_management import undo
from .logging_utils import display_logs

class MetaError(Exception):
    """Custom exception for meta function errors"""
    pass

def validate_data(data: Any) -> Tuple[bool, str]:
    """Validate input data type"""
    if data is None:
        return False, "Data cannot be None"
    
    valid_types = (pd.DataFrame, pd.Series, list, dict, tuple, np.ndarray, str)
    if not isinstance(data, valid_types):
        return False, f"Unsupported data type. Must be one of: {', '.join([t.__name__ for t in valid_types])}"
    
    return True, ""

def validate_prompt(prompt: str) -> Tuple[bool, str]:
    """Validate user prompt"""
    if not prompt or not isinstance(prompt, str):
        return False, "Prompt must be a non-empty string"
    if len(prompt) > 1000:  # Arbitrary limit, adjust as needed
        return False, "Prompt exceeds maximum length (1000 characters)"
    return True, ""

def get_cleaning_plan(prompt: str, api_key: str,df: pd.DataFrame, max_retries: int = 3, retry_delay: float = 1.0) -> Dict:
    """Get cleaning plan from OpenAI with retry logic"""
    client = OpenAI(api_key=api_key)
    
    system_message = """You are an expert data scientist using the pyspan library to clean and preprocess data.Your task is to analyze the user's requirements and create a cleaning plan using pyspan's functions.Think like a human data scientist - understand the data issues and choose the most appropriate functions and parameters.
    Return a JSON object with a 'steps' array, where each step has:
    - function: the name of the pyspan function to call (must be exactly as listed below)
    - description: a brief description of what this step will do
    - args: a dictionary of arguments to pass to the function (use exact column names from the DataFrame)
    
    Available functions and their parameters:
    1. handle_nulls(df, columns=None, action='remove', with_val=None, by=None, inplace=False, threshold=None, axis='rows')
       - df: DataFrame, List, dict, tuple, ndarray, or str
       - columns: str or List[str], column names to process
       - action: 'remove' (drop rows), 'replace' (with custom value), or 'impute' (using strategy)
       - with_val: value to replace nulls with (for action='replace')
       - by: 'mean', 'median', 'mode', 'interpolate', 'forward_fill', 'backward_fill'
       - threshold: 0-100 percentage for dropping rows/columns with nulls
       - axis: 'rows' or 'columns' for threshold application
Always set inplace=False to get the modified data back
    2. remove(df, operation, columns=None, keep='first', consider_all=True, inplace=False)
       - df: DataFrame, List, dict, tuple, ndarray, or str
       - operation: 'duplicates' or 'columns'
       - columns: str or List[str], for duplicates check or columns to remove
       - keep: 'first', 'last', 'none' (for duplicates)
       - consider_all: bool, check all columns for duplicates
       - inplace: bool, modify in place

    3. refine(df, clean_rows=True)
       - df: DataFrame, List, dict, tuple, ndarray, or str
       - clean_rows: bool, clean row content by removing special chars

    4. manual_rename_columns(df, rename_dict)
       - df: DataFrame, List, dict, tuple, ndarray, or str
       - rename_dict: dict, mapping of old_name: new_name

    5. format_dt(df, columns, day=False, month=False, year=False, quarter=False, hour=False, minute=False,
                day_of_week=False, date_format="%Y-%m-%d", time_format="%H:%M:%S", from_timezone=None, to_timezone=None)
       - df: DataFrame, List, dict, tuple, ndarray, or str
       - columns: str, datetime column name
       - day/month/year/quarter/hour/minute/day_of_week: bool, features to add
       - date_format/time_format: str, format strings
       - from_timezone/to_timezone: str, timezone conversion

    6. split_column(df, column, delimiter=None)
       - df: DataFrame, List, dict, tuple, ndarray, or str
       - column: str, column to split
       - delimiter: str, separator character

    7. detect_errors(df, date_columns=None, numeric_columns=None, text_columns=None, date_format='%Y-%m-%d')
       - df: DataFrame, List, dict, tuple, ndarray, or str
       - date_columns: List[str], columns to check dates
       - numeric_columns: List[str], columns to check numbers
       - text_columns: List[str], columns for spell check
       - date_format: str, expected date format

    8. convert_type(df, columns=None)
       - df: DataFrame/Series, List, dict, tuple, ndarray, or str
       - columns: List[str], columns to convert

    9. detect_outliers(df, method='iqr', threshold=1.5, columns=None, handle_missing=True,
                      anomaly_method=None, contamination=0.05, n_neighbors=20, eps=0.5, min_samples=5)
       - df: DataFrame/Series, List, dict, tuple, ndarray, or str
       - method: 'iqr', 'z-score'
       - threshold: float, outlier detection threshold
       - columns: List[str], columns to check
       - handle_missing: bool, drop missing values
       - anomaly_method: 'isolation_forest', 'lof', 'dbscan'
       - contamination: float, proportion of outliers
       - n_neighbors: int, for LOF
       - eps/min_samples: float/int, for DBSCAN

    10. remove_chars(df, columns=None, strip_all=False, custom_characters=None)
        - df: DataFrame/Series, List, dict, tuple, or str
        - columns: List[str], columns to clean
        - strip_all: bool, remove all extra spaces
        - custom_characters: str, specific chars to remove

    11. reformat(df, target_column, reference_column)
        - df: DataFrame, List, dict, tuple, ndarray, or str
        - target_column: str, column to format
        - reference_column: str, column to copy format from

    12. scale_data(df, method='minmax', columns=None)
        - df: DataFrame, List, dict, tuple, ndarray, or str
        - method: 'minmax', 'robust', 'standard'
        - columns: List[str], columns to scale

    13. convert_unit(df, columns, unit_category, from_unit, to_unit)
        - df: DataFrame, List, dict, tuple, ndarray, or str
        - columns: List[str], columns to convert
        - unit_category: 'length', 'mass', 'time', 'volume', 'temperature', 'speed', 'energy', 'area', 'pressure'
        - from_unit/to_unit: str, source/target units
    14. sample_data()
    15. display_logs()
    16. undo()
    
    IMPORTANT:
    - Use exact column names from the DataFrame
    - The 'df' parameter will be added automatically, do not include it in args
    - Function names must match exactly as listed above
    1. Analyze the user's requirements carefully
    2. Choose functions and parameters based on:
       - The specific data issues mentioned
       - The type of data in each column
       - The user's cleaning preferences
    3. Order the steps logically
    4. Use default parameters when appropriate, but customize when needed(you have all functions parameters and you know all para values)
    5. Consider data quality and preservation
    6. Think about efficiency and effectiveness
    7. You can use multiple functions together for complex cleaning tasks
    8. You can use the same function multiple times with different parameters if needed

    Example thought process:
    1. What are the main data issues?
    2. Which columns need special handling?
    3. What's the most efficient order of operations?
    4. Are there any dependencies between steps?
    5. What parameters would work best for this specific case?
    6. How can we preserve data quality while cleaning?
    """
    
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-2024-05-13",
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"DataFrame columns: {df.columns.tolist()}\n\nTask: {prompt}"}
                ],
                temperature=0.7,
                max_tokens=2000,
                response_format={"type": "json_object"}
            )
            
            try:
                cleaning_plan = json.loads(response.choices[0].message.content)
                if not isinstance(cleaning_plan, dict) or "steps" not in cleaning_plan:
                    raise MetaError("Invalid cleaning plan format")
                return cleaning_plan
            except json.JSONDecodeError:
                raise MetaError("Failed to parse cleaning plan")
                
        except RateLimitError:
            if attempt == max_retries - 1:
                raise MetaError("OpenAI API rate limit exceeded")
            time.sleep(retry_delay * (attempt + 1))
            
        except APIError as e:
            if attempt == max_retries - 1:
                raise MetaError(f"OpenAI API error: {str(e)}")
            time.sleep(retry_delay)
            
        except Exception as e:
            raise MetaError(f"Unexpected error getting cleaning plan: {str(e)}")

def format_summary(summary: Dict) -> str:
    """Format the summary in a human-readable way"""
    output = []
    
    # Add cleaned data section first
    if "cleaned_data" in summary:
        output.append("\n✨ Cleaned Data:")
        output.append(str(summary["cleaned_data"]))
    
    # Add successful operations
    successful_steps = [s for s in summary["steps_performed"] if s["status"] == "success"]
    if successful_steps:
        output.append("\n✅ Successful Operations:")
        for step in successful_steps:
            output.append(f"- {step['description']}")
    
    # Add failed operations
    failed_steps = [s for s in summary["steps_performed"] if s["status"] == "failed"]
    if failed_steps:
        output.append("\n❌ Failed Operations:")
        for step in failed_steps:
            output.append(f"- {step['description']}")
            output.append(f"  Error: {step['error']}")
    
    # Add data quality report if exists
    if "error_report" in summary and not summary["error_report"].empty:
        output.append("\n🔍 Data Quality Report:")
        output.append(summary["error_report"].to_string())
    
    # Add warnings
    if summary["warnings"]:
        output.append("\n⚠️ Warnings:")
        for warning in summary["warnings"]:
            output.append(f"- {warning}")
    
    # Add insights
    if summary["insights"]:
        output.append("\n💡 Insights:")
        for insight in summary["insights"]:
            output.append(f"- {insight}")
    
    # Add statistics
    stats = summary["final_stats"]
    output.append("\n📊 Statistics:")
    output.append(f"- Total steps attempted: {stats['total_steps']}")
    output.append(f"- Successful steps: {stats['successful_steps']}")
    output.append(f"- Failed steps: {stats['failed_steps']}")
    
    return "\n".join(output)

@log_function_call
@track_changes
def meta(
    data: Union[pd.DataFrame, pd.Series, list, dict, tuple, np.ndarray, str],
    openai_api_key: str,
    prompt: str,
    max_retries: int = 3
) -> str:
    """
    Clean data based on natural language prompt using OpenAI API.
    
    Args:
        data: Input data in various formats (DataFrame, Series, list, dict, tuple, ndarray, str)
        openai_api_key: OpenAI API key
        prompt: Natural language description of cleaning tasks
        max_retries: Maximum number of API call retries
        
    Returns:
        str: Formatted report including cleaned data and execution summary
    """
    # Initialize variables
    df = None
    original_type = type(data)
    cleaned_data = data  # Default to original data in case of early failure
    
    # Initialize summary
    summary = {
        "steps_performed": [],
        "insights": [],
        "errors": [],
        "warnings": [],
        "state_history": []  # Track DataFrame states for rollback
    }
    
    try:
        # Validate inputs
        valid_data, data_error = validate_data(data)
        if not valid_data:
            raise MetaError(f"Invalid data: {data_error}")
            
        valid_prompt, prompt_error = validate_prompt(prompt)
        if not valid_prompt:
            raise MetaError(f"Invalid prompt: {prompt_error}")
        
        # Store original type for later conversion
        original_type = type(data)
        
        # Convert to DataFrame if necessary
        df = convert_to_dataframe(data)
        if df is None:
            raise MetaError("Failed to create DataFrame from input data")
        
        # Save initial state
        summary["state_history"].append(df.copy())
        
        # Get cleaning plan from OpenAI
        cleaning_plan = get_cleaning_plan(prompt, openai_api_key, df, max_retries)
        
        # Map function names to actual functions
        function_map = {
            'remove_chars': remove_chars,
            'convert_type': convert_type,
            'detect_errors': detect_errors,
            'handle_nulls': handle_nulls,
            'format_dt': format_dt,
            'split_column': split_column,
            'detect_outliers': detect_outliers,
            'reformat': reformat,
            'scale_data': scale_data,
            'convert_unit': convert_unit,
            'remove': remove,
            'refine': refine,
            'manual_rename_columns': manual_rename_columns,
            'sample_data': sample_data,
            'display_logs': display_logs,
            'undo': undo
        }
        
        # Execute each step in the plan sequentially
        current_data = df
        for step in cleaning_plan.get("steps", []):
            try:
                function_name = step["function"]
                description = step["description"]
                args = step.get("args", {}).copy()
                
                # Get the function from the map
                func = function_map.get(function_name)
                if func is None:
                    raise MetaError(f"Unknown function: {function_name}")
                
                # Add the current data as the first argument
                if function_name not in ['sample_data', 'display_logs', 'undo']:
                    args["df"] = current_data
                
                # Execute the function with exact arguments from OpenAI
                result = func(**args)
                
                # Update current_data for next function if result is not None
                if result is not None:
                    if function_name == 'detect_errors':
                        summary["error_report"] = result
                    else:
                        current_data = result
                        summary["state_history"].append(current_data.copy())
                
                # Add to summary
                summary["steps_performed"].append({
                    "function": function_name,
                    "description": description,
                    "arguments": args,
                    "status": "success"
                })
                
                # Add insights based on the function result
                add_function_insights(summary, function_name, args, current_data, data)
                
            except Exception as e:
                error_msg = str(e)
                summary["errors"].append(f"Error in {function_name}: {error_msg}")
                summary["steps_performed"].append({
                    "function": function_name,
                    "description": description,
                    "arguments": args,
                    "status": "failed",
                    "error": error_msg
                })
                continue
        
        # Update final cleaned data
        df = current_data

    except Exception as e:
        summary["errors"].append(f"Error executing cleaning plan: {str(e)}")

    # Convert back to original type
    try:
        cleaned_data = convert_from_dataframe(df, original_type) if df is not None else data
        summary["cleaned_data"] = cleaned_data
    except Exception as e:
        summary["errors"].append(f"Error converting back to original type: {str(e)}")
        cleaned_data = data

    # Add final statistics
    summary["final_stats"] = {
        "total_steps": len(cleaning_plan["steps"]) if "cleaning_plan" in locals() else 0,
        "successful_steps": len([s for s in summary["steps_performed"] if s["status"] == "success"]),
        "failed_steps": len([s for s in summary["steps_performed"] if s["status"] == "failed"]),
        "total_errors": len(summary["errors"]),
        "total_warnings": len(summary["warnings"])
    }

    formatted_output = format_summary(summary)
    return formatted_output

def convert_to_dataframe(data: Any) -> Optional[pd.DataFrame]:
    """Convert input data to DataFrame"""
    try:
        if isinstance(data, pd.DataFrame):
            return data.copy()
        elif isinstance(data, pd.Series):
            df = pd.DataFrame(data)
            df.columns = [data.name] if data.name else ['value']
            return df
        elif isinstance(data, (list, tuple)):
            if not data:
                return pd.DataFrame()
            elif isinstance(data[0], (list, tuple)):
                try:
                    return pd.DataFrame(data)
                except ValueError:
                    max_len = max(len(row) if isinstance(row, (list, tuple)) else 1 for row in data)
                    padded_data = [
                        list(row) + [None] * (max_len - len(row)) if isinstance(row, (list, tuple))
                        else [row] + [None] * (max_len - 1)
                        for row in data
                    ]
                    return pd.DataFrame(padded_data)
            else:
                return pd.DataFrame(data, columns=['value'])
        elif isinstance(data, dict):
            if not data:
                return pd.DataFrame()
            elif any(isinstance(v, (dict, list, tuple)) for v in data.values()):
                flattened_data = {}
                for k, v in data.items():
                    if isinstance(v, dict):
                        for sub_k, sub_v in v.items():
                            flattened_data[f"{k}_{sub_k}"] = sub_v
                    elif isinstance(v, (list, tuple)):
                        for i, item in enumerate(v):
                            flattened_data[f"{k}_{i}"] = item
                    else:
                        flattened_data[k] = v
                return pd.DataFrame([flattened_data])
            else:
                return pd.DataFrame([data])
        elif isinstance(data, np.ndarray):
            if data.size == 0:
                return pd.DataFrame()
            elif data.ndim == 1:
                return pd.DataFrame(data, columns=['value'])
            else:
                return pd.DataFrame(data)
        elif isinstance(data, str):
            if not data.strip():
                return pd.DataFrame()
            try:
                return pd.read_json(data)
            except:
                try:
                    return pd.read_csv(StringIO(data))
                except:
                    if '\n' in data:
                        return pd.DataFrame([line.strip() for line in data.split('\n') if line.strip()], columns=['value'])
                    else:
                        return pd.DataFrame([data], columns=['value'])
    except Exception as e:
        raise MetaError(f"Error converting to DataFrame: {str(e)}")
    return None

def convert_from_dataframe(df: pd.DataFrame, target_type: type) -> Any:
    """Convert DataFrame back to original type"""
    try:
        if target_type == list:
            return df.values.tolist()
        elif target_type == tuple:
            return tuple(df.values.tolist())
        elif target_type == dict:
            return df.to_dict()
        elif target_type == np.ndarray:
            return df.values
        elif target_type == str:
            return df.to_json()
        else:
            return df
    except Exception as e:
        raise MetaError(f"Error converting from DataFrame: {str(e)}")

def add_function_insights(summary: Dict, function_name: str, args: Dict, current_data: pd.DataFrame, original_data: Any) -> None:
    """Add insights based on function execution"""
    if function_name == "detect_outliers":
        summary["insights"].append(f"Outlier detection completed with parameters: {args}")
    elif function_name == "handle_nulls":
        summary["insights"].append(f"Null handling completed with parameters: {args}")
    elif function_name == "detect_errors":
        summary["insights"].append(f"Error detection completed with parameters: {args}")
    elif function_name == "remove":
        if args.get('operation') == 'duplicates':
            dup_count = len(original_data) - len(current_data)
            summary["insights"].append(f"Removed {dup_count} duplicates")
        elif args.get('operation') == 'columns':
            summary["insights"].append(f"Removed columns: {args.get('columns')}")
    elif function_name == "convert_type":
        summary["insights"].append(f"Type conversion completed with parameters: {args}")
    elif function_name == "format_dt":
        features = [feat for feat in ['day', 'month', 'year', 'quarter', 'hour', 'minute', 'day_of_week'] if args.get(feat)]
        insight = f"Formatted datetime for column '{args.get('columns')}'"
        if features:
            insight += f" (added features: {features})"
        if args.get('from_timezone') and args.get('to_timezone'):
            insight += f", converted timezone: {args['from_timezone']} → {args['to_timezone']}"
        summary["insights"].append(insight)
    elif function_name == "split_column":
        summary["insights"].append(f"Split column '{args.get('column')}' using delimiter: '{args.get('delimiter')}'")
    elif function_name == "refine":
        summary["insights"].append(f"Refined data with clean_rows={args.get('clean_rows', True)}")
    elif function_name == "manual_rename_columns":
        summary["insights"].append(f"Renamed columns: {args.get('rename_dict')}")
    elif function_name == "remove_chars":
        insight = f"Cleaned text in columns: {args.get('columns')}"
        if args.get('strip_all'):
            insight += " (removed all extra spaces)"
        if args.get('custom_characters'):
            insight += f" (removed characters: {args.get('custom_characters')})"
        summary["insights"].append(insight)
    elif function_name == "reformat":
        summary["insights"].append(f"Reformatted column '{args.get('target_column')}' based on format of '{args.get('reference_column')}'")
    elif function_name == "scale_data":
        summary["insights"].append(f"Scaled data in columns {args.get('columns')} using method: {args.get('method', 'minmax')}")
    elif function_name == "convert_unit":
        summary["insights"].append(f"Converted units for {args.get('columns')} from {args.get('from_unit')} to {args.get('to_unit')} ({args.get('unit_category')})")
    elif function_name == "sample_data":
        summary["insights"].append("Loaded example dataset")
    elif function_name == "display_logs":
        summary["insights"].append("Retrieved function call history and data transformation logs")
    elif function_name == "undo":
        summary["insights"].append("Reverted to previous state in data transformation history")


