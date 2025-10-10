import torch
import torch.nn as nn


class EEGNet(nn.Module):
    """
    PyTorch implementation of the EEGNet model.
    See: https://arxiv.org/abs/1611.08024
    """
    def __init__(self, n_channels, n_classes, input_size_s,
                 F1=8, D=2, F2=16, kernel_size=64, dropout_rate=0.5):
        super(EEGNet, self).__init__()
        self.n_channels = n_channels
        self.n_classes = n_classes
        self.input_size_s = input_size_s

        # Block 1: Temporal Convolution
        self.block1 = nn.Sequential(
            nn.Conv2d(1, F1, (1, kernel_size), stride=1, padding=(0, kernel_size // 2), bias=False),
            nn.BatchNorm2d(F1),
            # Depthwise Convolution
            nn.Conv2d(F1, F1 * D, (n_channels, 1), groups=F1, bias=False),
            nn.BatchNorm2d(F1 * D),
            nn.ELU(),
            nn.AvgPool2d((1, 4)),
            nn.Dropout(dropout_rate)
        )

        # Block 2: Separable Convolution
        self.block2 = nn.Sequential(
            # Separable Conv2d
            nn.Conv2d(F1 * D, F2, (1, 16), padding=(0, 8), groups=F1*D, bias=False),
            nn.Conv2d(F2, F2, 1, bias=False),
            nn.BatchNorm2d(F2),
            nn.ELU(),
            nn.AvgPool2d((1, 8)),
            nn.Dropout(dropout_rate)
        )

        # Classifier
        self.classifier = nn.Sequential(
            nn.Linear(self._get_classifier_input_features(), n_classes)
        )

    def _get_classifier_input_features(self):
        """
        Calculates the input size for the classifier block.
        """
        with torch.no_grad():
            dummy_input = torch.zeros(1, 1, self.n_channels, self.input_size_s)
            features = self.block1(dummy_input)
            features = self.block2(features)
            return features.view(1, -1).size(1)

    def forward(self, x):
        # Expected input shape: (batch_size, n_channels, n_samples)
        # Reshape to (batch_size, 1, n_channels, n_samples) for Conv2d
        x = x.unsqueeze(1)
        
        x = self.block1(x)
        x = self.block2(x)
        
        # Flatten for the classifier
        x = x.view(x.size(0), -1)
        
        # Apply classifier
        output = self.classifier(x)
        
        # Apply sigmoid for binary classification (or can be done in loss function)
        return torch.sigmoid(output)

