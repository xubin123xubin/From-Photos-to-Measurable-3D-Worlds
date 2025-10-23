import fs from 'fs';
import multer from 'multer';
import { exec } from 'child_process';
import express from 'express';
import cors from 'cors';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';


/* ========= 三维重建接口：/run-reconstruction ========= */
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(cors());
app.use(express.json());

app.get('/run-reconstruction', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  res.flushHeaders();

  const scriptPath = path.resolve(__dirname, 'public/InstantSplat/scripts/run_infer.sh');
  const child = spawn('bash', [scriptPath]);

  child.stdout.on('data', chunk => {
    chunk.toString().split('\n').forEach(line => {
      if (line.trim()) res.write(`data: ${line}\n\n`);
    });
  });

  child.stderr.on('data', chunk => {
    chunk.toString().split('\n').forEach(line => {
      if (line.trim()) res.write(`data: [ERR] ${line}\n\n`);
    });
  });

  // ===== 脚本真正完成后才触发 =====
  child.on('close', code => {
    res.write(`data: [DONE] exit code ${code}\n\n`);
    res.write('event: close\ndata: 1\n\n'); // 自定义结束事件
    res.end();
  });

  req.on('close', () => child.kill());
});

app.listen(8081, () => {
  console.log('✅ 后端服务已启动：http://localhost:8081');
});


/* ========= 文件上传接口：/upload-images ========= */
const uploadDir = path.resolve('public/InstantSplat/assets/sora/Art/images');

/* ---------- 清空目录工具 ---------- */
function emptyDir(dir) {
  if (!fs.existsSync(dir)) return;
  fs.rmSync(dir, { recursive: true, force: true });
  fs.mkdirSync(dir, { recursive: true });
}

/* ---------- multer 配置 ---------- */
const storage = multer.diskStorage({
  destination: (req, file, cb) => cb(null, uploadDir),
  filename: (req, file, cb) => {
    const ext = path.extname(file.originalname);
    // 按顺序 0.ext, 1.ext ...
    cb(null, `${req.files.length}${ext}`);
  }
});

/* ---------- 在 multer 之前清空目录 ---------- */
const upload = (() => {
  const u = multer({ storage });
  return (req, res, next) => {
    emptyDir(uploadDir); // 整批开始前清空一次
    u.array('images')(req, res, next);
  };
})();

/* ---------- 上传接口 ---------- */
app.post('/upload-images', upload, (req, res) => {
  if (!req.files || req.files.length === 0) {
    return res.status(400).json({ error: '未收到文件' });
  }
  const names = req.files.map(f => f.filename);
  console.log('[UPLOAD]', names);
  res.json({ success: true, files: names });
});


/* ========= 文件下载接口：/download-model ========= */
app.get('/download-model', (_req, res) => {
  // 注意：改成你实际的绝对/相对路径
  const filePath = path.resolve('public/InstantSplat/assets/output_infer/sora/Art/point_cloud/iteration_1000/point_cloud.ply');

  if (!fs.existsSync(filePath)) {
    return res.status(404).json({ error: '文件不存在' });
  }

  res.download(filePath, 'result.ply'); // 触发浏览器下载
});