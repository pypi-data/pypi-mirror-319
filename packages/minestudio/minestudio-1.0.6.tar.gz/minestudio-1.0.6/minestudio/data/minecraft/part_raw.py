'''
Date: 2024-11-10 10:26:32
LastEditors: caishaofei caishaofei@stu.pku.edu.cn
LastEditTime: 2024-12-17 06:14:29
FilePath: /MineStudio/minestudio/data/minecraft/part_raw.py
'''
import io
import re
import os
import math
import lmdb
import pickle
import random

import numpy as np
import torch
from rich.console import Console
from pathlib import Path
from typing import Union, Tuple, List, Dict, Callable, Sequence, Mapping, Any, Optional, Literal

from minestudio.data.minecraft.core import BaseDataset

class RawDataset(BaseDataset):
    """Raw dataset for training and testing. """
    def __init__(self, 
        win_len: int = 1, 
        skip_frame: int = 1, 
        split: Literal['train', 'val'] = 'train',
        split_ratio: float = 0.8,
        verbose: bool = True,
        shuffle: bool = False, 
        **kernel_kwargs, 
    ) -> Any:
        super(RawDataset, self).__init__(verbose=verbose, **kernel_kwargs)
        self.win_len = win_len
        self.skip_frame = skip_frame
        self.split = split
        self.split_ratio = split_ratio
        self.verbose = verbose
        self.shuffle = shuffle
        self.build_items()
    
    def build_items(self) -> None:
        self.episodes_with_length = self.kernel.get_episodes_with_length()
        _episodes_with_length = list(self.episodes_with_length.items())

        if self.shuffle:
            seed = 0
            print(f"[Raw Dataset] Shuffling episodes with seed {seed}. ")
            random.seed(seed) # ensure the same shuffle order for all workers
            random.shuffle(_episodes_with_length)

        divider = int(len(_episodes_with_length) * self.split_ratio)
        if self.split == 'train':
            _episodes_with_length = _episodes_with_length[:divider]
        else:
            _episodes_with_length = _episodes_with_length[divider:]
        
        self.items = []
        self.num_items = 0
        self.episodes_with_items = []
        for episode, length in _episodes_with_length:
            num_episode_items = (length + self.win_len - 1) // self.win_len 
            self.episodes_with_items.append( (episode, num_episode_items, self.num_items) )
            self.num_items += num_episode_items
            self.items.append( (self.num_items, episode) )

    def locate_item(self, idx: int) -> Tuple[str, int]:
        """Find the first episode that idx > acc[episode]"""
        left, right = 0, len(self.items)
        while left < right:
            mid = (left + right) // 2
            if self.items[mid][0] <= idx:
                left = mid + 1
            else:
                right = mid
        if left == 0:
            relative_idx = idx
        else:
            relative_idx = idx - self.items[left-1][0]
        episode = self.items[left][1]
        return episode, relative_idx

    def __len__(self) -> int:
        return self.num_items
    
    def __getitem__(self, idx: int) -> Mapping[str, torch.Tensor]:
        assert idx < len(self), f"Index <{idx}> out of range <{len(self)}>"
        episode, relative_idx = self.locate_item(idx)
        start = max(1, relative_idx * self.win_len) # start > 0 is the prequest for previous action
        item = self.kernel.read(episode, start, self.win_len, self.skip_frame)
        item['text'] = 'raw'
        item['timestamp'] = np.arange(start, start+self.win_len, self.skip_frame)
        item['episode'] = episode
        episode_samples = math.ceil(self.episodes_with_length[episode] / self.win_len)
        item['progress'] = f"{relative_idx}/{episode_samples}"
        item = self.postprocess(item)
        return item

if __name__ == '__main__':
    
    kernel_kwargs = dict(
        dataset_dirs=[
            '/nfs-shared-2/data/contractors/dataset_6xx', 
            '/nfs-shared-2/data/contractors/dataset_7xx', 
            '/nfs-shared-2/data/contractors/dataset_8xx', 
            '/nfs-shared-2/data/contractors/dataset_9xx', 
            '/nfs-shared-2/data/contractors/dataset_10xx', 
        ], 
        enable_contractor_info=False, 
        enable_segment=True, 
    )
    
    dataset = RawDataset(
        frame_width=224,
        frame_height=224,
        win_len=128, 
        skip_frame=1,
        split='train',
        split_ratio=0.9,
        verbose=True,
        **kernel_kwargs, 
    )
    
    from minestudio.data.minecraft.utils import MineDistributedBatchSampler
    sampler = MineDistributedBatchSampler(dataset, batch_size=4, num_replicas=1, rank=0, shuffle=False, drop_last=True)
    from torch.utils.data import DataLoader
    from tqdm import tqdm
    loader = DataLoader(dataset, batch_sampler=sampler, num_workers=4)
    for idx, batch in enumerate(loader):
        print(
            "\t".join(
                [f"{a} {b}" for a, b in zip(batch['episode'], batch['progress'])]
            )
        )
        if idx > 50:
            break
