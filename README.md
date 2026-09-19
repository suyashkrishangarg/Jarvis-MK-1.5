# 🤖 Jarvis-MK-1.5 — "Mission Real Jarvis" (voice I/O experiment)

**Jarvis-MK-1.5** ("Mission Real Jarvis") is a focused experiment toward a more
natural Jarvis: **offline hot-word detection** (Picovoice Porcupine listening for
*"jarvis"* / *"ok google"* / *"hey google"* / *"alexa"*) plus **interruptible
cloud TTS** (Deepgram Aura voices) that stops speaking the moment the hot-word
fires mid-reply, with **Chrome Web-Speech recognition** for input.

> 🧪 **Experiment, not a full assistant** — there is no chat brain, no main loop,
> and no tool routing here. `Models/Llama_3_70.py` is an empty stub (0 bytes);
> the working brains live in [Jarvis-MK-1](https://github.com/suyashkrishangarg/Jarvis-MK-1)
> and [Jarvis-Mark-1](https://github.com/suyashkrishangarg/Jarvis-Mark-1).
> ⚠️ **Windows-only** paths (`Functions\Listen.html`, `Resources\…`, `temp\data.mp3`).

---

## ✨ What's here

- 👂 **`Functions/Hotword_Detection.py`** — Porcupine wake-word listener
  (`pvporcupine==1.9.5` + `pyaudio`); blocks until a keyword is heard, then returns `True`
- 🗣️ **`Functions/Speak.py`** — Deepgram Aura TTS (`aura-luna-en` female default,
  `aura-arcas-en` male option) → `temp/data.mp3` → `pygame` playback, with a
  **barge-in thread**: hot-word detection runs while speaking and cuts playback
  the instant you say the wake word (`IS_HOT_WRD` flag)
- 🎙️ **`Functions/SpeechRecognition.py`** — headless-Chrome Web Speech API loop
  over the local `Functions/Listen.html` page (streaming interim transcripts,
  `<ended>` terminator, mic chime, optional Hindi→English `mtranslate`)
- 👤 **`API_keys.py`** — persona only (no secrets needed): `AI_Name='Jarvis'`, user profile
- 🧪 **`test.py`** — unrelated fibonacci-generator scratch file

## 🏗️ How the pieces fit (intended loop)

```
Porcupine hot-word ("jarvis") ──► SpeechRecognition.py ──► text ──► (your LLM here)
                                                                             │
Speak.py (Deepgram Aura → pygame) ◄─── reply ────────────────────────────────┘
   ▲ hot-word barge-in thread cuts audio if you interrupt
```

### Project structure

```
├── API_keys.py                  # persona only (AI/user profile, no keys)
├── requirements.txt             # selenium, webdriver_manager, pvporcupine==1.9.5
├── test.py                      # fibonacci scratch (unrelated)
├── Functions/
│   ├── Hotword_Detection.py     # Porcupine wake-word listener
│   ├── Speak.py                 # Deepgram Aura TTS + barge-in playback
│   ├── SpeechRecognition.py     # headless-Chrome Web-Speech STT loop
│   └── Listen.html              # local STT page (start/stop → live transcript)
├── Models/Llama_3_70.py         # ⚠️ empty stub — LLM not implemented here
├── Resources/                   # mic chimes + notification sounds
└── temp/data.mp3                # last synthesized reply (regenerated each speak())
```

---

## 🚀 Getting Started

### Prerequisites

- **Windows** 10/11, Python 3.10/3.11, Chrome, microphone + speakers
- `pyaudio` needs a wheel on Windows: `pip install pipwin && pipwin install pyaudio`
  (or `conda install pyaudio`)

### Installation

```bat
pip install -r requirements.txt
pip install pygame colorama requests mtranslate playaudio
```

### Try each module standalone

```bat
python Functions\Hotword_Detection.py   :: say "jarvis" → prints "aahaa"
python Functions\SpeechRecognition.py   :: live mic → transcript loop
python Functions\Speak.py               :: speaks demo lines (interruptable via hot-word)
```

Wire them into a real assistant by inserting your LLM between the STT output and
`speak()` — see `Jarvis-MK-1` / `Jarvis-Mark-1` for complete loops.

## 🛠️ Tech Stack

- **Wake word:** Picovoice Porcupine + PyAudio
- **TTS:** Deepgram Aura voices, pygame playback
- **STT:** Chrome Web Speech API via Selenium + local HTML page

## ⚠️ Notes

- `Resources/The Box.wav` (~35 MB) dominates the ~32 MB repo and is unused by
  this code — delete it to slim the repo.
- `Speak.py` hits an undocumented Deepgram page endpoint (`deepgram.com/api/ttsAudioGeneration`)
  with no API key — it can break without notice; prefer the official Deepgram SDK.
- Next steps if you revive this: implement `Models/Llama_3_70.py`, add the wake→listen→think→speak
  main loop, and drop `test.py`.

## 📄 License

MIT — free to use and modify.
