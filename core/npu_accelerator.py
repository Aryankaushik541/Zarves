"""
NPU Accelerator for JARVIS
Leverages Neural Processing Unit (NPU) on Omen PC for faster AI inference
Supports Intel NPU, AMD XDNA, NVIDIA GPU, AMD GPU, and CPU
Auto-detects best available hardware
"""

import os
import sys
import platform
import subprocess
from typing import Optional, Dict, Any

class NPUAccelerator:
    """
    Hardware Acceleration Manager for JARVIS
    Automatically detects and uses best available hardware:
    1. NVIDIA GPU (CUDA)
    2. AMD GPU (ROCm)
    3. Intel NPU/GPU
    4. Apple Silicon (MPS)
    5. CPU (fallback)
    """
    
    def __init__(self):
        self.npu_available = False
        self.npu_type = None
        self.device = "cpu"  # Default fallback
        self.acceleration_enabled = False
        self.device_name = "CPU"
        
        # Detect best hardware
        self._detect_hardware()
        
    def _detect_hardware(self):
        """Detect best available hardware in priority order"""
        print("🔍 Detecting hardware...")
        
        # Priority 1: NVIDIA GPU (CUDA)
        if self._check_nvidia_gpu():
            return
        
        # Priority 2: AMD GPU (ROCm)
        if self._check_amd_gpu():
            return
        
        # Priority 3: Intel NPU/GPU
        if self._check_intel_npu():
            return
        
        # Priority 4: Apple Silicon (MPS)
        if self._check_apple_silicon():
            return
        
        # Priority 5: CPU (fallback)
        print("⚠️  No GPU/NPU detected. Using CPU.")
        self.device = "cpu"
        self.device_name = platform.processor() or "CPU"
        self.npu_type = "CPU"
    
    def _check_nvidia_gpu(self) -> bool:
        """Check for NVIDIA GPU with CUDA support"""
        try:
            import torch
            if torch.cuda.is_available():
                self.device = "cuda"
                self.device_name = torch.cuda.get_device_name(0)
                self.npu_type = "GPU (NVIDIA CUDA)"
                self.acceleration_enabled = True
                print(f"✅ Detected: {self.device_name}")
                print(f"   CUDA Version: {torch.version.cuda}")
                return True
        except Exception as e:
            pass
        
        return False
    
    def _check_amd_gpu(self) -> bool:
        """Check for AMD GPU with ROCm support"""
        try:
            import torch
            # Check for ROCm (AMD GPU)
            if hasattr(torch.version, 'hip') and torch.version.hip:
                self.device = "hip"
                self.device_name = "AMD GPU"
                self.npu_type = "GPU (AMD ROCm)"
                self.acceleration_enabled = True
                print(f"✅ Detected: AMD GPU (ROCm)")
                print(f"   ROCm Version: {torch.version.hip}")
                return True
        except Exception as e:
            pass
        
        return False
    
    def _check_intel_npu(self) -> bool:
        """Check for Intel NPU/GPU"""
        try:
            # Check for Intel Extension for PyTorch
            import intel_extension_for_pytorch as ipex
            import torch
            
            # Intel XPU (NPU/GPU)
            if hasattr(torch, 'xpu') and torch.xpu.is_available():
                self.device = "xpu"
                self.device_name = "Intel NPU/GPU"
                self.npu_type = "NPU (Intel)"
                self.npu_available = True
                self.acceleration_enabled = True
                print(f"✅ Detected: Intel NPU/GPU")
                return True
        except ImportError:
            pass
        except Exception as e:
            pass
        
        # Check for Intel Core Ultra (has NPU)
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["wmic", "cpu", "get", "name"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW  # Hide window
                )
                cpu_info = result.stdout.lower()
                
                if "core ultra" in cpu_info or "meteor lake" in cpu_info:
                    print("💡 Intel Core Ultra detected (has NPU)")
                    print("   Install intel-extension-for-pytorch for NPU support")
                    print("   pip install intel-extension-for-pytorch")
        except:
            pass
        
        return False
    
    def _check_apple_silicon(self) -> bool:
        """Check for Apple Silicon (M1/M2/M3)"""
        try:
            if platform.system() == 'Darwin' and platform.machine() == 'arm64':
                import torch
                if torch.backends.mps.is_available():
                    self.device = "mps"
                    self.device_name = "Apple Silicon"
                    self.npu_type = "NPU (Apple Silicon)"
                    self.npu_available = True
                    self.acceleration_enabled = True
                    print(f"✅ Detected: Apple Silicon (MPS)")
                    return True
        except Exception as e:
            pass
        
        return False
    
    def get_torch_device(self):
        """Get PyTorch device object"""
        try:
            import torch
            return torch.device(self.device)
        except:
            return None
    
    def get_optimized_config(self) -> Dict[str, Any]:
        """Get optimized configuration for current hardware"""
        config = {
            "device": self.device,
            "npu_available": self.npu_available,
            "npu_type": self.npu_type,
            "batch_size": 1,
            "num_threads": os.cpu_count() or 4,
        }
        
        if self.device in ["cuda", "hip"]:
            # GPU optimizations
            config.update({
                "use_fp16": True,
                "batch_size": 8,
                "cache_enabled": True,
                "optimization_level": "balanced",
            })
        elif self.device in ["xpu", "mps"]:
            # NPU optimizations
            config.update({
                "use_fp16": True,
                "use_int8": True,
                "batch_size": 4,
                "cache_enabled": True,
                "optimization_level": "aggressive",
            })
        else:
            # CPU optimizations
            config.update({
                "use_fp16": False,
                "batch_size": 1,
                "cache_enabled": True,
                "optimization_level": "conservative",
            })
        
        return config
    
    def setup_openvino_npu(self):
        """Setup OpenVINO for Intel NPU"""
        try:
            import openvino as ov
            
            core = ov.Core()
            
            # Configure NPU
            if "NPU" in core.available_devices:
                print("🚀 Configuring Intel NPU with OpenVINO...")
                
                # Set NPU properties for optimal performance
                core.set_property("NPU", {
                    "PERFORMANCE_HINT": "LATENCY",  # Low latency mode
                    "CACHE_DIR": ".npu_cache",      # Enable model caching
                })
                
                self.acceleration_enabled = True
                print("✅ Intel NPU configured successfully!")
                return True
        except Exception as e:
            print(f"⚠️  OpenVINO NPU setup failed: {e}")
        
        return False
    
    def setup_onnx_runtime(self):
        """Setup ONNX Runtime with NPU/GPU acceleration"""
        try:
            import onnxruntime as ort
            
            providers = []
            
            # CUDA (NVIDIA)
            if self.device == "cuda":
                if "CUDAExecutionProvider" in ort.get_available_providers():
                    providers.append("CUDAExecutionProvider")
            
            # ROCm (AMD)
            elif self.device == "hip":
                if "ROCMExecutionProvider" in ort.get_available_providers():
                    providers.append("ROCMExecutionProvider")
            
            # Intel NPU
            elif self.device == "xpu":
                if "OpenVINOExecutionProvider" in ort.get_available_providers():
                    providers.append(("OpenVINOExecutionProvider", {"device_type": "NPU"}))
            
            # DirectML (Windows GPU fallback)
            if platform.system() == "Windows":
                if "DmlExecutionProvider" in ort.get_available_providers():
                    providers.append("DmlExecutionProvider")
            
            # CPU fallback
            providers.append("CPUExecutionProvider")
            
            print(f"🚀 ONNX Runtime providers: {providers}")
            self.acceleration_enabled = True
            return providers
            
        except Exception as e:
            print(f"⚠️  ONNX Runtime setup failed: {e}")
            return ["CPUExecutionProvider"]
    
    def optimize_for_speech_recognition(self):
        """Optimize hardware for speech recognition tasks"""
        if not self.acceleration_enabled:
            return {}
        
        print("🎤 Optimizing for speech recognition...")
        
        config = {
            "latency_mode": True,
            "streaming": True,
            "precision": "fp16" if self.device != "cpu" else "fp32",
            "cache_audio_features": True,
        }
        
        return config
    
    def optimize_for_llm_inference(self):
        """Optimize hardware for LLM inference"""
        if not self.acceleration_enabled:
            return {}
        
        print("🧠 Optimizing for LLM inference...")
        
        config = {
            "quantization": "int8" if self.npu_available else "fp16",
            "kv_cache_enabled": True,
            "batch_size": 4 if self.acceleration_enabled else 1,
            "use_flash_attention": self.device == "cuda",
        }
        
        return config
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get hardware performance statistics"""
        stats = {
            "device": self.device,
            "device_name": self.device_name,
            "npu_type": self.npu_type,
            "acceleration_enabled": self.acceleration_enabled,
            "cpu_count": os.cpu_count(),
        }
        
        # Add memory info
        try:
            import psutil
            mem = psutil.virtual_memory()
            stats["total_memory_gb"] = round(mem.total / (1024**3), 2)
            stats["available_memory_gb"] = round(mem.available / (1024**3), 2)
        except:
            pass
        
        # Add GPU memory if available
        if self.device == "cuda":
            try:
                import torch
                if torch.cuda.is_available():
                    stats["gpu_memory_gb"] = round(torch.cuda.get_device_properties(0).total_memory / (1024**3), 2)
            except:
                pass
        
        return stats
    
    def print_status(self):
        """Print hardware status and configuration"""
        print("\n" + "="*60)
        print("🔧 NPU Accelerator Status")
        print("="*60)
        
        stats = self.get_performance_stats()
        config = self.get_optimized_config()
        
        print(f"Device: {stats['device'].upper()}")
        print(f"NPU Type: {stats['npu_type']}")
        print(f"Acceleration: {'✅ Enabled' if stats['acceleration_enabled'] else '❌ Disabled'}")
        print(f"CPU Cores: {stats['cpu_count']}")
        
        if 'total_memory_gb' in stats:
            print(f"Total RAM: {stats['total_memory_gb']} GB")
            print(f"Available RAM: {stats['available_memory_gb']} GB")
        
        if 'gpu_memory_gb' in stats:
            print(f"GPU Memory: {stats['gpu_memory_gb']} GB")
        
        print(f"\nOptimizations:")
        print(f"  - Batch Size: {config['batch_size']}")
        print(f"  - FP16: {'✅' if config.get('use_fp16') else '❌'}")
        print(f"  - INT8: {'✅' if config.get('use_int8') else '❌'}")
        print(f"  - Cache: {'✅' if config.get('cache_enabled') else '❌'}")
        print(f"  - Optimization Level: {config.get('optimization_level', 'N/A')}")
        
        print("="*60 + "\n")


# Global NPU accelerator instance
npu_accelerator = NPUAccelerator()


def get_npu_config():
    """Get NPU configuration for use in other modules"""
    return npu_accelerator.get_optimized_config()


def is_npu_available():
    """Check if NPU is available"""
    return npu_accelerator.npu_available


def get_device():
    """Get optimal device (cuda/hip/xpu/mps/cpu)"""
    return npu_accelerator.device


def get_torch_device():
    """Get PyTorch device object"""
    return npu_accelerator.get_torch_device()
