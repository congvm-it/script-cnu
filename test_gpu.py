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

