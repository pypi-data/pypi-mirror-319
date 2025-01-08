# Endoc SDK

The Endoc software development kit (SDK) is for developers, researchers and other academic groups who want to programmatically access the NLP features developed for the Endoc platform.

It provides an interface agnostic approach allowing you to bypass the Endoc platform website and, directly integrate select NLP research-derived state of the art APIs into your own standalone applications.

# Motivation

LLMs are increasingly used as tools in academia, providing ways to access information, alternative views in reasoning, paraphraasing of content or summarisation of papers.

The intent of the Endoc SDK is to act as a scientific guard, providing an interface to Endoc LLM technologies programmatically that layer ETH in-house curated filters for scientific language accuracy.

## Get started

1. Install the Endoc SDK using pip:

```bash
pip install endoc-sdk
```

2. Get a free API key from the Endoc platform, under your Swiss affiliated account page or request one from the developers (if outside of Switzerland).

3. Initalize the Endoc SDK with your API key:

```python
# Import Endoc from endoc-sdk
from endoc-sdk import Endoc

# API Key available on the account page
client = Endoc("your_api_key");
```

## Contributing

We welcome contributions to the Endoc SDK. Please refer to the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.
