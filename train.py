import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, Dataset
from models.classifier import SurfaceClassifier
import os

# Dummy Dataset for Scaffold
class DummyDataset(Dataset):
    def __init__(self, length=100):
        self.length = length
    
    def __len__(self):
        return self.length
    
    def __getitem__(self, idx):
        # Return dummy image and dummy labels
        return torch.randn(3, 224, 224), torch.randint(0, 5, (1,)).item(), torch.randint(0, 4, (1,)).item()

def train_model(num_epochs=5):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")
    
    # Instantiate Model
    model = SurfaceClassifier(num_materials=6, num_finishes=5).to(device)
    
    # Loss Functions for multi-task learning
    criterion_material = nn.CrossEntropyLoss()
    criterion_finish = nn.CrossEntropyLoss()
    
    # Optimizer
    optimizer = optim.Adam(model.parameters(), lr=1e-4)
    
    # Dataloader
    dataset = DummyDataset()
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)
    
    print("Starting Training Loop...")
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        
        for images, mat_labels, fin_labels in dataloader:
            images = images.to(device)
            mat_labels = mat_labels.to(device)
            fin_labels = fin_labels.to(device)
            
            optimizer.zero_grad()
            
            # Forward pass
            mat_out, fin_out = model(images)
            
            # Compute loss
            loss_mat = criterion_material(mat_out, mat_labels)
            loss_fin = criterion_finish(fin_out, fin_labels)
            
            # Combined loss (can use weighted sum)
            total_loss = loss_mat + loss_fin
            
            # Backward pass
            total_loss.backward()
            optimizer.step()
            
            running_loss += total_loss.item()
            
        print(f"Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(dataloader):.4f}")

    # Save Model
    print("Saving model...")
    os.makedirs('checkpoints', exist_ok=True)
    torch.save(model.state_dict(), 'checkpoints/v_sams_model.pth')
    print("Model saved to checkpoints/v_sams_model.pth")

if __name__ == "__main__":
    train_model(num_epochs=1)
