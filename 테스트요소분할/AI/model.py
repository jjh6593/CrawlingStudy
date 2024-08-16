import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import random
import re
import pickle
import pandas as pd
from torch.optim.lr_scheduler import StepLR


#하이퍼 파라미터
hidden_size = 256
PAD_token = 0
SOS_token = 1
EOS_token = 2
UNK_token = 3
MAX_LENGTH = 300
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def clean_text(text):
    if pd.isna(text):  # NaN값을 처리
        return ''
    text = text.lower()
    text = re.sub(r'\d+', ' ', text)   #숫자를 공백으로
    text = re.sub(r'([^\w\s])', r' \1 ', text)   # 마침표 앞 뒤로 공백 추가
    text = re.sub(r'\s+', ' ', text)  # 두개 이상의 공백은 하나의 공백으로..
    text = text.strip()  # 텍스트 앞 뒤의 공백 제거
    return text