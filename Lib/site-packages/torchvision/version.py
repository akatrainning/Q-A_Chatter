__version__ = '0.21.0+cpu'
git_version = '7af698794eded568735f9519593603c1ec889eba'
from torchvision.extension import _check_cuda_version
if _check_cuda_version() > 0:
    cuda = _check_cuda_version()
