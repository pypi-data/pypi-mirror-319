from typing import cast
import torch
from PIL import Image


class D15Model:
    _instance = None

    def __init__(self):
        self.pipeline = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.bfloat16

    def load(self, pretrained_model_name_or_path: str = "justin/d15") -> None:
        """Load the model if not already loaded"""
        if self.pipeline is None:
            from .pipeline import MaskedStableDiffusionPipeline

            self.pipeline = cast(
                MaskedStableDiffusionPipeline,
                MaskedStableDiffusionPipeline.from_pretrained(  # type: ignore
                    pretrained_model_name_or_path,
                ).to(self.device, dtype=self.dtype),
            )

    def render(
        self,
        prompt: str,
        *,
        height: int = 768,
        width: int = 768,
        steps: int = 30,
        seed: int | None = None,
    ) -> Image.Image:
        """Render an image using the loaded model"""
        if self.pipeline is None:
            raise RuntimeError("Model not loaded. Call load() first.")

        # Generate image
        generator = torch.Generator(device=self.device)
        if seed is not None:
            generator.manual_seed(seed)

        # Prepare text embeddings
        batch_inputs = self.pipeline.tokenizer(
            [prompt],
            return_tensors="pt",
            padding="max_length",
            max_length=77,
            truncation=True,
        ).to(self.device)

        encoder_outputs = self.pipeline.text_encoder(
            batch_inputs["input_ids"],
            attention_mask=batch_inputs["attention_mask"],
            return_dict=False,
        )
        text_condition = encoder_outputs[0]
        cross_attn_masks = batch_inputs["attention_mask"]

        # Generate image
        images = cast(
            list[Image.Image],
            self.pipeline(
                prompt_embeds=text_condition,
                negative_prompt_embeds=None,
                encoder_attention_mask=cross_attn_masks,
                height=height,
                width=width,
                num_inference_steps=steps,
                generator=generator,
                output_type="pil",
                guidance_rescale=0.7,
            ).images,  # type: ignore
        )
        return images[0]

    @classmethod
    def get_model(cls) -> "D15Model":
        """Get or create the singleton model instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def d15_render(
    prompt: str,
    *,
    height: int = 768,
    width: int = 768,
    steps: int = 30,
    seed: int | None = None,
    pretrained_model_name_or_path: str = "justin/d15",
) -> Image.Image:
    """Legacy render function that loads model on each call"""
    model = D15Model.get_model()
    model.load(pretrained_model_name_or_path)
    return model.render(
        prompt,
        height=height,
        width=width,
        steps=steps,
        seed=seed,
    )


__all__ = ["d15_render", "D15Model"]
