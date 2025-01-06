import torch
import logging
from abc import ABC, abstractmethod
from torch import nn
import lightning as L

from ..model_correction import ModelCorrectionMethod

logger = logging.getLogger(__name__)


class PosthocBase(ModelCorrectionMethod, ABC):
    """Abstract base class for binary post-hoc debiasing methods."""

    def __init__(
        self,
        model: nn.Module | L.LightningModule,
        experiment_name: str,
        device: str,
        **kwargs,
    ) -> None:
        super().__init__(model, experiment_name, device)
        self.hooks = []

    @abstractmethod
    def apply_model_correction(self) -> None:
        raise NotImplementedError

    def _get_model_predictions(
        self, dataloader: torch.utils.data.DataLoader
    ) -> torch.Tensor:
        """Get model predictions on dataloader"""
        self.model.eval()
        predictions = []
        with torch.no_grad():
            for batch in dataloader:
                inputs, _ = batch
                inputs = inputs.to(self.device)
                outputs = self.model(inputs)
                predictions.append(outputs)
        return torch.cat(predictions)
