import pandas as pd

import torch
import torch.nn as nn

import torchevent.layers as L
from torchevent.profile import LayerwiseProfiler

def conv_pool_block(in_channels, out_channels, kernel_size, padding, pooling_size, pooling_stride, tsslbp_config):
    """
    A block combining convolution and pooling layers with TSSLBP configuration.
    
    Args:
        in_channels (int): Number of input channels.
        out_channels (int): Number of output channels.
        kernel_size (int): Size of the convolutional kernel.
        padding (int): Padding for the convolutional layer.
        pooling_size (int): Pooling kernel size.
        pooling_stride (int): Pooling stride.
        tsslbp_config (dict): Configuration for TSSLBP.
    
    Returns:
        nn.Sequential: A sequential block of convolution and pooling layers.
    """
    return nn.Sequential(
        L.SNNConv3d(in_channels, out_channels, kernel_size, padding=padding, **tsslbp_config),
        L.SNNSumPooling(pooling_size, pooling_stride)
    )

# Base Network Class
class BaseNet(nn.Module):
    def __init__(self, tau_m, tau_s, n_steps):
        super(BaseNet, self).__init__()
        self.tsslbp_config = {
            'use_tsslbp': True,
            'tau_m': tau_m,
            'tau_s': tau_s,
            'n_steps': n_steps
        }
        self.layers = nn.ModuleList()  # A single ModuleList to store all layers (conv and fc)
        
        # Initialize LayerwiseProfiler and attach to the model
        self.profiler = LayerwiseProfiler(self)

    def forward(self, x):
        x = x.permute(0, 2, 3, 4, 1)  # Assuming the permutation is common across models
        for layer in self.layers:
            x = layer(x)
        return x

    def _make_layers(self, layer_configs):
        """
        Helper method to create layers dynamically.
        """
        layers = []
        for layer_class, layer_params in layer_configs:
            layer = layer_class(**layer_params)
            layers.append(layer)
        return layers

    def weight_clipper(self):
        for _, module in self.named_modules():
            # Check if the module has no submodules (leaf module)
            if len(list(module.children())) == 0:
                if hasattr(module, 'weight_clipper'):
                    module.weight_clipper()
                
    def save_model(self, filename):
        model_data = {
            "state_dict": self.state_dict(),
            "tsslbp_config": self.tsslbp_config
        }
        torch.save(model_data, filename)
        print(f"Model save to {filename}")
        
    def load_model(self, filename):
        model_data = torch.load(filename)
        state_dict = model_data['state_dict']

        # Filter out keys not present in the current model
        keys_to_delete = []
        for key in state_dict.keys():
            # Check if the key exists in the model
            parts = key.split('.')
            module = self
            exists = True

            for part in parts[:-1]:  # Traverse the hierarchy
                if not hasattr(module, part):
                    exists = False
                    break
                module = getattr(module, part)

            if not exists or not hasattr(module, parts[-1]):  # Check final attribute
                keys_to_delete.append(key)

        # Remove keys not present in the model
        for key in keys_to_delete:
            print(f"Deleting key: {key} from state_dict")
            del state_dict[key]

        # Load the filtered state_dict into the model
        self.load_state_dict(state_dict, strict=False)
        self.tsslbp_config = model_data.get('tsslbp_config', None)  # Load config if present

        print(f"Model loaded from {filename}")
        print("tsslbp config updated:", self.tsslbp_config)

    
    def trace(self, input_data):
        """
        Perform a trace using LayerwiseProfiler with a given input shape or tensor.

        Args:
            input_data (tuple or torch.Tensor): If tuple, it is treated as input shape. 
                                                If torch.Tensor, it is used directly as input.
        Returns:
            list: Collected profiling data from LayerwiseProfiler.
        """
        # Determine input tensor
        if isinstance(input_data, tuple):
            dummy_input = torch.rand((1,) + input_data)  # Create dummy input from shape
        elif isinstance(input_data, torch.Tensor):
            dummy_input = input_data  # Use the provided tensor directly
        else:
            raise ValueError("input_data must be either a tuple (input shape) or a torch.Tensor")

        # Perform profiling
        with self.profiler.profile(profile_type='trace') as prof:
            self(dummy_input)  # Perform a forward pass

        return self.profiler.get_data()
    
    def summary(self, input_shape):
        """
        Generate a summary of the model using LayerwiseProfiler.
        """
        dummy_input = torch.rand((1,) + input_shape)
        with self.profiler.profile(profile_type='summary') as prof:
            _ = self(dummy_input)  # Perform a forward pass with dummy input

        summary_data = self.profiler.get_data()
        
        df = pd.DataFrame(summary_data)
        
        print(df.to_string())

        return df

