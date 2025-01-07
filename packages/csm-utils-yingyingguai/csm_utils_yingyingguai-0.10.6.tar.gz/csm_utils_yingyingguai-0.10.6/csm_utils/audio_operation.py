from itertools import count
from mutagen.mp3 import MP3
import os
from pydub.utils import mediainfo
from pydub import AudioSegment
import time
import io
import threading
from pydub.playback import play
import tempfile
tempfiledir='./tempfile'
os.path.exists(tempfiledir) or os.makedirs(tempfiledir)
tempfile.tempdir=tempfiledir
from csm_utils.file_utils import get_file_info
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from pydub import AudioSegment
from icecream import ic

'''
功能点：
1.加载MP3、wav、pcm时全保存为pcm格式
支持从路径加载、从pcm列表数据加载
2.可导出MP3、wav、pcm格式
导出可选择保存为文件，或者保存到字节流中，
3.支持重采样
4.支持按帧、时间切分音频
5.支持生成随机噪音
6.支持绘制音频波形图、频谱图、声纹图
支持计算vad、LUFS

'''

class CustomAudioOpt():
    def __init__(self, audio_file_path,sr=None,sampe_width=None,channels=None):
        file_info=get_file_info(audio_file_path)
        file_suffix=file_info['file_suffix']
        self.file_path = audio_file_path
        if file_suffix in ['.mp3', '.wav', '.flac', '.ogg', '.aac']:
            self.audio = AudioSegment.from_file(self.file_path)
            self.pcm_data=self.audio.get_array_of_samples()
            self.sr=self.audio.frame_rate
            print(f"Audio loaded successfully from {self.file_path}")
        elif file_suffix=='.pcm':
            self.pcm_data=np.fromfile(audio_file_path,dtype=np.int16)
            self.audio=AudioSegment(self.pcm_data,sample_width=sampe_width,frame_rate=sr,channels=channels)
            self.sr=sr
            print(f"Audio loaded successfully from {self.file_path}")
        else:
            raise ValueError(f"Unsupported file type: {file_suffix}")
    
    def resampe_sr(self,target_sr,setin=True):
        if target_sr<8000:
            print('target_sr should be greater or equal than 8000')
            return self.pcm_data
        origin_len=len(self.pcm_data)
        target_len=int(origin_len*target_sr/self.sr)
        target_pcm_data=np.interp(np.linspace(0,origin_len-1,target_len),np.arange(origin_len),self.pcm_data)
        # target_pcm_data=np.array(target_pcm_data,dtype=np.int16)
        target_pcm_data = target_pcm_data / np.max(np.abs(target_pcm_data)) * 32767  # 归一化
        target_pcm_data = np.clip(target_pcm_data, -32768, 32767)  # 限制范围
        target_pcm_data = np.array(target_pcm_data, dtype=np.int16)
        if setin:
            self.pcm_data=target_pcm_data
            ic(self.audio.sample_width,target_sr,self.audio.channels)
            self.audio=AudioSegment(target_pcm_data.tobytes(),sample_width=2,frame_rate=target_sr,channels=1)
            self.sr=target_sr
        return target_pcm_data
            
    def load_audio(self,audio_file_path,sr=None,sampe_width=None,channels=None):
        self.__init__(audio_file_path,sr,sampe_width,channels)
        pass
    
    def show_info(self):
        detailed_info = mediainfo(self.file_path)
        print("\nDetailed Info:")
        for key, value in detailed_info.items():
            print(f"{key}: {value}")
            
    def convert2(self,output_path,target_foramt='wav'):
        try:
            if target_foramt=='wav':
                self.audio.export(output_path, format="wav", 
                   parameters=["-ar", str(self.sr), 
                               "-ac", str(self.audio.channels)])
            elif target_foramt=='pcm':
                with open(output_path, 'wb') as f:
                    f.write(self.pcm_data.tobytes())
            elif target_foramt=='mp3':
                self.audio.export(output_path, format="mp3",codec="libmp3lame")
            else:
                raise ValueError(f"Unsupported file type: {target_foramt}")
            print(f"Audio converted and saved to {output_path}")
        except Exception as e:
            print(f"Error during conversion: {e}")
            
    def play_audio(self):
        # play(self.audio)#需修改NamedTemporaryFile("w+b", suffix=".wav",delete=False) 
        threading.Thread(target=play, args=(self.audio,), daemon=True).start()
        
    def plot_audio_and_mel(self):
        from librosa.feature import melspectrogram
        from librosa.display import specshow
        import librosa
        raw_data = np.array(self.pcm_data)
        frame_rate = self.audio.frame_rate
        duration = len(raw_data) / frame_rate
        
        # Plot the raw waveform
        plt.figure(figsize=(12, 6))
        plt.subplot(2, 1, 1)
        time = np.linspace(0, duration, num=len(raw_data))
        plt.plot(time, raw_data)
        plt.title("Raw Waveform")
        plt.xlabel("Time (s)")
        plt.ylabel("Amplitude")

        # Convert AudioSegment to NumPy array and calculate Mel spectrogram
        samples = raw_data.astype(np.float32) / (2 ** (self.audio.sample_width * 8 - 1))  # Normalize PCM data
        mel_spect = melspectrogram(y=samples, sr=frame_rate, n_fft=2048, hop_length=512, n_mels=128)

        # Plot the Mel spectrogram
        plt.subplot(2, 1, 2)
        specshow(librosa.power_to_db(mel_spect, ref=np.max), sr=frame_rate, hop_length=512, x_axis='time', y_axis='mel')
        plt.title("Mel Spectrogram")
        plt.colorbar(format='%+2.0f dB')
        plt.tight_layout()
        plt.show()
            
if __name__=='__main__':
    mp3path=r'E:\高频常用函数\csm_utils\data\audio\mp3\music\file_example_MP3_700KB.mp3'
    wavpath=r'E:\高频常用函数\csm_utils\data\audio\wav\human\taunt.wav'
    convert_file_path=r'E:\高频常用函数\csm_utils\data\audio\wav\human\taunt1.mp3'
    test=CustomAudioOpt(wavpath)
    test.plot_audio_and_mel()
    test.resampe_sr(8000)
    test.plot_audio_and_mel()
    test.convert2(convert_file_path,'mp3')
    test.load_audio(convert_file_path)
    test.plot_audio_and_mel()
    test.play_audio()
    time.sleep(5)
    # test.show_info()



