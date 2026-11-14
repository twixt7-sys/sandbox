"""Free local stills: SDXL-Lightning (4-step) on CPU, for when Figma AI credits run out (EP11).

    python pipeline/local_stills.py ep11 hook,visitor --seeds 11 23     # candidates -> out/stills/ep11/<shot>_<seed>.png
    python pipeline/local_stills.py ep11 hook --pick 11                 # lanczos 1080x1920 -> episodes/ep11/plates/hook.jpg
    python pipeline/local_stills.py ep31 statue --sprite --prompt "grey stone statue of ..." --seeds 62 5
                                                                        # a Season 2 field-card sprite in true pixel art (EP31)

Prompts come from each shot's `sdxlPrompt` (keep it under ~70 words: CLIP truncates at 77 tokens), plus STYLE below.
Weights: SDXL base 1.0 text encoders + VAE (CreativeML OpenRAIL++-M) and ByteDance/SDXL-Lightning 4-step UNet (OpenRAIL++),
both allow commercial use. About 2.5 min per image on 4 CPU cores. Memory is staged (prompts encoded, encoders freed,
UNet cast to fp32 tensor by tensor, all latents denoised, UNet freed, then VAE decode) so it fits a 14 GB container.
Install: `uv pip install -r pipeline/requirements-stills.txt`. Then run `python pipeline/plates.py <ep> --register`.

`--sprite` (EP31) is for Season 2 field-card sprites: it swaps STYLE for SPRITE_STYLE and fuses the nerijs/pixel-art-xl
LoRA (CreativeML OpenRAIL-M; needs `peft`) into the UNet, which gives a real pixel grid instead of an illustration (same
speed: the LoRA is merged into the weights). `--prompt` takes the prompt directly instead of a shot's `sdxlPrompt`; the
shot id is then just the output name. Ask for the plain subject on a flat background and make compositional changes in
code (see episodes/ep31/art/), then re-grid it with pipeline/pixelate.py.
"""
import argparse, gc, json, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STYLE = ", painterly realism, atmospheric perspective, 35mm anamorphic film still, soft film grain, muted palette, original fantasy costume, no text"
SPRITE_STYLE = ", pixel art sprite, dark outline, flat dark navy background, no text"
PIXEL_LORA = ("nerijs/pixel-art-xl", "pixel-art-xl.safetensors")
BASE = "stabilityai/stable-diffusion-xl-base-1.0"


def generate(ep, shots, seeds, out, style=STYLE, lora=None, lora_scale=1.0):
    import torch
    from accelerate import init_empty_weights
    from diffusers import EulerDiscreteScheduler, StableDiffusionXLPipeline, UNet2DConditionModel
    from huggingface_hub import hf_hub_download
    from safetensors.torch import load_file

    prompts = {s["id"]: s["sdxlPrompt"] + style for s in ep["shots"] if s["id"] in shots}
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
    if lora:
        # SGM-format LoRA keys need the UNet config to map onto diffusers' block names; the text encoders are already
        # freed, so only the UNet part is loaded, fused into the weights and unloaded.
        state, alphas = StableDiffusionXLPipeline.lora_state_dict(lora[0], weight_name=lora[1], unet_config=unet.config)
        state = {k: v for k, v in state.items() if "text_encoder" not in k}
        StableDiffusionXLPipeline.load_lora_into_unet(state, network_alphas=alphas, unet=unet, adapter_name="style", _pipeline=pipe)
        pipe.fuse_lora(components=["unet"], lora_scale=lora_scale)
        pipe.unload_lora_weights()
        del state
        gc.collect()
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
    a.add_argument("--sprite", action="store_true", help="field-card sprite: SPRITE_STYLE plus the pixel-art LoRA")
    a.add_argument("--prompt", help="use this prompt instead of each shot's sdxlPrompt (the shot id names the output)")
    args = a.parse_args()
    out = ROOT / "out" / "stills" / args.episode
    if args.pick is not None:
        for s in args.shots.split(","):
            pick(args.episode, s, args.pick, out)
    else:
        shots = args.shots.split(",")
        if args.prompt:
            ep = {"shots": [{"id": s, "sdxlPrompt": args.prompt} for s in shots]}
        else:
            ep = json.load(open(ROOT / "episodes" / args.episode / "episode.json"))
        if args.sprite:
            generate(ep, shots, args.seeds, out, style=SPRITE_STYLE, lora=PIXEL_LORA)
        else:
            generate(ep, shots, args.seeds, out)
