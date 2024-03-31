# 环境配置只需 pip install -U funasr modelscope

from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

inference_pipeline = pipeline(
    task=Tasks.emotion_recognition,
    model="iic/emotion2vec_base_finetuned")

rec_result = inference_pipeline('../static/example_wav/anger.wav', granularity="utterance", extract_embedding=False)
print(rec_result)
