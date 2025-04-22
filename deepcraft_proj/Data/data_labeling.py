import os
import wave
import contextlib
import shutil
import numpy as np
from pydub import AudioSegment, silence


SubName1 = ['01_A', '02_Ba', '03_Ta', '04_Tsa', '05_Ja', '06_Hha', '07_Kha', '08_Da', '09_Dza', '10_Ro', '11_Za', '12_Sa', '13_Sya',
            '14_Sho', '15_Dho', '16_Tho', '17_Zho', '18_Ain', '19_Gho', '20_Fa', '21_Qo', '22_Ka', '23_La', '24_Ma', '25_Na', '26_Ha', '27_Wa', '28_Ya']
SubName2 = ['A_Pup', 'Ba_Pup', 'Ta_Pup', 'Tsa_Pup', 'Ja_Pup', 'Hha_Pup', 'Kha_Pup', 'Da_Pup', 'Dza_Pup', 'Ro_Pup', 'Za_Pup', 'Sa_Pup', 'Sya_Pup',
            'Sho_Pup', 'Dho_Pup', 'Tho_Pup', 'Zho_Pup', 'Ain_Pup', 'Gho_Pup', 'Fa_Pup', 'Qo_Pup', 'Ka_Pup', 'La_Pup', 'Ma_Pup', 'Na_Pup', 'Ha_Pup', 'Wa_Pup', 'Ya_Pup']


def convert_to_mono(wav_path):
    audio = AudioSegment.from_wav(wav_path)
    if audio.channels > 1:
        audio = audio.set_channels(1)
        audio.export(wav_path, format='wav')
        # print(f"Converted to mono: {wav_path}")


def get_wav_duration(wav_path):
    with contextlib.closing(wave.open(wav_path, 'r')) as f:
        frames = f.getnframes()
        rate = f.getframerate()
        channels = f.getnchannels()
        duration = frames / float(rate)
        channel_type = 'Mono' if channels == 1 else 'Stereo'
        return duration, channel_type


def analyze_wav(wav_path, silence_thresh_db=-35, min_silence_len_ms=400):
    audio = AudioSegment.from_wav(wav_path)
    total_duration = len(audio) / 1000.0
    channels = audio.channels
    channel_type = 'Mono' if channels == 1 else 'Stereo'

    # Detect silent ranges
    silent_ranges = silence.detect_silence(
        audio,
        min_silence_len=min_silence_len_ms,
        silence_thresh=silence_thresh_db
    )
    silent_ranges = [(start / 1000.0, end / 1000.0)
                     for start, end in silent_ranges]

    # Invert silent ranges to get sound range
    sound_ranges = []
    prev_end = 0.0
    for start, end in silent_ranges:
        if start > prev_end:
            sound_ranges.append((prev_end, start))
        prev_end = end
    if prev_end < total_duration:
        sound_ranges.append((prev_end, total_duration))

    if len(sound_ranges) == 0:  # No sound detected
        return total_duration, 0.0, total_duration, channel_type

    # We assume there's only one sound region
    sound_start, sound_end = sound_ranges[0]

    # Results
    print(
        f"total_duration: {total_duration}\nsound_start:{sound_start}")
    print(
        f"sound_duration: {sound_end-sound_start}\nchannel_type:{channel_type}\n")
    return total_duration, sound_start, sound_end-sound_start, channel_type


def create_txt_for_each_wav(directory, Name1, Name2):
    prefix = 0
    # Loop through all files in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.wav'):
            old_filename = f"{prefix}"
            new_filename = Name1 + old_filename + '_Pup.wav'
            prefix = prefix + 1

            new_path = os.path.join(directory, new_filename)
            os.rename(os.path.join(directory, filename), new_path)
            _, wav_start, wav_duration, wave_type = analyze_wav(
                os.path.join(directory, new_filename))

            # Convert to mono if needed
            if wave_type == 'Stereo':
                convert_to_mono(new_path)

            label_filename = f"{new_filename}.label"
            label_path = os.path.join(directory, label_filename)
            wav_path = os.path.join(directory, new_filename)

            # Create a new text file (empty or with custom content)
            with open(label_path, 'w') as f:
                #   f.write(f"Generated from: {filename}\n")  # You can change or remove this line
                # You can change or remove this line
                f.write(
                    f"Time(Seconds),Length(Seconds),Label(string),Confidence(double),Comment(string)\n{wav_start},{wav_duration},{Name2},1,")

            # Create new subfolder and move both files into it
            target_folder_path = os.path.join(directory, old_filename+Name2)
            os.makedirs(target_folder_path, exist_ok=True)

            shutil.move(wav_path, os.path.join(
                target_folder_path, new_filename))
            shutil.move(label_path, os.path.join(
                target_folder_path, label_filename))

            # print(f"Created: {label_filename}")


def split_wav_file(file_path, output_dir="output_parts", parts=5):
    # Load audio file
    audio = AudioSegment.from_wav(file_path)
    duration_ms = len(audio)
    part_duration = duration_ms // parts

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    # Split and export
    for i in range(parts):
        start = i * part_duration
        end = start + part_duration if i < parts - \
            1 else duration_ms  # Ensure last segment gets any extra ms
        part = audio[start:end]
        output_path = os.path.join(output_dir, f"heavyload_{i + 1}.wav")
        part.export(output_path, format="wav")
        print(f"Exported: {output_path}")


# Example usage
# Replace with your path
for i in range(0, len(SubName1)):
    directory_path = f"C:/SWs/AI/ArabicCharacters/ArabicCharactersClassification/Data/Mahasiswa_Publik/{SubName1[i]}"
    create_txt_for_each_wav(directory_path, SubName1[i], SubName2[i])
    print(f".")

# print(f"done")

# analyze_wav(
#     "C:/SWs/AI/ArabicCharacters/ArabicCharactersClassification/Data/Mahasiswa_Publik/01_A/Mahasiswa2a.wav")
# directory = 'C:\SWs\AI\PSoC_AI_KIT\deepcraft_proj\Data\engine3_heavyload'

# for filename in os.listdir(directory):
#     if filename.endswith('.wav'):
#         split_wav_file(os.path.join(directory, filename))
