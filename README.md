# One-Click Web-Based 3D Reconstruction: A System for Interactive and Measurable 3D Scenes Using Gaussian Splatting
Computer vision research focuses on restoring the 3D structure of objects or scenes from images, with 3D reconstruction technology becoming indispensable in fields such as medicine, robotics, and digital twins. Traditional methods rely on extensive image sets and precomputed camera poses, limiting practical applications. This paper introduces a novel web-based, one-click system for large-scale 3D Gaussian Splatting reconstruction and visualization, eliminating the need for pre-acquired camera pose information. The system supports arbitrary image resolutions, camera parameters, and shooting angles, significantly lowering technical barriers. Employing the InstantSplat algorithm, it achieves rapid sparse view reconstruction and introduces the SPX model file format for optimized network transmission. Experimental results demonstrate the system's capability to rapidly reconstruct diverse real-world scenarios with high visual fidelity and measurement accuracy, marking a significant step towards zero-barrier, low-cost, scalable web-based 3D reconstruction and visualization technology. Our code and demos are available at https://github.com/xubin123xubin/From-Photos-to-Measurable-3D-Worlds.
### Click the link to watch the video. https://easylink.cc/o8052c

## 3D Reconstruction
### Installation
1. Clone project and download pre-trained model.
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

## Citation
If you find our work beneficial in your research, please consider citing this paper. Please note that this paper is currently under review at The Visual Computers journal. The formal citation format will be provided upon acceptance.
