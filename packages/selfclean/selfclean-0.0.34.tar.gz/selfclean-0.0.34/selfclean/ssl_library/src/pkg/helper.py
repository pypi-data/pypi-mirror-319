import tempfile
from pathlib import Path
from typing import List, Optional, Tuple, Union

import numpy as np
import torch
from tqdm.auto import tqdm

ARR_TYPE = Union[np.ndarray, np.memmap, torch.Tensor]


def embed_dataset(
    torch_dataset: torch.utils.data.DataLoader,
    model: Optional[torch.nn.Sequential],
    n_layers: int,
    normalize: bool = False,
    memmap: bool = True,
    memmap_path: Union[Path, str, None] = None,
    return_only_embedding_and_labels: bool = False,
    tqdm_desc: Optional[str] = None,
) -> Union[Tuple[ARR_TYPE, ARR_TYPE, ARR_TYPE, ARR_TYPE], Tuple[ARR_TYPE, ARR_TYPE]]:
    labels = []
    paths = []
    batch_size = torch_dataset.batch_size
    iterator = tqdm(
        enumerate(torch_dataset),
        position=0,
        leave=True,
        total=len(torch_dataset),
        desc=tqdm_desc,
    )
    # calculate the embedding dimension for memmap array
    _batch = torch_dataset.dataset[0][0][None, ...]
    if model is not None:
        _batch = _batch.to(model.device)
    batch_dim = tuple(_batch.shape)[1:]
    if (
        type(model) is torch.jit._script.RecursiveScriptModule
        or type(model) is torch.nn.Sequential
    ):
        emb_dim = model(_batch).squeeze().shape[0]
    elif model is None:
        emb_dim = _batch.squeeze().shape[0]
    else:
        emb_dim = model(_batch, n_layers=n_layers).squeeze().shape[0]
    # create the memmap's
    if memmap:
        memmap_path = create_memmap_path(memmap_path=memmap_path)
        emb_space = create_memmap(
            memmap_path,
            "embedding_space.dat",
            len(torch_dataset.dataset),
            *(emb_dim,),
        )
        if not return_only_embedding_and_labels:
            images = create_memmap(
                memmap_path,
                "images.dat",
                len(torch_dataset.dataset),
                *batch_dim,
            )
    else:
        emb_space = np.zeros(shape=(len(torch_dataset.dataset), emb_dim))
        if not return_only_embedding_and_labels:
            images = np.zeros(shape=(len(torch_dataset.dataset), *batch_dim))
    del emb_dim, batch_dim, _batch
    # embed the dataset
    for i, batch_tup in iterator:
        if len(batch_tup) == 3:
            batch, path, label = batch_tup
        elif len(batch_tup) == 2:
            batch, label = batch_tup
            path = None
        else:
            raise ValueError("Unknown batch tuple.")

        with torch.no_grad():
            if model is not None:
                batch = batch.to(model.device)
            if (
                type(model) is torch.jit._script.RecursiveScriptModule
                or type(model) is torch.nn.Sequential
            ):
                emb = model(batch)
            elif model is None:
                emb = batch
            else:
                emb = model(batch, n_layers=n_layers)
            emb = emb.squeeze()
            if normalize:
                emb = torch.nn.functional.normalize(emb, dim=-1, p=2)
            emb_space[batch_size * i : batch_size * (i + 1), :] = emb.cpu()
            if type(emb_space) is np.memmap:
                emb_space.flush()
            labels.append(label.cpu())
            if not return_only_embedding_and_labels:
                images[batch_size * i : batch_size * (i + 1), :] = batch.cpu()
                if type(images) is np.memmap:
                    images.flush()
                if path is not None:
                    paths += path
    labels = torch.concat(labels).cpu()
    if return_only_embedding_and_labels:
        return emb_space, labels
    if len(paths) > 0:
        paths = np.array(paths)
    else:
        paths = None
    return emb_space, labels, images, paths


def create_memmap(memmap_path: Path, memmap_file_name: str, len_dataset: int, *dims):
    memmap_file = memmap_path / memmap_file_name
    if memmap_file.exists():
        memmap_file.unlink()
    memmap = np.memmap(
        str(memmap_file),
        dtype=np.float32,
        mode="w+",
        shape=(len_dataset, *dims),
    )
    return memmap


def create_memmap_path(memmap_path: Union[str, Path, None]) -> Path:
    if memmap_path is None:
        # temporary folder for saving memory map
        memmap_path = Path(tempfile.mkdtemp())
    else:
        # make sure the path exists
        memmap_path = Path(memmap_path)
        memmap_path.mkdir(parents=True, exist_ok=True)
    return memmap_path