# NCARS Network 64x64 input
class NCARSNet(BaseNet):
    def __init__(self, tau_m, tau_s, n_steps, weight = None):
        super(NCARSNet, self).__init__(tau_m, tau_s, n_steps)
        
        # Configuration of layers for NCARSNet
        layer_configs = [
            (conv_pool_block, {'in_channels': 1, 'out_channels': 15, 'kernel_size': 5, 'padding': 2, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}),
            (conv_pool_block, {'in_channels': 15, 'out_channels': 40, 'kernel_size': 5, 'padding': 2, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}),
            (conv_pool_block, {'in_channels': 40, 'out_channels': 80, 'kernel_size': 3, 'padding': 1, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}),
            (conv_pool_block, {'in_channels': 80, 'out_channels': 160, 'kernel_size': 3, 'padding': 1, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}),
            (conv_pool_block, {'in_channels': 160, 'out_channels': 320, 'kernel_size': 3, 'padding': 1, 'pooling_size': 4, 'pooling_stride': 4, 'tsslbp_config': self.tsslbp_config}),
            (L.SNNLinear, {'in_features': 320, 'out_features': 64, **self.tsslbp_config}),
            (L.SNNLinear, {'in_features': 64, 'out_features': 2, **self.tsslbp_config}),
        ]

        # Create the layers dynamically and store them in self.layers
        self.layers = nn.ModuleList(self._make_layers(layer_configs))
        
        # If a weight path is provided, load the model weights
        if weight is not None:
            self.load_model(weight)

# NMNIST Network 34x34 input
class NMNISTNet(BaseNet):
    def __init__(self, tau_m, tau_s, n_steps, weight = None):
        super(NMNISTNet, self).__init__(tau_m, tau_s, n_steps)
        
        # Configuration of layers for NMNISTNet
        layer_configs = [
            (conv_pool_block, {'in_channels': 2, 'out_channels': 12, 'kernel_size': 5, 'padding': 1, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}),
            (conv_pool_block, {'in_channels': 12, 'out_channels': 64, 'kernel_size': 5, 'padding': 0, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}),
            (L.SNNLinear, {'in_features': 2304, 'out_features': 10, **self.tsslbp_config}),
        ]

        # Create the layers dynamically and store them in self.layers
        self.layers = nn.ModuleList(self._make_layers(layer_configs))
        
        # If a weight path is provided, load the model weights
        if weight is not None:
            self.load_model(weight)

# DVSGesture Network 128x128 input
class DVSGestureNet(BaseNet):
    def __init__(self, tau_m, tau_s, n_steps, weight = None):
        super(DVSGestureNet, self).__init__(tau_m, tau_s, n_steps)
        
        # Configuration of layers for DVSGestureNet
        layer_configs = [
            (conv_pool_block, {'in_channels': 2, 'out_channels': 15, 'kernel_size': 5, 'padding': 2, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}), 
            (conv_pool_block, {'in_channels': 15, 'out_channels': 40, 'kernel_size': 5, 'padding': 2, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}), 
            (conv_pool_block, {'in_channels': 40, 'out_channels': 80, 'kernel_size': 3, 'padding': 1, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}), 
            (conv_pool_block, {'in_channels': 80, 'out_channels': 160, 'kernel_size': 3, 'padding': 1, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}), 
            (conv_pool_block, {'in_channels': 160, 'out_channels': 320, 'kernel_size': 3, 'padding': 1, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}), 
            (L.SNNLinear, {'in_features': 5120, 'out_features': 512, **self.tsslbp_config}),
            (L.SNNLinear, {'in_features': 512, 'out_features': 11, **self.tsslbp_config}),
        ]

        # Create the layers dynamically and store them in self.layers
        self.layers = nn.ModuleList(self._make_layers(layer_configs))
        
        # If a weight path is provided, load the model weights
        if weight is not None:
            self.load_model(weight)
            

# DVSGesture Network 64x64 input
class PGen4NetMini(BaseNet):
    def __init__(self, tau_m, tau_s, n_steps, weight = None):
        super(PGen4NetMini, self).__init__(tau_m, tau_s, n_steps)
        
        # Configuration of layers for NCARSNet
        layer_configs = [
            (conv_pool_block, {'in_channels': 1, 'out_channels': 15, 'kernel_size': 5, 'padding': 2, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}), #32
            (conv_pool_block, {'in_channels': 15, 'out_channels': 40, 'kernel_size': 5, 'padding': 2, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}), #16
            (conv_pool_block, {'in_channels': 40, 'out_channels': 80, 'kernel_size': 3, 'padding': 1, 'pooling_size': 2, 'pooling_stride': 2, 'tsslbp_config': self.tsslbp_config}), #8
            (L.SNNConv3d, {'in_channels': 80, 'out_channels': 160, 'kernel_size': 3, 'padding': 1, 'stride': 2, **self.tsslbp_config}), # 4
            (conv_pool_block, {'in_channels': 160, 'out_channels': 320, 'kernel_size': 3, 'padding': 1, 'pooling_size': 4, 'pooling_stride': 4, 'tsslbp_config': self.tsslbp_config}), # ?
            (L.SNNLinear, {'in_features': 320, 'out_features': 64, **self.tsslbp_config}),
            (L.SNNLinear, {'in_features': 64, 'out_features': 5, **self.tsslbp_config}),
        ]

        # Create the layers dynamically and store them in self.layers
        self.layers = nn.ModuleList(self._make_layers(layer_configs))
        
        # If a weight path is provided, load the model weights
        if weight is not None:
            self.load_model(weight)
