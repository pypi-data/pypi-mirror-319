import torch
import soundfile as sf
from transformers import AutoConfig

from  modeling_xcodec2 import XCodec2Model

model_path = "/data/zheny/xcodec2"  # 这是你在 huggingface 上的仓库名

model = XCodec2Model.from_pretrained(model_path)
model.eval().cuda()

# 准备一段音频
wav, sr = sf.read("test.flac")
wav_tensor = torch.from_numpy(wav).float().unsqueeze(0)  # [1, time]

with torch.no_grad():
    vq_code = model.encode_code(input_waveform=wav_tensor )
    print(vq_code)
    recon_wav = model.decode_code(vq_code).cpu()

sf.write("reconstructed.wav", recon_wav[0,0,:].numpy(), sr)
