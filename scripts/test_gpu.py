import torch
print(torch.__version__)  # Should print 1.10.0
print(torch.cuda.is_available())  # Should print True
print(torch.cuda.get_device_name(0))  # Should show your GPU