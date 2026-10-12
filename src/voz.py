
import os
import tempfile
import wave

import sounddevice as sd
import speech_recognition as sr


class ReconhecedorDeVoz:

    def __init__(self, dispositivo=None):
        self.dispositivo = dispositivo
        self.reconhecedor = sr.Recognizer()
        self.reconhecedor.dynamic_energy_threshold = True
        self.reconhecedor.energy_threshold = 300
        self.reconhecedor.pause_threshold = 0.8
        self.reconhecedor.non_speaking_duration = 0.5

        self.frequencia = 16000
        self.canais = 1

    def gravar(self, duracao=6):
        print()
        print("Watari: Estou ouvindo...")

        try:
            audio = sd.rec(
                int(duracao * self.frequencia),
                samplerate=self.frequencia,
                channels=self.canais,
                dtype="int16",
                device=self.dispositivo
            )

            sd.wait()
            return audio

        except Exception as erro:
            print(f"Watari: Erro ao acessar o microfone: {erro}")
            return None

    def salvar_wav(self, audio):
        arquivo_temporario = tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        )

        caminho = arquivo_temporario.name
        arquivo_temporario.close()

        try:
            with wave.open(caminho, "wb") as arquivo:
                arquivo.setnchannels(self.canais)
                arquivo.setsampwidth(2)
                arquivo.setframerate(self.frequencia)
                arquivo.writeframes(audio.tobytes())

            return caminho

        except Exception:
            if os.path.exists(caminho):
                os.remove(caminho)

            return None

    def reconhecer(self, duracao=6):
        audio = self.gravar(duracao)

        if audio is None:
            return None

        caminho = self.salvar_wav(audio)

        if caminho is None:
            return None

        try:
            with sr.AudioFile(caminho) as fonte:
                dados_audio = self.reconhecedor.record(fonte)

            print("Watari: Processando sua voz...")

            texto = self.reconhecedor.recognize_google(
                dados_audio,
                language="pt-BR"
            )

            texto = texto.strip()

            if len(texto) < 3:
                print("Watari: Não ouvi um comando completo. Tente novamente.")
                return None

            return texto

        except sr.UnknownValueError:
            print("Watari: Não consegui entender. Fale mais perto do microfone.")
            return None

        except sr.RequestError as erro:
            print(f"Watari: Falha no serviço de reconhecimento: {erro}")
            return None

        except Exception as erro:
            print(f"Watari: Erro no reconhecimento: {erro}")
            return None

        finally:
            if os.path.exists(caminho):
                os.remove(caminho)