# One-Click Web-Based 3D Reconstruction: A System for Interactive and Measurable 3D Scenes Using Gaussian Splatting
Click the link to watch the video. https://easylink.cc/o8052c

## 3D Reconstruction
### Installation
1. Clone InstantSplat and download pre-trained model.
```bash
git clone https://github.com/xubin123xubin/From-Photos-to-Measurable-3D-Worlds.git
cd public
git clone --recursive https://github.com/NVlabs/InstantSplat.git
cd InstantSplat
mkdir -p mast3r/checkpoints/
wget https://download.europe.naverlabs.com/ComputerVision/MASt3R/MASt3R_ViTLarge_BaseDecoder_512_catmlpdpt_metric.pth -P mast3r/checkpoints/
```

2. Create the environment, here we show an example using conda.
```bash
conda create -n instantsplat python=3.10.13 cmake=3.14.0 -y
conda activate instantsplat
conda install pytorch torchvision pytorch-cuda=12.1 -c pytorch -c nvidia  # use the correct version of cuda for your system
pip install -r requirements.txt
pip install submodules/simple-knn
pip install submodules/diff-gaussian-rasterization
pip install submodules/fused-ssim
```

### Usage
1. Data preparation (download our pre-processed data from: [Hugging Face](https://huggingface.co/datasets/kairunwen/InstantSplat) or [Google Drive](https://drive.google.com/file/d/1Z17tIgufz7-eZ-W0md_jUlxq89CD1e5s/view))
```bash
  cd <data_path>
  # then do whatever data preparation
```

2. Command
```bash
  # Train and output video using the following command.
  # Users can place their data in the 'assets/examples/<scene_name>/images' folder and run the following command directly.
  bash scripts/run_infer.sh

  # Train and evaluate using the following command.
  bash scripts/run_eval.sh
```

## 3D Visualization
### Installation
```bash
npm install @reall3d/reall3dviewer
```

### Usage
```bash
npm run dev
```

## Others
**If you have any concerns or questions, please contact us at xubin@stu.sau.edu.cn**

If the paper is fortunate enough to be accepted, we will optimize the code into a more mature and stable version.

## Acknowledgments
We are deeply grateful to the following projects for their invaluable reference implementations.

- [Reall3dViewer](https://github.com/reall3d-com/Reall3dViewer)
- [gsbox](https://github.com/gotoeasy/gsbox)
- [InstantSplat: Sparse-view Gaussian Splatting in Seconds](https://github.com/NVlabs/InstantSplat)