def get_concept_list(concept_list: Optional[List[str]] = None):
    if concept_list is None:
        concept_list = [
            # SkinCon
            "Vesicle",
            "Papule",
            "Macule",
            "Plaque",
            "Abscess",
            "Pustule",
            "Bulla",
            "Patch",
            "Nodule",
            "Ulcer",
            "Crust",
            "Erosion",
            "Excoriation",
            "Atrophy",
            "Exudate",
            "Purpura/Petechiae",
            "Fissure",
            "Induration",
            "Xerosis",
            "Telangiectasia",
            "Scale",
            "Scar",
            "Friable",
            "Sclerosis",
            "Pedunculated",
            "Exophytic/Fungating",
            "Warty/Papillomatous",
            "Dome-shaped",
            "Flat topped",
            "Brown(Hyperpigmentation)",
            "Translucent",
            "White(Hypopigmentation)",
            "Purple",
            "Yellow",
            "Black",
            "Erythema",
            "Comedo",
            "Lichenification",
            "Blue",
            "Umbilicated",
            "Poikiloderma",
            "Salmon",
            "Wheal",
            "Acuminate",
            "Burrow",
            "Gray",
            "Pigmented",
            "Cyst",
            # Derm7pt Concept
            # "pigment network",
            # "typical pigment network",
            # "atypical pigment network",
            # "regression structure",
            # "pigmentation",
            # "regular pigmentation",
            # "irregular pigmentation",
            # "blue whitish veil",
            # "vascular structures",
            # "typical vascular structures",
            # "atypical vascular structures",
            # "streaks",
            # "regular streaks",
            # "irregular streaks",
            # "dots and globules",
            # "regular dots and globules",
            # "irregular dots and globules",
            # General
            # "purple pen",
            # "nail",
            # "pinkish",
            # "red",
            # "hair",
            # "orange sticker",
            # "dermoscope border",
            # "gel",
        ]
    disease_list = [
        "seborrheic keratosis",
        "nevus",
        "squamous cell carcinoma",
        "melanoma",
        "lichenoid keratosis",
        "lentigo",
        "actinic keratosis",
        "basal cell carcinoma",
        "dermatofibroma",
        "atypical melanocytic proliferation",
        "verruca",
        "clear cell acanthoma",
        "angiofibroma or fibrous papule",
        "scar",
        "angioma",
        "atypical spitz tumor",
        "solar lentigo",
        "AIMP",
        "neurofibroma",
        "lentigo simplex",
        "acrochordon",
        "angiokeratoma",
        "vascular lesion",
        "cafe-au-lait macule",
        "pigmented benign keratosis",
        # more diseases
        "basal cell carcinoma",
        "blue nevus",
        "clark nevus",
        "combined nevus",
        "congenital nevus",
        "dermal nevus",
        "dermatofibroma",
        "lentigo",
        "melanoma",
        "melanosis",
        "recurrent nevus",
        "reed or spitz nevus",
        "seborrheic keratosis",
        "vascular lesion",
        # from me
        "ringworm",
    ]

    concept_term_list = []
    for concept_name in concept_list:
        ret = concept_to_prompt(concept_name)
        if ret is not None:
            prompt_dict, _ = ret
            prompt_engineered_list = []
            for k, v in prompt_dict.items():
                if k != "original":
                    prompt_engineered_list += v
        else:
            prompt_engineered_list = [concept_name]
        concept_term_list += [
            list(
                set(
                    [
                        prompt.replace("This is ", "")
                        .replace("This photo is ", "")
                        .replace("This lesion is ", "")
                        .replace("skin has become ", "")
                        .lower()
                        for prompt in prompt_engineered_list
                    ]
                )
            )
        ]
    # NOTE: For now we are not considering diseases
    del disease_list
    return concept_list, concept_term_list


