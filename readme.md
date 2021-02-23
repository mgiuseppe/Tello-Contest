# Tello contest

## Introduction

This is my entry for the tello contest

## Project Description

This repo contains a bunch of samples

- **First_Steps**

Move Tello using DJITelloPy. 

- **Sport**

Get commands from keyboard 

## Environmental configuration

1. Create a conda environment (optional)
    ```
    > conda create -n tello python=3.9
    > conda activate tello
    ```
2. Install the requirements using pip
    ```
    > pip install -r requirements.txt
    ```
3. Create inbound firewall rules for UDP ports 8890 (state) and 11111 (video)
4. Run the samples
    ```
    > cd First_Steps
    > python main.py
    ```

## Tools

- [vs code](https://code.visualstudio.com/)
- [vs code python extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python)
- [miniconda3](https://docs.conda.io/en/latest/miniconda.html)

## Sources

- [Tello Manual](https://dl-cdn.ryzerobotics.com/downloads/Tello/20180404/Tello_User_Manual_V1.2_EN.pdf)
- [Tello SDK doc](https://dl-cdn.ryzerobotics.com/downloads/tello/20180910/Tello%20SDK%20Documentation%20EN_1.3.pdf)
- [Tello SDK samples](https://github.com/dji-sdk/Tello-Python)
- [Tello SDK wrapper](https://github.com/damiafuentes/DJITelloPy)
- [OpenCV Tutorial](https://www.youtube.com/watch?v=WQeoO7MI0Bs)