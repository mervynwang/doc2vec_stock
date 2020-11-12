
import torch
import torch.nn as nn
import torch.nn.functional as F

class MyModel(nn.Module):
    def __init__(self, model_param: ModelParam):
        super().__init__()
        self.embedding = nn.Embedding(
            model_param.vocab_size,
            model_param.embedding_dim
        )
        self.lin = nn.Linear(
            model_param.input_size * model_param.embedding_dim,
            model_param.target_dim
        )

    def forward(self, x):
        features = self.embedding(x).view(x.size()[0], -1)
        features = F.relu(features)
        features = self.lin(features)
        return features