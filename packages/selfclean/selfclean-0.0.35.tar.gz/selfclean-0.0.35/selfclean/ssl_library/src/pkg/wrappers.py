import inspect
from typing import List, Optional, Tuple

import numpy as np
import scipy
import torch
import torchvision.transforms as transforms

from .helper import get_concept_list


class Wrapper(torch.nn.Module):
    def __init__(self, model: Optional[torch.nn.Module] = None):
        super(Wrapper, self).__init__()
        self.model = model

    def forward(self, x, n_layers: int = 4, **kwargs):
        if self.model is not None:
            return self.model(x, **kwargs)
        else:
            raise ValueError("No model was defined.")

    @property
    def device(self):
        return next(self.parameters()).device


class ViTWrapper(Wrapper):
    def __init__(
        self,
        model: torch.nn.Module,
        head: torch.nn.Module = torch.nn.Identity(),
    ):
        super(ViTWrapper, self).__init__(model=model)
        if type(head) is not torch.nn.Identity:
            self.head = head.mlp
        else:
            self.head = head

    def forward(self, x, n_layers: int = 4, return_all_tokens: bool = False, **kwargs):
        # extract the embeddings from the last N layers and combine
        inter_out = self.model.get_intermediate_layers(x, n_layers)
        if return_all_tokens:
            emb = torch.cat(inter_out, dim=-1)
        else:
            emb = torch.cat([x[:, 0, :] for x in inter_out], dim=-1)
        emb = self.head(emb)
        return emb


class ViTHuggingFaceWrapper(Wrapper):
    def __init__(
        self,
        vit_huggingface_name: str = "WinKawaks/vit-tiny-patch16-224",
        n_layers: Optional[int] = None,
    ):
        super(ViTHuggingFaceWrapper, self).__init__()
        self.n_layers = n_layers
        from transformers import ViTModel

        self.model = ViTModel.from_pretrained(vit_huggingface_name)

    def forward(
        self,
        x: torch.Tensor,
        n_layers: int = 4,
        return_all_tokens: bool = False,
        **kwargs
    ):
        kwargs = {}
        if "interpolate_pos_encoding" in inspect.getargspec(self.model).args:
            # makes sure that all input resolutions are allowed
            kwargs["interpolate_pos_encoding"] = True
        if self.n_layers is not None:
            n_layers = self.n_layers
        # extract the embeddings from the ViT
        if n_layers == 1:
            inter_out = self.model(
                pixel_values=x,
                **kwargs,
            )["last_hidden_state"]
            if return_all_tokens:
                return inter_out
            else:
                return inter_out[:, 0, :]
        else:
            hidden_states = self.model(
                pixel_values=x,
                output_hidden_states=True,
                **kwargs,
            )["hidden_states"]
            inter_out = hidden_states[-n_layers:]
            if return_all_tokens:
                emb = torch.cat(inter_out, dim=-1)
            else:
                emb = torch.cat([x[:, 0, :] for x in inter_out], dim=-1)
            return emb


class MonetHuggingFaceWrapper(ViTHuggingFaceWrapper):
    def __init__(
        self,
        vit_huggingface_name: str = "suinleelab/monet",
        n_layers: Optional[int] = None,
    ):
        super(MonetHuggingFaceWrapper, self).__init__()
        self.n_layers = n_layers
        from transformers import AutoModelForZeroShotImageClassification

        self.model = AutoModelForZeroShotImageClassification.from_pretrained(
            vit_huggingface_name
        )
        self.model = self.model.vision_model


