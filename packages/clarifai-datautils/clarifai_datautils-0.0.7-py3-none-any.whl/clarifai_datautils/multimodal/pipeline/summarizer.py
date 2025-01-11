import base64
import random
from typing import List

try:
  from unstructured.documents.elements import CompositeElement, ElementMetadata, Image
except ImportError:
  raise ImportError(
      "Could not import unstructured package. "
      "Please install it with `pip install 'unstructured[pdf] @ git+https://github.com/clarifai/unstructured.git@support_clarifai_model'`."
  )

from clarifai.client.input import Inputs
from clarifai.client.model import Model

from .basetransform import BaseTransform

SUMMARY_PROMPT = """You are an assistant tasked with summarizing images for retrieval.
        These summaries will be embedded and used to retrieve the raw image.
        Give a concise summary of the image that is well optimized for retrieval.
        Also add relevant keywords that can be used for search. """


class ImageSummarizer(BaseTransform):
  """ Summarizes image elements. """

  def __init__(self,
               model_url: str = "https://clarifai.com/qwen/qwen-VL/models/qwen-VL-Chat",
               pat: str = None,
               prompt: str = SUMMARY_PROMPT,
               batch_size: int = 4):
    """Initializes an ImageSummarizer object.

    Args:
        pat (str): Clarifai PAT.
        model_url (str): Model URL to use for summarization.
        prompt (str): Prompt to use for summarization.
    """
    self.pat = pat
    self.model_url = model_url
    self.model = Model(url=model_url, pat=pat)
    self.summary_prompt = prompt
    self.batch_size = batch_size

  def __call__(self, elements: List) -> List:
    """Applies the transformation.

    Args:
        elements (List[str]): List of all elements.

    Returns:
        List of transformed elements along with added summarized elements.

    """
    img_elements = []
    for _, element in enumerate(elements):
      element.metadata.update(ElementMetadata.from_dict({'is_original': True}))
      if isinstance(element, Image):
        element.metadata.update(
            ElementMetadata.from_dict({
                'input_id': f'{random.randint(1000000, 99999999)}'
            }))
        img_elements.append(element)
    new_elements = self._summarize_image(img_elements)
    elements.extend(new_elements)
    return elements

  def _summarize_image(self, image_elements: List[Image]) -> List[CompositeElement]:
    """Summarizes an image element.

    Args:
        image_elements (List[Image]): Image elements to summarize.

    Returns:
        Summarized image elements list.

    """
    image_summary = []
    try:
      for i in range(0, len(image_elements), self.batch_size):
        batch = image_elements[i:i + self.batch_size]

        input_proto = [
            Inputs.get_multimodal_input(
                input_id=batch[id].metadata.input_id,
                image_bytes=base64.b64decode(batch[id].metadata.image_base64),
                raw_text=self.summary_prompt) for id in range(len(batch))
            if isinstance(batch[id], Image)
        ]
        resp = self.model.predict(input_proto)
        for i, output in enumerate(resp.outputs):
          summary = ""
          if image_elements[i].text:
            summary = image_elements[i].text
          summary = summary + " \n " + output.data.text.raw
          eid = batch[i].metadata.input_id
          meta_dict = {'source_input_id': eid, 'is_original': False, 'image_summary': 'yes'}
          comp_element = CompositeElement(
              text=summary,
              metadata=ElementMetadata.from_dict(meta_dict),
              element_id="summarized_" + eid)
          image_summary.append(comp_element)

    except Exception as e:
      raise e

    return image_summary
