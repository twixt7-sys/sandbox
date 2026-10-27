"""Free local stills: SDXL-Lightning (4-step) on CPU, for when Figma AI credits run out (EP11).

    python pipeline/local_stills.py ep11 hook,visitor --seeds 11 23     # candidates -> out/stills/ep11/<shot>_<seed>.png
    python pipeline/local_stills.py ep11 hook --pick 11                 # lanczos 1080x1920 -> episodes/ep11/plates/hook.jpg

Prompts come from each shot's `sdxlPrompt` (keep it under ~70 words: CLIP truncates at 77 tokens), plus STYLE below.
Weights: SDXL base 1.0 text encoders + VAE (CreativeML OpenRAIL++-M) and ByteDance/SDXL-Lightning 4-step UNet (OpenRAIL++),
both allow commercial use. About 2.5 min per image on 4 CPU cores. Memory is staged (prompts encoded, encoders freed,
UNet cast to fp32 tensor by tensor, all latents denoised, UNet freed, then VAE decode) so it fits a 14 GB container.
Then run `python pipeline/plates.py <ep> --register`.
"""
import argparse, gc, json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE = ", painterly realism, atmospheric perspective, 35mm anamorphic film still, soft film grain, muted palette, original fantasy costume, no text"
BASE = "stabilityai/stable-diffusion-xl-base-1.0"


def generate(ep, shots, seeds, out):
    import torch
    from accelerate import init_empty_weights
    from diffusers import EulerDiscreteScheduler, StableDiffusionXLPipeline, UNet2DConditionModel
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file

    prompts = {s["id"]: s["sdxlPrompt"] + STYLE for s in ep["shots"] if s["id"] in shots}
    torch.set_num_threads(max(1, torch.get_num_threads()))
    pipe = StableDiffusionXLPipeline.from_pretrained(BASE, unet=None, torch_dtype=torch.float32, variant="fp16", use_safetensors=True)
    with torch.no_grad():
        emb = {k: pipe.encode_prompt(p, do_classifier_free_guidance=False) for k, p in prompts.items()}
    pipe.text_encoder = pipe.text_encoder_2 = None
    gc.collect()
    with init_empty_weights():
        unet = UNet2DConditionModel.from_config(UNet2DConditionModel.load_config(BASE, subfolder="unet"))
    sd = load_file(hf_hub_download("ByteDance/SDXL-Lightning", "sdxl_lightning_4step_unet.safetensors"))
    for k in list(sd):
        sd[k] = sd[k].float()
    unet.load_state_dict(sd, assign=True)
    del sd
    gc.collect()
    pipe.unet = unet
    pipe.scheduler = EulerDiscreteScheduler.from_config(pipe.scheduler.config, timestep_spacing="trailing")
    pipe.enable_attention_slicing()
    lat = {}
    for k, (pe, _, ppe, _) in emb.items():
        for seed in seeds:
            t = time.time()
            lat[(k, seed)] = pipe(prompt_embeds=pe, pooled_prompt_embeds=ppe, num_inference_steps=4, guidance_scale=0, width=768, height=1344,
                                  generator=torch.Generator().manual_seed(seed), output_type="latent").images
            print(f"[stills] {k} seed {seed}: {time.time() - t:.0f}s", flush=True)
    pipe.unet = unet = None
    gc.collect()
    vae = pipe.vae
    vae.enable_tiling()
    out.mkdir(parents=True, exist_ok=True)
    with torch.no_grad():
        for (k, seed), l in lat.items():
            img = vae.decode(l / vae.config.scaling_factor, return_dict=False)[0]
            pipe.image_processor.postprocess(img, output_type="pil")[0].save(out / f"{k}_{seed}.png")
            print(f"[stills] wrote {out / f'{k}_{seed}.png'}")


def pick(ep_id, shot, seed, out):
    from PIL import Image
    im = Image.open(out / f"{shot}_{seed}.png").convert("RGB")
    w = round(im.width * 1920 / im.height)
    im = im.resize((w, 1920), Image.LANCZOS)
    x = (w - 1080) // 2
    dst = ROOT / "episodes" / ep_id / "plates" / f"{shot}.jpg"
    dst.parent.mkdir(parents=True, exist_ok=True)
    im.crop((x, 0, x + 1080, 1920)).save(dst, quality=93)
    print(f"[stills] {dst}")


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("episode")
    a.add_argument("shots", help="comma-separated shot ids")
    a.add_argument("--seeds", nargs="+", type=int, default=[11, 23])
    a.add_argument("--pick", type=int, help="upscale this seed into episodes/<ep>/plates/<shot>.jpg")
    args = a.parse_args()
    out = ROOT / "out" / "stills" / args.episode
    if args.pick is not None:
        for s in args.shots.split(","):
            pick(args.episode, s, args.pick, out)
    else:
        ep = json.load(open(ROOT / "episodes" / args.episode / "episode.json"))
        generate(ep, args.shots.split(","), args.seeds, out)
