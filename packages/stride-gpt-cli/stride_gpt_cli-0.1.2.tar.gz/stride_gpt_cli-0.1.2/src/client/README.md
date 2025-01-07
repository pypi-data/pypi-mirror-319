# STRIDE GPT CLI

A powerful command-line tool for automated threat modeling using the STRIDE methodology. This tool helps security professionals and developers identify potential security threats in their system designs and architectures.

## Features

- 🔍 Automated threat identification using LLM technology
- 📊 Risk assessment using DREAD scoring
- 🛡️ Mitigation strategy recommendations
- 📝 System template generation
- 🔄 Continuous improvement suggestions

## Installation

Install the STRIDE GPT CLI using pip:

```bash
pip install stride-gpt-cli
```

## API Access

The STRIDE GPT CLI is free and open-source, but it requires an API key to access the STRIDE GPT API service. You can obtain an API key by:

1. Visiting [https://stridegpt.ai](https://stridegpt.ai)
2. Creating an account
3. Choosing a subscription plan
4. Generating your API key

For enterprise plans or custom pricing, please contact sales@stridegpt.ai.

## Quick Start

1. Set your API key:
```bash
# Unix/Linux/macOS
export STRIDE_GPT_API_KEY=your_api_key_here

# Windows (Command Prompt)
set STRIDE_GPT_API_KEY=your_api_key_here

# Windows (PowerShell)
$env:STRIDE_GPT_API_KEY=your_api_key_here
```

2. Generate a system template:
```bash
stride-gpt template > system.json
```

3. Analyze your system for threats:
```bash
stride-gpt analyze-all system.json
```

## Key Commands

- `stride-gpt template` - Generate a template system description
- `stride-gpt identify <file>` - Quick threat identification
- `stride-gpt analyze-all <file>` - Complete threat analysis with attack trees
- `stride-gpt assess <threat-id>` - Detailed risk assessment of a specific threat
- `stride-gpt mitigate <threat-id>` - Get mitigation strategies
- `stride-gpt improve <file>` - Get system description improvement suggestions

## Authentication

The CLI requires an API key for authentication. You can provide it through:
- Environment variable: `STRIDE_GPT_API_KEY`
- Command-line option: `--api-key`

API usage is subject to rate limits and quotas based on your subscription plan.

## Example Usage

1. Generate and customize a system template:
```bash
# Generate template
stride-gpt template > system.json

# Edit the system.json file to describe your system
```

2. Run a complete threat analysis:
```bash
stride-gpt analyze-all system.json
```

3. Get detailed risk assessment for a specific threat:
```bash
stride-gpt assess THR001 --system system.json
```

4. Generate mitigation strategies:
```bash
stride-gpt mitigate THR001 --system system.json
```

## Error Handling

Common error messages and solutions:

- `Authentication failed`: Check your API key is set correctly
- `Connection error`: Verify your internet connection and API endpoint
- `Invalid system description`: Ensure your JSON follows the required schema
- `Rate limit exceeded`: Wait a few minutes or upgrade your subscription plan

## Support

- Documentation: [https://docs.stridegpt.ai](https://docs.stridegpt.ai)
- Support Portal: [https://support.stridegpt.ai](https://support.stridegpt.ai)
- Email: support@stridegpt.ai

For enterprise support or custom integrations, please contact sales@stridegpt.ai.

## License

The STRIDE GPT CLI is open source software licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

Note: While this CLI tool is open source, the STRIDE GPT API is a commercial service with separate terms of service and pricing. API usage requires a valid subscription and API key.
 