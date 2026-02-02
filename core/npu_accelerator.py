"""
NPU Accelerator for JARVIS
Leverages Neural Processing Unit (NPU) on Omen PC for faster AI inference
Supports Intel NPU, AMD XDNA, and fallback to CPU/GPU
"""

import os
import sys
import platform
import subprocess
from typing import Optional, Dict, Any

class NPUAccelerator:
    """
    NPU Acceleration Manager for JARVIS
    Automatically detects and uses available NPU hardware
    """
    
    def __init__(self):
        self.npu_available = False
        self.npu_type = None
        self.device = "cpu"  # Default fallback
        self.acceleration_enabled = False
        
        # Detect NPU
        self._detect_npu()
        
    def _detect_npu(self):
        """Detect available NPU hardware"""
        print("🔍 Detecting NPU hardware...")
        
        # Check for Intel NPU (AI Boost)
        if self._check_intel_npu():
            self.npu_type = "Intel NPU"
            self.npu_available = True
            self.device = "npu"
            print(f"✅ Detected: {self.npu_type}")
            return
        
        # Check for AMD XDNA NPU
        if self._check_amd_npu():
            self.npu_type = "AMD XDNA NPU"
            self.npu_available = True
            self.device = "npu"
            print(f"✅ Detected: {self.npu_type}")
            return
        
        # Fallback to GPU if available
        if self._check_gpu():
            self.npu_type = "GPU (CUDA/DirectML)"
            self.device = "gpu"
            print(f"✅ Using GPU acceleration")
            return
        
        print("⚠️  No NPU detected. Using CPU.")
        self.device = "cpu"
    
    def _check_intel_npu(self) -> bool:
        """Check for Intel NPU (Core Ultra processors)"""
        try:
            # Check CPU info for Intel Core Ultra
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["wmic", "cpu", "get", "name"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                cpu_info = result.stdout.lower()
                
                # Intel Core Ultra has NPU
                if "core ultra" in cpu_info or "meteor lake" in cpu_info:
                    return True
                
                # Check for Intel AI Boost
                if "ai boost" in cpu_info:
                    return True
            
            # Check for OpenVINO NPU plugin
            try:
                import openvino as ov
                core = ov.Core()
                devices = core.available_devices
                if "NPU" in devices:
                    return True
            except:
                pass
                
        except Exception as e:
            print(f"Intel NPU check error: {e}")
        
        return False
    
    def _check_amd_npu(self) -> bool:
        """Check for AMD XDNA NPU (Ryzen AI)"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ["wmic", "cpu", "get", "name"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                cpu_info = result.stdout.lower()
                
                # AMD Ryzen AI has XDNA NPU
                if "ryzen ai" in cpu_info or "7040" in cpu_info or "8040" in cpu_info:
                    return True
            
            # Check for AMD NPU driver
            try:
                import onnxruntime as ort
                providers = ort.get_available_providers()
                if "VitisAIExecutionProvider" in providers:
                    return True
            except:
                pass
                
        except Exception as e:
            print(f"AMD NPU check error: {e}")
        
        return False
    
    def _check_gpu(self) -> bool:
        """Check for GPU (CUDA or DirectML)"""
        try:
            # Check NVIDIA GPU
            try:
                import torch
                if torch.cuda.is_available():
                    return True
            except:
                pass
            
            # Check DirectML (Windows GPU)
            if platform.system() == "Windows":
                try:
                    import onnxruntime as ort
                    if "DmlExecutionProvider" in ort.get_available_providers():
                        return True
                except:
                    pass
        except:
            pass
        
        return False
    
    def get_optimized_config(self) -> Dict[str, Any]:
        """Get optimized configuration for current hardware"""
        config = {
            "device": self.device,
            "npu_available": self.npu_available,
            "npu_type": self.npu_type,
            "batch_size": 1,
            "num_threads": os.cpu_count() or 4,
        }
        
        if self.npu_available:
            # NPU optimizations
            config.update({
                "use_fp16": True,  # NPU works best with FP16
                "use_int8": True,  # NPU supports INT8 quantization
                "batch_size": 4,   # NPU can handle larger batches
                "cache_enabled": True,
                "optimization_level": "aggressive",
            })
        elif self.device == "gpu":
            # GPU optimizations
            config.update({
                "use_fp16": True,
                "batch_size": 8,
                "cache_enabled": True,
                "optimization_level": "balanced",
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
            
            if self.npu_available:
                # Try NPU providers
                if self.npu_type == "AMD XDNA NPU":
                    providers.append("VitisAIExecutionProvider")
                
                # Intel NPU via OpenVINO
                if "OpenVINOExecutionProvider" in ort.get_available_providers():
                    providers.append(("OpenVINOExecutionProvider", {"device_type": "NPU"}))
            
            # GPU fallback
            if self.device == "gpu":
                available = ort.get_available_providers()
                if "CUDAExecutionProvider" in available:
                    providers.append("CUDAExecutionProvider")
                elif "DmlExecutionProvider" in available:
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
        """Optimize NPU for speech recognition tasks"""
        if not self.npu_available:
            return
        
        print("🎤 Optimizing NPU for speech recognition...")
        
        # Speech recognition benefits from:
        # - Low latency
        # - Continuous processing
        # - FP16 precision
        
        config = {
            "latency_mode": True,
            "streaming": True,
            "precision": "fp16",
            "cache_audio_features": True,
        }
        
        return config
    
    def optimize_for_llm_inference(self):
        """Optimize NPU for LLM inference"""
        if not self.npu_available:
            return
        
        print("🧠 Optimizing NPU for LLM inference...")
        
        # LLM inference benefits from:
        # - INT8 quantization
        # - KV cache
        # - Batch processing
        
        config = {
            "quantization": "int8",
            "kv_cache_enabled": True,
            "batch_size": 4,
            "use_flash_attention": True,
        }
        
        return config
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get NPU performance statistics"""
        stats = {
            "device": self.device,
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
        
        return stats
    
    def print_status(self):
        """Print NPU status and configuration"""
        print("\n" + "="*60)
        print("🔧 NPU Accelerator Status")
        print("="*60)
        
        stats = self.get_performance_stats()
        config = self.get_optimized_config()
        
        print(f"Device: {stats['device'].upper()}")
        if stats['npu_type']:
            print(f"NPU Type: {stats['npu_type']}")
        print(f"Acceleration: {'✅ Enabled' if stats['acceleration_enabled'] else '❌ Disabled'}")
        print(f"CPU Cores: {stats['cpu_count']}")
        
        if 'total_memory_gb' in stats:
            print(f"Total RAM: {stats['total_memory_gb']} GB")
            print(f"Available RAM: {stats['available_memory_gb']} GB")
        
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
    """Get optimal device (npu/gpu/cpu)"""
    return npu_accelerator.device
