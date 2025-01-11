import random
import re
from datasets import load_dataset
from datasets.dataset_dict import DatasetDict, IterableDatasetDict
from datasets.arrow_dataset import Dataset
from datasets.iterable_dataset import IterableDataset
from .base_dataset import BaseDataset
from loguru import logger
from zangief.validator.reward import Reward
from typing import Any, Dict, List, Union


class CC100(BaseDataset):

    def __init__(self):
        super().__init__()
        self.all_languages = [
            "ar",
            "bn",
            "cs",
            "de",
            "el",
            "en",
            "es",
            "fa",
            "fr",
            "he",
            "hi",
            "hu",
            "it",
            "ja",
            "jv",
            "ko",
            "my",
            "nl",
            "pa",
            "pl",
            "pt",
            "ro",
            "ru",
            "sv",
            "ta",
            "te",
            "th",
            "tr",
            "uk",
            "ur",
            "vi",
            "zh",
        ]
        # Just select 10 random languages at init
        self.selected_languages = random.sample(self.all_languages, 10)
        self.language_alias = {"zh": "zh-Hans", "zht": "zh-Hant"}
        logger.info(f"Selected languages: {self.selected_languages}")

    @staticmethod
    def filter_dataset(example):
        text = example["text"].strip()
        length_filter = len(text) > 50
        url_filter = CC100.contains_url(text)
        return length_filter and url_filter

    @staticmethod
    def contains_url(text: str) -> bool:
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return not bool(url_pattern.search(text))

    def get_random_record(self, language="es") -> str:
        """Get a random record from a language dataset using streaming"""
        try:
            # Get the correct language code
            dataset_language = self.language_alias.get(language, language)
            
            # Load the dataset in streaming mode
            streaming_dataset = load_dataset(
                "cc100", 
                dataset_language, 
                split="train", 
                streaming=True
            )
            
            # Shuffle with a small buffer and apply filters
            filtered_dataset = streaming_dataset.shuffle(
                seed=random.randint(1, 10000),  # Random seed for better distribution
                buffer_size=100  # Small buffer just for shuffling
            ).filter(self.filter_dataset)
            
            # Take first valid record
            for item in filtered_dataset:
                return item["text"].strip()
                
        except Exception as e:
            logger.error(f"Error getting random record for {language}: {e}")
            return "Error fetching text"