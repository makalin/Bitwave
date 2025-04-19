# 🎧 Bitwave - Next-Gen Multi-Channel Audio Format

![Version](https://img.shields.io/badge/version-v1.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Build](https://img.shields.io/badge/build-passing-brightgreen)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)
![Status](https://img.shields.io/badge/status-alpha-orange)

**Bitwave** is a high-fidelity, developer-friendly, future-proof audio format designed for modern sound experiences — including spatial audio, dynamic tempo adjustment, and multi-track support.

> Minimal. Powerful. Immersive.

---

## 🔥 Features

- 🎚️ **Multi-channel support** – From stereo to 7.1+, ambisonic, and 3D formats
- ⏱️ **Dynamic tempo control** – Ideal for DJs, generative music, and interactive environments
- 🌐 **Spatial-ready** – Built-in XYZ positioning for VR/AR and immersive experiences
- 🧠 **AI-enhanced compatibility** – Ready for real-time audio transformation and neural mixing
- 💾 **Compact & efficient** – Optimized binary format with optional lossless compression
- 📁 **Modern file extension**: `.bwx`

---

## 🧩 Supported Extensions

| Extension | Description |
|-----------|-------------|
| `.bw2`    | Bitwave v2 – Latest version with enhanced features |
| `.bwx`    | Bitwave eXtended – Multichannel, 3D, spatial audio |
| `.bwa`    | Bitwave Audio – Standard audio content |
| `.bwm`    | Bitwave Master – Mastering / studio-level quality |
| `.bwd`    | Bitwave Dynamic – Tempo & rhythm adaptive version |
| `.bwl`    | Bitwave Light – Lightweight, streaming optimized |
| `.bwf`    | Bitwave Full – Includes full metadata and spatial data |
| `.bwr`    | Bitwave Raw – Uncompressed or minimally processed |
| `.bwi`    | Bitwave Immersive – VR/AR ready, full 3D audio |
| `.bwt`    | Bitwave Track – Optimized for music tracks |
| `.bwp`    | Bitwave Pro – Professional content & production ready |

---

## 📦 File Structure (v1)

| Section        | Description                            |
|----------------|----------------------------------------|
| `BWX_HEADER`   | Magic bytes, version, flags            |
| `META_BLOCK`   | Sample rate, channels, duration, bpm   |
| `SPATIAL_BLOCK`| Positional data (x, y, z) per channel  |
| `AUDIO_STREAM` | Encoded audio frames                   |
| `FOOTER`       | Checksum & optional tags               |

---

## 🚀 Getting Started

### Playback Tool (coming soon)

```bash
bwplay track.bwx
```

### Encode from WAV

```bash
bwencode input.wav -o output.bwx --spatial --bpm 120
```

---

## 📚 Use Cases

- 🎮 Game Audio Engines (Unity, Unreal, Godot)
- 🎧 VR / AR Experiences
- 🎛️ Live DJ sets with tempo-controlled transitions
- 🎼 Immersive installations & 3D soundscapes
- 📡 Real-time streaming with spatial audio

---

## 🛠️ Developer Tools

- CLI tools for encoding/decoding (`bwencode`, `bwdecode`)
- Python & Rust libraries coming soon
- Plugin support for DAWs (Ableton, FL, Reaper, etc.)

---

## 🧪 Roadmap

- [x] Core `.bwx` format & parser
- [ ] Lossless & hybrid compression support
- [ ] Open source cross-platform player
- [ ] Realtime tempo-sync with MIDI/OSC
- [ ] Plugin SDK for audio software

---

## 💬 Community & Feedback

We’re building Bitwave in the open. Feedback, feature requests, and contributors are welcome!

👉 [Issues](https://github.com/makalin/Bitwave/issues) • [Discussions](https://github.com/makalin/Bitwave/discussions)

---

## ⚡ License

MIT License — use it freely, contribute openly, play it loud.

---

**Built for creators, coders, and cosmic listeners.**  
→ _Bitwave: Redefining the sound of the future._
