# Beyond LoRA: alternative fine-tuning techniques benchmarked

- lane: primary-source
- source: [Hugging Face Blog](https://huggingface.co/blog/peft-beyond-lora)
- published: 2026-06-18
- confidence: high
- action_surface: experiment

**Gist:** HF published a head-to-head of fine-tuning methods that go beyond LoRA, comparing accuracy and cost across the PEFT library.

**Mechanism:** Practitioner-grade benchmark across PEFT methods (DoRA, AdaLoRA, and successors) with reproducible scripts in the peft library.

**Why matters:** If you've defaulted to LoRA for the past two years, this gives a primary-source baseline to revisit before your next fine-tune.

**Try:** Pick one finetune you ran with LoRA in the last 90 days and re-run with one alternate method from the post; record delta in eval score and VRAM.
