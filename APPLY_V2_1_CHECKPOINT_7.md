# Apply v2.1 Development — Checkpoint 7

1. Gunakan patch CP7 di atas baseline repository **Checkpoint 6** atau ekstrak snapshot lengkap CP7 ke folder baru.
2. Jangan menghapus/menimpa arsip stabil `releases/v2.0.0/`. Tidak perlu tag GitHub Release.
3. Jalankan: `python tools/build_chatgpt_context.py` kemudian `python tools/build_chatgpt_context.py --verify`.
4. Untuk memakai langsung di ChatGPT, unggah `dist/chatgpt-v2.1-cp7/GAS_CHATGPT_CONTEXT.txt`; unggah referensi panjang dan kode hanya jika dibutuhkan.
5. Untuk Project, tempatkan isi `CHATGPT_PROJECT_INSTRUCTIONS.txt` pada Project Instructions.
6. Validasi: `PYTHONPATH=tools python -m unittest tools.test_chatgpt_context -v` plus workflow pengujian GAS existing.

**Catatan:** upload file ≠ instalasi Agent Skill. File yang diunggah tidak menghubungkan akun Google atau menjalankan script secara otomatis. ZIP context ditujukan untuk ekstraksi dahulu.
