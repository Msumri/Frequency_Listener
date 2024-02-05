import pyaudio
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


hz=[]

def find_most_common_value(input_list):
    counter = Counter(input_list)
    most_common_value, _ = counter.most_common(1)[0]
    return most_common_value


def detect_frequencies(sample_rate, chunk_size):
    p = pyaudio.PyAudio()

    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=sample_rate,
                    input=True,
                    frames_per_buffer=chunk_size)

    print("Listening...")

    try:
        while True:
            data = np.frombuffer(stream.read(chunk_size), dtype=np.int16)
            fft_result = np.fft.fft(data)
            frequencies = np.fft.fftfreq(len(fft_result), 1 / sample_rate)
            magnitude = np.abs(fft_result)

            # Plot the spectrum
            plt.plot(frequencies, magnitude)
            plt.title('Frequency Spectrum')
            plt.xlabel('Frequency (Hz)')
            plt.ylabel('Magnitude')
            plt.xlim(0, 5000)  # Adjust the range as needed
            plt.pause(0.01)
            plt.clf()

            # Find the frequency with the maximum magnitude
            max_index = np.argmax(magnitude)
            max_frequency = frequencies[max_index]
            max_magnitude = magnitude[max_index]
            hz.append(max_frequency)
    except KeyboardInterrupt:
            result = find_most_common_value(hz)
            print(result)
            print(f"your object frequncy is :  {result} Hz")

    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    sample_rate = 44100  # You may need to adjust this based on your microphone
    chunk_size = 1024  # Adjust this for better frequency resolution
    detect_frequencies(sample_rate, chunk_size)