class MONETConceptWrapper(Wrapper):

    def __init__(self, concept_list: Optional[List[str]] = None):
        super(MONETConceptWrapper, self).__init__()
        import clip

        self.model, _ = clip.load("ViT-L/14", jit=False)
        self.model.load_state_dict(
            torch.hub.load_state_dict_from_url(
                "https://aimslab.cs.washington.edu/MONET/weight_clip.pt",
                map_location=self.device,
            )
        )

        self.preprocess = MONETConceptWrapper.get_transform(img_size=(256, 224))
        # get the concepts used for matching
        self.concept_list = get_concept_list(concept_list=concept_list)
        self.concept_list, self.concept_term_list = self.concept_list
        self.prompt_embeddings = []
        for concept in self.concept_term_list:
            if type(concept) is str:
                concept = [concept]
            self.prompt_embeddings.append(
                self.get_prompt_embedding(
                    concept_term_list=concept,
                )
            )

    def forward(self, x, n_layers: int = 4, **kwargs):
        with torch.no_grad():
            reference_emb = self.model.encode_image(x)
        reference_emb_norm = reference_emb / reference_emb.norm(dim=1, keepdim=True)
        reference_emb_norm = reference_emb_norm.to(self.device)
        # get concept annotations
        concept_scores = []
        for concept_embedding in self.prompt_embeddings:
            concept_presence_score = self.calculate_concept_presence_score(
                image_features_norm=reference_emb_norm,
                prompt_target_embedding_norm=concept_embedding[
                    "prompt_target_embedding_norm"
                ],
                prompt_ref_embedding_norm=concept_embedding[
                    "prompt_ref_embedding_norm"
                ],
            )
            concept_scores.append(concept_presence_score)
        concept_scores = torch.stack(concept_scores, dim=-1)
        return concept_scores

    def get_prompt_embedding(
        self,
        concept_term_list: List[str] = [],
        prompt_template_list: List[str] = [
            "This is skin image of {}",
            "This is dermatology image of {}",
            "This is image of {}",
            # But we don't have dermatoscopy images
            # "This is dermatoscopy of {}",
            # "This is dermoscopy of {}",
        ],
        prompt_ref_list: List[List[str]] = [
            ["This is skin image"],
            ["This is dermatology image"],
            ["This is image"],
            # But we don't have dermatoscopy images
            # ["This is dermatoscopy"],
            # ["This is dermoscopy"],
        ],
    ):
        """
        Generate prompt embeddings for a concept.

        Args:
            concept_term_list (list): List of concept terms that will be used to generate prompt target embeddings.
            prompt_template_list (list): List of prompt templates.
            prompt_ref_list (list): List of reference phrases.

        Returns:
            dict: A dictionary containing the normalized prompt target embeddings and prompt reference embeddings.
        """
        import clip

        # target embedding
        prompt_target = [
            [prompt_template.format(term) for term in concept_term_list]
            for prompt_template in prompt_template_list
        ]
        prompt_target_tokenized = [
            clip.tokenize(prompt_list, truncate=True) for prompt_list in prompt_target
        ]
        with torch.no_grad():
            prompt_target_embedding = torch.stack(
                [
                    self.model.encode_text(prompt_tokenized.to(self.device))
                    for prompt_tokenized in prompt_target_tokenized
                ]
            )
        prompt_target_embedding_norm = (
            prompt_target_embedding / prompt_target_embedding.norm(dim=2, keepdim=True)
        )

        # reference embedding
        prompt_ref_tokenized = [
            clip.tokenize(prompt_list, truncate=True) for prompt_list in prompt_ref_list
        ]
        with torch.no_grad():
            prompt_ref_embedding = torch.stack(
                [
                    self.model.encode_text(prompt_tokenized.to(self.device))
                    for prompt_tokenized in prompt_ref_tokenized
                ]
            )
        prompt_ref_embedding_norm = prompt_ref_embedding / prompt_ref_embedding.norm(
            dim=2, keepdim=True
        )

        return {
            "prompt_target_embedding_norm": prompt_target_embedding_norm,
            "prompt_ref_embedding_norm": prompt_ref_embedding_norm,
        }

    @staticmethod
    def calculate_concept_presence_score(
        image_features_norm,
        prompt_target_embedding_norm,
        prompt_ref_embedding_norm,
        temp=1 / np.exp(4.5944),
    ):
        """
        Calculate the concept presence score based on image features and concept embeddings.

        Args:
            image_features_norm (numpy.Tensor): Normalized image features.
            prompt_target_embedding_norm (torch.Tensor): Normalized concept target embedding.
            prompt_ref_embedding_norm (torch.Tensor): Normalized concept reference embedding.
            temp (float, optional): Temperature parameter for softmax. Defaults to 1 / np.exp(4.5944).

        Returns:
            np.array: Concept presence score.
        """
        target_similarity = (
            prompt_target_embedding_norm.float() @ image_features_norm.T.float()
        )
        ref_similarity = (
            prompt_ref_embedding_norm.float() @ image_features_norm.T.float()
        )

        target_similarity_mean = target_similarity.mean(dim=[1])
        ref_similarity_mean = ref_similarity.mean(axis=1)

        concept_presence_score = torch.nn.functional.softmax(
            torch.stack([target_similarity_mean / temp, ref_similarity_mean / temp]),
            dim=0,
        )[0, :].mean(axis=0)

        return concept_presence_score

    @staticmethod
    def get_transform(img_size: Tuple[int, int] = (256, 224)):
        def convert_image_to_rgb(image):
            return image.convert("RGB")

        return transforms.Compose(
            [
                transforms.Resize(
                    img_size[0],
                    interpolation=transforms.InterpolationMode.BICUBIC,
                ),
                transforms.CenterCrop(img_size[1]),
                convert_image_to_rgb,
                transforms.ToTensor(),
                transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
            ]
        )


class UNetWrapper(Wrapper):
    def __init__(self, model: torch.nn.Module):
        super(UNetWrapper, self).__init__(model=model)

    def forward(self, x):
        # extract only the green channel (input colorme)
        x = x[:, 1, :, :][:, None, :, :]
        # get the last features from the encoder
        emb = self.model(x)[-1]
        emb = torch.nn.AdaptiveAvgPool2d((1, 1))(emb)
        return emb


class ColorMeSegWrapper(Wrapper):
    def __init__(self, model: torch.nn.Module):
        super(ColorMeSegWrapper, self).__init__(model=model)

    def forward(self, x):
        # extract only the green channel (input colorme)
        x = x[:, 1, :, :][:, None, :, :]
        # get the last features from the encoder
        mask = self.model(x)
        return mask
