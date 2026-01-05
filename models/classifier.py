import torch
import torch.nn as nn
import timm

class SurfaceClassifier(nn.Module):
    def __init__(self, num_materials=6, num_finishes=5, backbone_name='resnet50'):
        super(SurfaceClassifier, self).__init__()
        # Load Pre-trained Backbone
        self.backbone = timm.create_model(backbone_name, pretrained=True, num_classes=0) # num_classes=0 removes the head
        self.num_features = self.backbone.num_features
        
        # Multi-Head Architecture
        # Head 1: Material Class (e.g. Metal, Plastic, Glass)
        self.material_head = nn.Sequential(
            nn.Linear(self.num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_materials)
        )
        
        # Head 2: Texture/Finish Class (e.g. Mirror, Rough, Embossed)
        self.finish_head = nn.Sequential(
            nn.Linear(self.num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_finishes)
        )

    def forward(self, x):
        # Extract features
        features = self.backbone(x)
        
        # Forward through heads
        material_logits = self.material_head(features)
        finish_logits = self.finish_head(features)
        
        return material_logits, finish_logits

if __name__ == "__main__":
    # Test model instantiation
    model = SurfaceClassifier()
    dummy_input = torch.randn(1, 3, 224, 224)
    mat, fin = model(dummy_input)
    print(f"Material Output Shape: {mat.shape}")
    print(f"Finish Output Shape: {fin.shape}")
