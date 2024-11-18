import os
import torch
from pathlib import Path
from setuptools import setup, find_packages

AUTOAWQ_VERSION = "0.2.7.post1"
INSTALL_KERNELS = os.getenv("INSTALL_KERNELS", "0") == "1"
IS_CPU_ONLY = not torch.backends.mps.is_available() and not torch.cuda.is_available()
TORCH_VERSION = str(os.getenv("TORCH_VERSION", None) or torch.__version__).split('+', maxsplit=1)[0]

CUDA_VERSION = os.getenv("CUDA_VERSION", None) or torch.version.cuda
if CUDA_VERSION:
    CUDA_VERSION = "".join(CUDA_VERSION.split("."))[:3]

common_setup_kwargs = {
    "version": AUTOAWQ_VERSION,
    "name": "autoawq",
    "author": "Casper Hansen",
    "license": "MIT",
    "python_requires": ">=3.8.0",
    "description": "AutoAWQ implements the AWQ algorithm for 4-bit quantization with a 2x speedup during inference.",
    "long_description": (Path(__file__).parent / "README.md").read_text(
        encoding="UTF-8"
    ),
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/casper-hansen/AutoAWQ",
    "keywords": ["awq", "autoawq", "quantization", "transformers"],
    "platforms": ["linux", "windows"],
    "classifiers": [
        "Environment :: GPU :: NVIDIA CUDA :: 11.8",
        "Environment :: GPU :: NVIDIA CUDA :: 12",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: C++",
    ],
}

requirements = [
    f"torch>={TORCH_VERSION}",
    "triton",
    "transformers>=4.35.0",
    "tokenizers>=0.12.1",
    "typing_extensions>=4.8.0",
    "accelerate",
    "datasets>=2.20",
    "zstandard",
]

try:
    import awq_ext

    KERNELS_INSTALLED = True
except ImportError:
    KERNELS_INSTALLED = False

if not KERNELS_INSTALLED and CUDA_VERSION and INSTALL_KERNELS and CUDA_VERSION.startswith("12"):
    requirements.append("autoawq-kernels")

elif IS_CPU_ONLY:
    requirements.append("intel-extension-for-pytorch>=2.4.0")

setup(
    packages=find_packages(),
    install_requires=requirements,
    extras_require={
        "eval": ["lm_eval==0.4.1", "tabulate", "protobuf", "evaluate", "scipy"],
        "dev": ["black", "mkdocstrings-python", "mkdocs-material", "griffe-typingdoc"],
    },
    **common_setup_kwargs,
)
