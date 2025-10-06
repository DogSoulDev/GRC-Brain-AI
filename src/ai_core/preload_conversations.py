"""
preload_conversations.py - Download and prepare robust English conversational datasets for incremental learning
"""
from datasets import load_dataset, DatasetDict
import os

def download_conversation_datasets():
    datasets_to_download = [
        ("OpenAssistant/oasst1", "openassistant"),
        ("tatsu-lab/alpaca", "alpaca"),
        ("daily_dialog", "dailydialog"),
    ]
    base_dir = os.path.join(os.path.dirname(__file__), "..", "conversation_datasets")
    os.makedirs(base_dir, exist_ok=True)
    for dataset_name, subdir in datasets_to_download:
        print(f"Downloading {dataset_name}...")
        try:
            ds = load_dataset(dataset_name)
        except Exception as e:
            print(f"Failed to download {dataset_name}: {e}")
            continue
        out_dir = os.path.join(base_dir, subdir)
        os.makedirs(out_dir, exist_ok=True)
        # If DatasetDict, iterate splits; else, treat as single Dataset
        if isinstance(ds, DatasetDict):
            for split_name, split_data in ds.items():
                # Only process splits that are datasets.Dataset
                import datasets
                if isinstance(split_data, datasets.Dataset):
                    try:
                        df = split_data.to_pandas()
                        import pandas as pd
                        if isinstance(df, pd.DataFrame):
                            df.to_parquet(os.path.join(out_dir, f"{split_name}.parquet"))
                            print(f"Saved {dataset_name} [{split_name}] to {os.path.join(out_dir, f'{split_name}.parquet')}")
                        else:
                            print(f"Skipped {dataset_name} [{split_name}] (not a DataFrame)")
                    except Exception as e:
                        print(f"Could not save {dataset_name} [{split_name}]: {e}")
                else:
                    print(f"Skipped {dataset_name} [{split_name}] (unsupported type)")
        else:
            import datasets
            if isinstance(ds, datasets.Dataset):
                try:
                    df = ds.to_pandas()
                    import pandas as pd
                    if isinstance(df, pd.DataFrame):
                        df.to_parquet(os.path.join(out_dir, "data.parquet"))
                        print(f"Saved {dataset_name} to {os.path.join(out_dir, 'data.parquet')}")
                    else:
                        print(f"Skipped {dataset_name} (not a DataFrame)")
                except Exception as e:
                    print(f"Could not save {dataset_name}: {e}")
            else:
                print(f"Skipped {dataset_name} (unsupported type)")

    # TODO: Preload all US GRC/legal/cybersecurity documents, laws, frameworks, and standards into official_docs/ for maximum coverage.

if __name__ == "__main__":
    download_conversation_datasets()
