# 循环测试cuda和cpu的速度

# In[ ]:
import torch
import time

def test_cuda_speed(devicestr : str):
    device = torch.device(devicestr)
    x = torch.randn(1000, 1000)
    y = torch.randn(1000, 1000)
    start = time.time()
    for _ in range(10000):
        z = torch.matmul(x, y)
    print(f"{device} time: {time.time() - start}")

if __name__ == "__main__":
    devicestr = "cuda" if torch.cuda.is_available() else "cpu"
    if devicestr == "cuda":
        print("cuda is available")
        test_cuda_speed(devicestr)
        test_cuda_speed("cpu")
    else:
        print("cuda is not available")



