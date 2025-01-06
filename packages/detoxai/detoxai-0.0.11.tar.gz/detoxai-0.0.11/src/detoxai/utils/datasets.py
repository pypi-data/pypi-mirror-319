import random
from typing import Optional, Tuple, Union, Dict, List
from pathlib import Path

import os
import PIL
import PIL.Image
import numpy as np
import pandas as pd
import torch

# from torch.utils.data import Dataset
import yaml
from torchvision.datasets.folder import VisionDataset

from ...detoxai import DETOXAI_DATASET_PATH

# NOTE: transforms and the combination of transform and target_transform are mutually exclusive

CELEBA_DATASET_CONFIG = {
    "name": "celeba",
    "variant": "default",  # or None
    "target": "Male",  # target attribute that should be predicted
    "splits": {"train": 0.6, "test": 0.2, "unlearn": 0.2},
}

CELEBA_VARIANT_CONFIG = {
    "dataset": "celeba",
    "variant": "default",
    "splits": {
        "train": {
            "fraction": 0.6,
        },
        "test": {
            "fraction": 0.2,
        },
        "unlearn": {
            "fraction": 0.2,
        },
    },
}


def make_detoxai_datasets_variant(config, name="default_variant"):
    """
    variants/
        celeba/
            variants/
                variant1/
                    splits/
                        train.npy
                        test.npy
                        unlearn.npy
                    variant_config.yaml
                variant2/
                    splits/
                        train.npy
                        test.npy
                        unlearn.npy
    """

    variant_path = (
        Path(DETOXAI_DATASET_PATH) / config["name"] / "variants" / name / "splits"
    )
    os.makedirs(variant_path, exist_ok=True)

    labels = pd.read_csv(Path(DETOXAI_DATASET_PATH) / config["name"] / "labels.csv")


def get_detoxai_datasets(
    config: dict,
    transform: Optional[
        callable
    ] = None,  # takes in a PIL image and returns a transformed version
    transforms: Optional[
        callable
    ] = None,  # takes in an image and a label and returns the transformed versions of both
    target_transform: Optional[
        callable
    ] = None,  # A function/transform that takes in the target and transforms it.
    download: bool = False,
    seed: Optional[int] = None,
    device: str = None,
    saved_variant: Optional[str] = None,
) -> Dict[str, "DetoxaiDataset"]:
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)

    # generate indices for all the splits randomly
    home_detoxai_dir = Path.home() / ".detoxai"
    labels = pd.read_csv(home_detoxai_dir / config["name"] / "labels.csv")
    all_indices = np.arange(len(labels))
    np.random.shuffle(all_indices)
    split_indices = {}
    start = 0
    for split_name, frac in config["splits"].items():
        end = start + int(frac * len(all_indices))
        split_indices[split_name] = all_indices[start:end]
        start = end

    datasets = {}
    for split, indices in split_indices.items():
        datasets[split] = DetoxaiDataset(
            config,
            home_detoxai_dir,
            indices,
            transform=transform,
            transforms=transforms,
            target_transform=target_transform,
            download=download,
            seed=seed,
            device=device,
        )

    return datasets


class DetoxaiDataset(VisionDataset):
    def __init__(
        self,
        config: dict,
        root: Union[str, Path],
        split_indices: np.ndarray,
        transform: Optional[
            callable
        ] = None,  # takes in a PIL image and returns a transformed version
        transforms: Optional[
            callable
        ] = None,  # takes in an image and a label and returns the transformed versions of both
        target_transform: Optional[
            callable
        ] = None,  # A function/transform that takes in the target and transforms it.
        download: bool = False,
        seed: Optional[int] = None,
        device: str = None,
    ) -> None:
        super().__init__(
            root,
            transform=transform,
            transforms=transforms,
            target_transform=target_transform,
        )
        self.config = config
        self.root = Path(root)
        self.device = device

        if download:
            self.download()

        if not self._check_integrity():
            raise RuntimeError(
                "Dataset not found or corrupted. You can use download=True to download it"
            )

        self.labels = self._read_labels_from_file()
        self.labels_mapping = self._read_labels_mapping_from_file()
        # self._target_labels_translation = self.get_target_label_translation()
        self.split_indices = split_indices

        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
            torch.manual_seed(seed)

    def _read_labels_from_file(self) -> pd.DataFrame:
        df = pd.read_csv(self.root / self.config["name"] / "labels.csv")
        return df

    def _read_labels_mapping_from_file(self) -> pd.DataFrame:
        labels_mapping_from_yaml = yaml.safe_load(
            (self.root / self.config["name"] / "labels_mapping.yaml").open()
        )
        return labels_mapping_from_yaml

    def download(self):
        pass

    def _check_integrity(self) -> bool:
        return (self.root / self.config["name"]).exists()

    def __len__(self) -> int:
        return len(self.split_indices)

    def __getitem__(self, idx: int) -> Tuple[PIL.Image.Image, int, dict]:
        img = self._load_image(self.split_indices[idx])
        label = self._load_label(self.split_indices[idx])
        fairness_attributes = self._load_fairness_attributes(self.split_indices[idx])

        if self.transforms is not None:
            img, label = self.transforms(img, label)
        else:
            if self.transform is not None:
                img = self.transform(img)
            if self.target_transform is not None:
                label = self.target_transform(label)

        return img, label, fairness_attributes

    def _load_image(self, idx: int) -> PIL.Image.Image:
        img_path = (
            self.root / self.config["name"] / "data" / self.labels.iloc[idx]["image_id"]
        )
        img = PIL.Image.open(img_path)
        return img

    def _load_label(self, idx: int):
        label = self.labels.iloc[idx][self.config["target"]]
        return label

    def _load_fairness_attributes(self, idx: int) -> dict:
        fairness_attributes = {}
        for key, value in self.labels_mapping.items():
            # fairness_attributes[key] = value[self.labels.iloc[idx][key]]
            fairness_attributes[key] = self.labels.iloc[idx][key]
        return fairness_attributes

    def get_class_names(self) -> List[str]:
        return [
            f"{self.config['target']}_{item.replace(' ', '_')}"
            for key, item in self.labels_mapping[self.config["target"]].items()
        ]

    # def get_target_label_translation(self) -> dict:
    #     return {i: name for i, name in enumerate(self.get_class_names())}

    def get_num_classes(self) -> int:
        return len(self.labels_mapping[self.config["target"]])

    def get_collate_fn(self, protected_attribute: str, protected_attribute_value: str):
        def collate_fn(
            batch: List[Tuple[torch.Tensor, str, Dict[str, Union[str, int]]]],
        ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
            images = torch.stack([item[0] for item in batch])
            labels = torch.tensor([item[1] for item in batch])
            protected_attributes = torch.tensor(
                [
                    int(item[2].get(protected_attribute) == protected_attribute_value)
                    for item in batch
                ]
            )
            return images, labels, protected_attributes

        return collate_fn
