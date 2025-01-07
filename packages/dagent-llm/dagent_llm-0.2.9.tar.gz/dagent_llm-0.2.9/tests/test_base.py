import os
import csv
import subprocess
import pandas as pd
from tqdm import tqdm
from datetime import datetime
import argparse
import time

from rich.console import Console
from rich.table import Table

console = Console()

# Importing relevant classes
from dspeech import STT
from dagent_llm import LLM
from dguard import DguardModel as dm

# Initialize LLM
dagent = LLM(
    "ollama123",
    api_key="your_api_key",
    # ollama
    base_url="http://localhost:8004/v1",
    timeout=10000,
    max_retries=3,
    model_name="Qwen/Qwen2.5-7B-Instruct-GPTQ-Int4",
    temperature=0.5
)

r = dagent.chat("讲个笑话",stream=True)
for i in r:
    # i转为字典
    i=i.dict()
    print(i["content"])