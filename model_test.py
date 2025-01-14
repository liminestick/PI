# Импортируем необходимые библиотеки
import os
import torch
import torchaudio

from TTS.tts.configs.xtts_config import XttsConfig  # Для загрузки конфигурации модели XTTS
from TTS.tts.models.xtts import Xtts  # Для загрузки самой модели XTTS
from omogre import Transcriptor  # Для преобразования текста в транскрипт

# Директория, где будет храниться модель
model_dir = 'model'

# Функция для очистки кэша GPU, если CUDA доступна
def clear_gpu_cache():
    """Clear the GPU cache if CUDA is available."""
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

XTTS_MODEL = None  # Переменная для хранения модели XTTS

# Функция для загрузки модели XTTS
def load_model(xtts_model_path='model'):
    """
    Загружает модель XTTS с заданного пути.

    Параметры:
    - xtts_model_path (str): Путь к директории с моделью XTTS.
    """
    global XTTS_MODEL  # Объявляем переменную как глобальную
    clear_gpu_cache()  # Очищаем кэш GPU перед загрузкой модели

    # Проверяем, что путь к модели задан
    assert xtts_model_path, "Model path must be provided."

    # Указываем пути к контрольным точкам и конфигурационным файлам модели
    xtts_checkpoint = os.path.join(xtts_model_path, "model.pth")  # Путь к файлу контрольной точки
    xtts_config = os.path.join(xtts_model_path, "config.json")  # Путь к конфигурационному файлу
    xtts_vocab = os.path.join(xtts_model_path, "vocab.json")  # Путь к файлу с вокабуляром

    # Загружаем конфигурацию модели из JSON-файла
    config = XttsConfig()
    config.load_json(xtts_config)  # Загружаем конфигурацию модели из файла
    XTTS_MODEL = Xtts.init_from_config(config)  # Инициализируем модель на основе конфигурации

    # Выводим сообщение о начале и завершении инициализации модели
    print("XTTS initialization ...")
    XTTS_MODEL.load_checkpoint(config, checkpoint_path=xtts_checkpoint,
                               vocab_path=xtts_vocab, use_deepspeed=False, speaker_file_path='-')  # Загружаем веса модели
    if torch.cuda.is_available():
        XTTS_MODEL.cuda()  # Если доступен GPU, переносим модель на GPU
    print(" ... done")

# Класс для выполнения инференса с использованием модели XTTS
class XttsInference:
    def __init__(self, transcriptor_data_path='omogre_data', xtts_model_path='model', reference_audio=None):
        """
        Инициализирует транскриптор и загружает модель XTTS.

        Параметры:
        - transcriptor_data_path (str): Путь для загрузки данных транскриптора.
        - xtts_model_path (str): Путь к директории с моделью XTTS.
        - reference_audio (str, optional): Путь к аудиофайлу для извлечения латентов. Если None, используется стандартный файл.
        """
        clear_gpu_cache()  # Очистка кэша GPU
        self.transcriptor = Transcriptor(data_path=transcriptor_data_path)  # Инициализация транскриптора
        load_model(xtts_model_path=xtts_model_path)  # Загружаем модель XTTS

        # Если пользователь не передал свой файл, используем стандартный reference_audio
        self.reference_audio = reference_audio or os.path.join(xtts_model_path, "reference_audio.wav")

        # Извлекаем латентные векторы для последующего использования в генерации речи
        self.gpt_cond_latent, self.speaker_embedding = XTTS_MODEL.get_conditioning_latents(
            audio_path=self.reference_audio,  # Используем переданный или стандартный файл
            gpt_cond_len=XTTS_MODEL.config.gpt_cond_len,
            max_ref_length=XTTS_MODEL.config.max_ref_len,
            sound_norm_refs=XTTS_MODEL.config.sound_norm_refs
        )

    def __call__(self, src_text):
        """
        Генерирует синтезированную речь из исходного текста.

        Параметры:
        - src_text (str): Текст, который нужно синтезировать в речь.

        Возвращает:
        - tuple: Текст и аудио в виде тензора.
        """
        # Транскрибируем входной текст с использованием транскриптора
        tts_text = ' '.join(self.transcriptor([src_text]))

        # Генерируем речь с помощью модели XTTS
        out = XTTS_MODEL.inference(
            text=tts_text,
            language='ru',  # Указываем язык, на котором будет генерироваться речь
            gpt_cond_latent=self.gpt_cond_latent,  # Условие для генерации
            speaker_embedding=self.speaker_embedding,  # Эмбеддинг голоса
            temperature=XTTS_MODEL.config.temperature,  # Температура (контролирует разнообразие)
            length_penalty=XTTS_MODEL.config.length_penalty,  # Штраф за длину
            repetition_penalty=XTTS_MODEL.config.repetition_penalty,  # Штраф за повторы
            top_k=XTTS_MODEL.config.top_k,  # Количество наиболее вероятных токенов
            top_p=XTTS_MODEL.config.top_p,  # Параметр для Nucleus sampling
        )

        # Преобразуем полученное аудио в тензор
        audio = torch.tensor(out["wav"]).unsqueeze(0)
        return tts_text, audio  # Возвращаем транскрибированный текст и аудио

# Инициализируем класс для инференса
xtts_inference = XttsInference()

# Пример текста для синтеза речи
src_text = 'Пролетело веселое лето. Вот и наступила осень. Пришла пора убирать урожай. Ваня и Федя копают картофель.'
output_file = 'audio.wav'  # Имя выходного файла для аудио

# Генерация аудио для данного текста
tts_text, audio = xtts_inference(src_text)
print('transcription:', tts_text)  # Выводим транскрибированный текст

# Сохраняем аудиофайл на диск
torchaudio.save(output_file, audio, sample_rate=24000)  # Сохраняем аудио с частотой дискретизации 24000 Гц

print('output_file:', output_file)  # Выводим путь к файлу с результатом
