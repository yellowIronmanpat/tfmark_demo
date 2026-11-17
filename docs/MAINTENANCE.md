# TFMark Demo 维护说明

网站：<https://yellowironmanpat.github.io/tfmark_demo/>  
仓库：<https://github.com/yellowIronmanpat/tfmark_demo>

## 修改哪个文件

| 修改内容 | 文件 |
| --- | --- |
| 标题、作者、摘要、图注、页面说明 | `index.html` |
| 字体、间距、表格和手机适配 | `assets/css/style.css` |
| 播放互斥和加载失败提示 | `assets/js/player.js` |
| 架构图 | `assets/images/architecture.png` 与 `assets/pdf/architecture.pdf` |
| 音频 | `audio/Original/`、`audio/AudioSeal/`、`audio/TimbreWatermark/`、`audio/WavMark/`、`audio/TFMark/` |
| 样本顺序、转写和路径 | `samples.json`，同时修改 `index.html` 对应行 |
| 音频与图片的文件校验和 | `asset-manifest.json` |

## 本地检查

在仓库根目录运行：

```sh
python3 scripts/validate.py
node scripts/check-player.cjs
python3 -m http.server 8000 --bind 127.0.0.1
```

浏览器打开 <http://localhost:8000/>。手机宽度下，音频表格可横向滑动。每格的 WAV 链接可直接打开对应文件；浏览器无法播放时也可用该链接获取音频。

## 更新音频或架构图

1. 按完整的 `sample_id` 配对，不按文件排列顺序配对；同一行的五种方法必须对应同一句话。
2. 更新文件、`samples.json` 和 HTML 中的路径、转写、时长、样本标签。继续使用相对路径，不要加以 `/` 开头的站点根路径。
3. 如果确实更换了音频或图，先核对新文件来源，再更新 `asset-manifest.json` 中对应文件的 SHA-256。可运行 `shasum -a 256 文件路径` 获取新值；不要为了让检查通过而直接覆盖全部旧校验和。
4. 运行两项本地检查，通过后提交到 `main`。
5. 在 GitHub 的 Actions 页面确认 **Validate demo** 和 **pages build and deployment** 成功。Validate demo 会等待当前首页发布，再检查所有线上资源；也可在 Actions → Validate demo → Run workflow 中选择 `main` 手动复查。

论文摘要和作者信息以当前 manuscript 为准。更新架构图时同时替换 PNG 展示图和真正的矢量 PDF。样例文件与总体实验指标是两种证据，不要把历史指标当作这些重新导出文件的实测值。

## 发布设置

Settings → Pages → Deploy from a branch → `main` → `/(root)`。仓库根目录应保留 `index.html` 和 `.nojekyll`。这个网站不需要 npm、构建产物目录、自定义域名或服务器。

## 常见问题

| 现象 | 检查方法 |
| --- | --- |
| 页面仍是旧版本 | 先检查 Pages 部署是否完成，再刷新；确认提交在 `main` |
| 单个音频打不开 | 检查大小写、方法目录、样本编号和文件路径；查看播放器下方 WAV 链接 |
| 表格在手机上显示不全 | 在表格区域横向滑动，五种方法会继续保留在同一行 |
| SHA-256 检查失败 | 确认文件是否被转码、归一化、截断或错误替换；先查原因再更新清单 |
| 线上检查暂时失败 | 检查 Pages 状态和网络；该检查下载全部资源并与当前提交逐字节比较 |

校验脚本检查文件和程序行为，不代替人工试听、视觉验收或水印解码实验。原始实验路径、模型 checkpoint、消息内容和导出日志不要上传到此公开仓库。