def concept_to_prompt(concept_name):
    if concept_name == "White(Hypopigmentation)":
        text_counter = "White"
        prompt_dict = {"original": "This is White(Hypopigmentation)"}
        prompt_dict.update(
            {
                "1": ["This is White(Hypopigmentation)"],
                "1_": ["This photo is White(Hypopigmentation)"],
                "2": ["This is Hypopigmentation"],
                "2_": ["This photo is Hypopigmentation"],
            }
        )
        prompt_dict["original"] = "This is White(Hypopigmentation)"

    elif concept_name == "Brown(Hyperpigmentation)":
        text_counter = "Brown"
        prompt_dict = {"original": "This is Brown(Hyperpigmentation)"}
        prompt_dict.update(
            {
                "1": ["This is Brown(Hyperpigmentation)"],
                "1_": ["This photo is Brown(Hyperpigmentation)"],
                "2": ["This is Hyperpigmentation"],
                "2_": ["This photo is Hyperpigmentation"],
                "3": ["This is Hyperpigmented"],
                "3_": ["This photo is Hyperpigmented"],
            }
        )

    elif concept_name == "Blue":
        text_counter = "Blue"
        prompt_dict = {"original": "This is Blue"}
        prompt_dict.update(
            {
                "1": ["This is Blue"],
                "2": ["This lesion is Blue"],
                "3": ["This lesion is Blue color"],
            }
        )

    elif concept_name == "Yellow":
        text_counter = "Yellow"
        prompt_dict = {"original": "This is Yellow"}
        prompt_dict.update(
            {
                "1": ["This is Yellow"],
            }
        )

    elif concept_name == "Black":
        text_counter = "Black"
        prompt_dict = {"original": "This is Black"}
        prompt_dict.update(
            {
                "1": ["This is Black"],
                "2": ["This lesion is Black"],
                "3": ["This lesion is Black color"],
            }
        )

    elif concept_name == "Purple":
        text_counter = "Purple"
        prompt_dict = {"original": "This is Purple"}
        prompt_dict.update(
            {
                "1": ["This is Purple"],
            }
        )

    elif concept_name == "Gray":
        text_counter = "Gray"
        prompt_dict = {"original": "This is Gray"}
        prompt_dict.update(
            {
                "1": ["This photo is Gray"],
            }
        )

    elif concept_name == "Pigmented":
        text_counter = "Pigmented"
        prompt_dict = {"original": "This is Pigmented"}
        prompt_dict.update(
            {
                "1": ["This is Pigmented"],
            }
        )

    elif concept_name == "Erythema":
        text_counter = "Erythema"
        prompt_dict = {"original": "This is Erythema"}
        prompt_dict.update(
            {
                "1": ["This is redness"],
                "2": ["This is erythematous"],
            }
        )

    ################################
    # primary
    ################################
    elif concept_name == "Patch":
        text_counter = "Patch"
        prompt_dict = {"original": "This is Patch"}
        prompt_dict.update(
            {
                "1": ["This is Vitiligo"],
                "1_": ["This photo is Vitiligo"],
                "2": ["This is Melasma"],
                "2_": ["This photo is Melasma"],
                "3": ["This is hyperpigmented"],
                "3_": ["This is hyperpigmented"],
            }
        )

    elif concept_name == "Nodule":
        text_counter = "Nodul"
        prompt_dict = {"original": "This is Nodule"}
        prompt_dict.update(
            {
                "1": ["This is Nodule"],
                "2": ["This is nodular"],
                "3": ["This is cyst"],
            }
        )

    elif concept_name == "Macule":
        text_counter = "Macul"
        prompt_dict = {"original": "This is Macule"}
        prompt_dict.update(
            {
                "1": ["This is Macular"],
                "2": ["This photo is Macule"],
                "3": ["This is Lentigo"],
                "4": ["This photo is Lentigo"],
                "5": ["This is freckle"],
                "6": ["This photo is freckle"],
            }
        )

    elif concept_name == "Papule":
        text_counter = "Papul"
        prompt_dict = {"original": "This is Papule"}
        prompt_dict.update(
            {
                "1": ["This is Papular"],
            }
        )

    elif concept_name == "Plaque":
        text_counter = "Plaqu"
        prompt_dict = {"original": "This is Plaque"}
        prompt_dict.update(
            {
                "1": ["This is Plaque"],
                "2": ["This is Psoriasis"],
                "3": ["This is dermatitis"],
            }
        )

    elif concept_name == "Vesicle":
        text_counter = "Vesicl"
        prompt_dict = {"original": "This is Vesicle"}
        prompt_dict.update(
            {
                "1": ["This photo is Vesicle"],
                "2": ["This is fluid-containing"],
            }
        )

    elif concept_name == "Pustule":
        text_counter = "Pustul"
        prompt_dict = {"original": "This is Pustule"}
        prompt_dict.update(
            {
                "1": ["This photo is Pustule"],
            }
        )

    ################################
    # secondary
    ################################

    elif concept_name == "Crust":
        text_counter = "Crust"
        prompt_dict = {"original": "This is Crust"}
        prompt_dict.update(
            {
                "1": ["This is Crust"],
                "2": ["This is dried Crust"],
                "2_": ["This photo is dried Crust"],
            }
        )

    elif concept_name == "Scale":
        text_counter = "Scale"
        prompt_dict = {"original": "This is Scale"}
        prompt_dict.update(
            {
                "1": ["Hyperkeratosis"],
                "2": ["This is scaly"],
                # "3": ["This is flaking scale"],
                "3": ["This is flaky and scaly"],
            }
        )
    elif concept_name == "Fissure":
        text_counter = "Fissure"
        prompt_dict = {"original": "This is Fissure"}
        prompt_dict.update(
            {
                "1": ["This is dry and cracked skin"],
            }
        )

    elif concept_name == "Erosion":
        text_counter = "Erosion"
        prompt_dict = {"original": "This is Erosion"}
        prompt_dict.update(
            {
                "1": ["This is Erosion"],
                "2": ["This photo is erosion"],
                "3": ["This is breakdown of the outer layers"],
                "4": ["This is Impetigo"],
                "5": ["This is Erosive"],
            }
        )

    elif concept_name == "Ulcer":
        text_counter = "Ulcer"
        prompt_dict = {"original": "This is Ulcer"}
        prompt_dict.update(
            {
                "1": ["This is Ulcer"],
                "2": ["This photo is Ulcer"],
                "3": ["This photo is Ulcerated"],
                "4": ["This is Ulcerated"],
            }
        )

    elif concept_name == "Excoriation":
        text_counter = "Excoriation"
        prompt_dict = {"original": "This is Excoriation"}
        prompt_dict.update(
            {
                "1": ["This photo is Excoriation"],
            }
        )

    elif concept_name == "Atrophy":
        text_counter = "Atrophy"
        prompt_dict = {"original": "This is Atrophy"}
        prompt_dict.update(
            {
                "1": ["This is Atrophic"],
            }
        )

    elif concept_name == "Lichenification":
        text_counter = "Lichenification"
        prompt_dict = {"original": "This is Lichenification"}
        prompt_dict.update(
            {
                "1": ["This is Lichenification"],
                "2": ["skin has become thickened and leathery"],
            }
        )

    ################################
    # others
    ################################

    elif concept_name == "Cyst":
        text_counter = "Cyst"
        prompt_dict = {"original": "This is Cyst"}
        prompt_dict.update(
            {
                "1": ["This photo is Cyst"],
            }
        )

    elif concept_name == "Salmon":
        text_counter = "Salmon"
        prompt_dict = {"original": "This is Salmon"}
        prompt_dict.update(
            {
                "1": ["This photo is Salmon patch"],
            }
        )

    elif concept_name == "Translucent":
        text_counter = "Translucent"
        prompt_dict = {"original": "This is Translucent"}
        prompt_dict.update(
            {
                "1": ["This is Translucent"],
                "2": ["This bump is Translucent"],
            }
        )

    elif concept_name == "Warty/Papillomatous":
        text_counter = "Wart"
        prompt_dict = {"original": "This is Warty/Papillomatous"}
        prompt_dict.update(
            {
                "1": ["This is Warty and Papillomatous"],
            }
        )
    elif concept_name == "Exophytic/Fungating":
        text_counter = "Exophyti"
        prompt_dict = {"original": "This is Exophytic/Fungating"}
        prompt_dict.update(
            {
                "1": ["This is Fungating"],
            }
        )

    elif concept_name == "Purpura/Petechiae":
        text_counter = "Purpura"
        prompt_dict = {"original": "This is Purpura/Petechiae"}
        prompt_dict.update(
            {
                "1": ["This is Purpura"],
            }
        )

    elif concept_name == "Friable":
        text_counter = "Friable"
        prompt_dict = {"original": "This is Friable"}
        prompt_dict.update(
            {
                "1": ["This photo is Friable"],
                "2": ["This is Friable"],
            }
        )

    elif concept_name == "Bulla":
        text_counter = "bullae"
        prompt_dict = {"original": "This is Bulla"}
        prompt_dict.update(
            {
                "1": ["This photo is bullae"],
                "2": ["This is bullae"],
                "3": ["This is blister"],
                "4": ["This photo is blister"],
            }
        )

    elif concept_name == "Xerosis":
        text_counter = "Xerosis"
        prompt_dict = {"original": "This is Xerosis"}
        prompt_dict.update(
            {
                "1": ["This photo is Xerosis"],
                "2": ["This is Xerosis"],
                "3": ["This is abnormally dry skin"],
                "4": ["This photo is abnormally dry skin"],
                "5": ["This is dry skin"],
                "6": ["This photo is dry skin"],
            }
        )

    elif concept_name == "Scar":
        text_counter = "Scar"
        prompt_dict = {"original": "This is Scar"}
        prompt_dict.update(
            {
                "1": ["This photo is Scar"],
                "2": ["This is Scar"],
                "3": ["This is Keloid scars"],
                "4": ["This is Contractures scars"],
                "5": ["This is Hypertrophic scars"],
                "6": ["This is Acnescars scars"],
            }
        )
    elif concept_name == "Sclerosis":
        text_counter = "Sclerosis"
        prompt_dict = {"original": "This is Sclerosis"}
        prompt_dict.update(
            {
                "1": ["This is Scleroderma"],
                "2": ["This is CREST syndrome"],
            }
        )

    elif concept_name == "Abscess":
        text_counter = "Abscess"
        prompt_dict = {"original": "This is Abscess"}
        prompt_dict.update(
            {
                "1": ["This is Abscess"],
                "2": ["This is swollen, pus-filled lump"],
            }
        )

    elif concept_name == "Exudate":
        text_counter = "Exudate"
        prompt_dict = {"original": "This is Exudate"}
        prompt_dict.update(
            {
                "1": ["This is Exudate"],
                "2": ["This is Ooze. Pus. Secretion"],
            }
        )

    elif concept_name == "Acuminate":  # THIS DOES NOT WORK WELL
        text_counter = "Acuminate"
        prompt_dict = {"original": "This is Acuminate"}
        prompt_dict.update(
            {
                "1": ["This is Acuminate"],
            }
        )

    elif concept_name == "Burrow":
        text_counter = "Burrow"
        prompt_dict = {"original": "This is Burrow"}
        prompt_dict.update(
            {
                "1": ["This is Burrow"],
                "2": ["This photo is Burrow"],
                "3": ["This is Scabies"],
                "4": ["This photo is Scabies"],
            }
        )

    elif concept_name == "Wheal":
        text_counter = "Urticaria"
        prompt_dict = {"original": "This is Wheal"}
        prompt_dict.update(
            {
                "1": ["This is Urticaria"],
                "2": ["This photo is Urticaria"],
            }
        )

    elif concept_name == "Comedo":  # ISN'T IT DISEASE?
        text_counter = "Comedo"
        prompt_dict = {"original": "This is Comedo"}
        prompt_dict.update(
            {
                "1": ["This photo is whitehead or blackhead"],
            }
        )

    elif concept_name == "Induration":
        text_counter = "Induration"
        prompt_dict = {"original": "This is Induration"}
        prompt_dict.update(
            {
                "1": ["This is Edema"],
                "2": ["This is oedema"],
            }
        )

    elif concept_name == "Telangiectasia":
        text_counter = "Telangiectasia"
        prompt_dict = {"original": "This is Telangiectasia"}
        prompt_dict.update(
            {
                "1": ["This is dilated or broken blood vessels"],
                "2": ["This photo is dilated or broken blood vessels"],
            }
        )

    elif concept_name == "Pedunculated":
        text_counter = "Pedunculated"
        prompt_dict = {"original": "This is Pedunculated"}
        prompt_dict.update(
            {
                "1": ["This is Pedunculated"],
                "2": ["This photo is Pedunculated"],
            }
        )

    elif concept_name == "Poikiloderma":
        text_counter = "Poikiloderma"
        prompt_dict = {"original": "This is Poikiloderma"}
        prompt_dict.update(
            {
                "1": ["This is sun aging"],
                "2": ["This photo is sun aging"],
            }
        )

    elif concept_name == "Umbilicated":
        text_counter = "Umbilicated"
        prompt_dict = {"original": "This is Umbilicated"}
        prompt_dict.update(
            {
                "1": ["This is Umbilicated"],
            }
        )

    elif concept_name == "Dome-shaped":
        text_counter = "Dome"
        prompt_dict = {"original": "This is Dome-shaped"}
        prompt_dict.update(
            {
                "1": ["This is like Dome"],
            }
        )

    elif concept_name == "Flat topped":
        text_counter = "Flat"
        prompt_dict = {"original": "This is Flat topped"}
        prompt_dict.update(
            {
                "1": ["This is Flat topped"],
            }
        )
    else:
        return None
    return prompt_dict, text_counter
