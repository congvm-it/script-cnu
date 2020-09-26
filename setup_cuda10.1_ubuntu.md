# CUDA 10.1 on Ubuntu>=18.04

Author: CongVM

## Installations

1. Remove previous installed cuda

```bash
sudo rm /etc/apt/sources.list.d/cuda*
sudo apt remove --autoremove nvidia-cuda-toolkit
sudo apt remove --autoremove nvidia-*
```

2. Setup CUDA PPA 

```bash
sudo apt update
sudo add-apt-repository ppa:graphics-drivers
sudo apt-key adv --fetch-keys  http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/7fa2af80.pub
sudo bash -c 'echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda.list'
sudo bash -c 'echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64 /" > /etc/apt/sources.list.d/cuda_learn.list'
```

3. Install CUDA 10.1

```bash
sudo apt update
sudo apt install cuda-10-1
sudo apt install libcudnn7
```

4. Modify PATH, LD_LIBRARY_PATH in `.profile`

Open `~./profile`

```bash
sudo vi ~/.profile
```

Then add the following lines at the end of the file:

```bash
if [ -d "/usr/local/cuda-10.1/bin/" ]; then
    export PATH=/usr/local/cuda-10.1/bin${PATH:+:${PATH}}
    export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
fi
```

5. Restart your computer

6. Check your installed NVIDIA Driver

`nvcc  --version`

7. Check libcudnn

`/sbin/ldconfig -N -v $(sed ‘s/:/ /’ <<< $LD_LIBRARY_PATH) 2>/dev/null | grep libcudnn`

## Issues

I noticed that the `cuda-10-1` package does not have libcublas. To download this lib, you can access to `https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/` and download your required lib file. 

Besides, there are many libraries compiled as deb file in the above url. 

Tips:
Some libraries in cuda-10-1 require higher version than the libcublas you installed above.
So you cannot update and install using `apt` or `apt-get` anymore. Otherwise, if you install the new-higher version, pytorch and tensorflow cannot recognize GPU device.
To overcome this prob, a tip [2] you can try is remove nvidia repo. It works in my case.

```bash
sudo rm /etc/apt/sources.list.d/cuda.list
sudo apt-get clean
sudo apt-get update
sudo apt install -f
```

## Testing

To test whether tensorflow or torch recognizes GPU devices or not, you can use python script below.

Firstly, please install tensorflow-gpu and pytorch.
```
pip install tensorflow-gpu torch
```

then run this script.

```python
try:
    import tensorflow as tf
    print(f'Import tensorflow: {tf.__version__}')
    if tf.test.gpu_device_name(): 
        print('Default GPU Device: {}'.format(tf.test.gpu_device_name()))
    else:
	    print("Please install GPU version of TF")
except ImportError:
    print('Cannot import tensorflow!')

print('='*100)
try:
    import torch
    print(f"Import torch {torch.__version__}")
    print(f"Is torch recognizes GPU: {torch.cuda.is_available()}")
except ImportError:
    print('Cannot import torch!')
```


## References

[1] https://medium.com/@exesse/cuda-10-1-installation-on-ubuntu-18-04-lts-d04f89287130

[2] https://askubuntu.com/questions/1132090/i-am-not-able-to-install-anything-in-ubuntu

