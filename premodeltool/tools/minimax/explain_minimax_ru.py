#!/bin/bash
import pandas as pd
import json


excel_file = "../autotestllm/report/minimax/minimax_abab55_20230907.xlsx"
out_file = "../autotestllm/report/minimax/minimax_abab55_20230907_simple.xlsx"


def get_reply(json_str):
    return json.loads(json_str)['reply']

if __name__ == "__main__":
    df = pd.read_excel(excel_file)
    print(df['回复'][0], type(df['回复'][0]))
    print(json.loads(df['回复'][0])['reply'])

    df['回复'] = df['回复'].apply(lambda x: get_reply(x))

    df.to_excel(out_file)