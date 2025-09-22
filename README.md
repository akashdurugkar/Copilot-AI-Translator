# Copilot Localization Translator

A comprehensive Python application for managing and translating Microsoft Copilot Studio localization files using AI-powered context-aware translation.

## Features

- **Smart File Parsing**: Automatically extracts topics, contexts, and UI component information from complex Copilot Studio localization keys
- **AI-Powered Translation**: Uses OpenAI GPT models for context-aware, accurate translations
- **Multiple Translation Styles**: Support for formal, conversational, and chatbot-optimized translation styles
- **Multi-Language Support**: Translate to 35+ languages including major European, Asian, and other world languages
- **Interactive UI**: User-friendly interface with advanced table view, search, and filtering capabilities
- **Manual Editing**: Edit translations directly in the UI with a comprehensive edit dialog
- **Batch Translation**: Translate all entries at once or just selected ones
- **Translation Validation**: Built-in validation to ensure translation quality and accuracy
- **Export Functionality**: Export translated files in the original Copilot Studio format
- **Translation Cache**: Intelligent caching to avoid duplicate API calls and reduce costs
- **Cost Estimation**: Estimate translation costs before running batch operations

## Screenshots

![Main Application Interface](docs/main_interface.png)
*Main application interface showing file management, translation controls, and results table*

![Translation Editor](docs/translation_editor.png)
*Translation editor with context information and manual editing capabilities*

## Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key (for AI-powered translations)
- Windows, macOS, or Linux

### Setup

1. **Clone or download** this repository to your local machine

2. **Create a virtual environment**:
   ## Copilot Localization Translator

   Modern Tkinter desktop utility to load, explore, translate, and export Microsoft Copilot Studio localization JSON while preserving key order and boosting productivity.

   ### ✨ Features
   * Order‑stable JSON parse & export
   * Topic + component heuristic extraction
   * Skips global/system variables
   * Parallel AI translation with live progress
   * Cancel/Stop mid‑batch (cooperative)
   * Multiple translation style modes
   * Rich filtering: text / topic / component / status
   * Bulk + smart selection helpers (all, visible, invert, clear)
   * Details panel for large text editing
   * Status badges (Pending / Translated) + selection count
   * Light / Dark / System themes (token driven)
   * Rounded accessible button components
   * Zebra striping & centered columns
   * Topic value sanitization (fixes stray trailing ) )

   ### 🖥 Layout Overview
   Top bar: file actions, translation controls, theme toggle.
   Filter bar: search + dropdown filters + clear.
   Translation table: key rows (Original / Translation / Topic / Component / Status).
   Details panel: expanded view for editing long strings.
   Status bar: progress, cancel control, selection metadata.

   ### 🏗 Key Modules
   | File | Purpose |
   |------|---------|
   | `main.py` | UI composition, theming, threading, filtering, table mgmt |
   | `localization_parser.py` | JSON ingest, topic/component heuristics, filtering globals |
   | `translation_service.py` | Translation abstraction (swap provider here) |
   | `config_manager.py` | (Legacy) configuration utilities (future refactor) |
   | `Sample.json` | Example input data (demo + legacy test scaffolding removed) |

   ### ⚙ Concurrency
   Bounded worker pool + shared cancellation flag; workers enqueue progress events consumed on the Tk main loop for safe UI updates.

   ### 🎨 Theming
   `DESIGN_TOKENS` drives semantic colors and spacing. Theme switch recalculates palette and Treeview header styling for contrast.

   ### 🚀 Quick Start
   1. `python main.py`
   2. File → Open Localization File…
   3. Choose target language / style
   4. (Optional) refine via filters
   5. Translate (All or Selected)
   6. Review & edit
   7. Export translated file

   ### 🧪 Validation
   Ensures non‑empty translation values; planned: placeholder preservation, glossary enforcement.

   ### 🛣 Roadmap (Planned)
   * Persist theme & window geometry
   * Collapsible filter bar
   * Inline row quick actions
   * Provider strategy + caching
   * Diff & change highlighting
   * Glossary / terminology module
   * Quality scoring heuristics
   * Delta export mode
   * Keyboard shortcut palette
   * Binary packaging (PyInstaller)

   ### 🔧 Extending
   * Add styles: extend mapping in `translation_service.py`.
   * Extra filters: add column + logic in `SimpleTranslationTable.apply_filters`.
   * New backend: implement same interface as `TranslationService` and swap construction.

   ### 📂 Input Format
   Flat or nested JSON of localization keys to strings. Parser derives topic/component segments from structured key paths. Non-user-facing keys excluded where identifiable.

   ### 🧵 Thread Safety
   Only main thread touches widgets. Workers push events through a queue; UI loop drains and applies.

   ### 🛡 Errors
   Individual translation failures are isolated; batch continues and UI status updates accordingly.

   ### 🌗 Theme Snapshot
   Light: layered neutrals w/ indigo accents
   Dark: charcoal surfaces w/ indigo + cyan
   Shared scale: radii 6/10/18, spacing 4/8/12/20

   ### 🤝 Contributing
   Please keep UX responsive and leverage semantic tokens. PRs for accessibility & performance welcome.

   ### 📜 License
   MIT (add LICENSE file if distributing).

   ---
   Maintenance: Legacy UI scaffolding & duplicate table removed in cleanup. Update this file when adding roadmap items.
   - Endpoint: Your Azure OpenAI resource endpoint URL
   - API Version: Use `2024-02-15-preview` (recommended)
   - Deployment Name: The name you gave your deployed model

4. **Configure the Application**:
   - Use the Settings dialog to enter your Azure OpenAI details
   - Or edit the `.env` file directly with your configuration

### Translation Settings
- Default language and style preferences
- Batch size for API calls
- Retry attempt configuration

### Cache Settings
- Enable/disable translation caching
- Cache size limits
- Auto-save preferences

## File Structure

```
AI Copilot Translator/
├── main.py                 # Application (modern UI + logic)
├── localization_parser.py  # Localization file parser
├── translation_service.py  # AI translation service abstraction
├── requirements.txt        # Python dependencies
├── .env.example            # (Optional) environment variables template
├── Sample.json             # Sample localization file
└── README.md               # Project documentation
```

## API Costs

Translation costs depend on the OpenAI model used:

- **GPT-4**: ~$0.03 per 1K input tokens, ~$0.06 per 1K output tokens
- **GPT-3.5-turbo**: ~$0.001 per 1K input tokens, ~$0.002 per 1K output tokens

The application includes a cost estimation feature to help you budget translation projects.

## Troubleshooting

### Common Issues

1. **"No OpenAI client" error**:
   - Ensure your API key is set in the `.env` file
   - Verify the API key is valid and has sufficient credits

2. **Translation fails**:
   - Check your internet connection
   - Verify API key permissions
   - Try reducing batch size in settings

3. **File parsing errors**:
   - Ensure the file is a valid Copilot Studio localization JSON
   - Check file encoding (should be UTF-8)

4. **UI responsiveness issues**:
   - Large files may take time to load
   - Use search/filter to work with subsets of data

### Development Mode

To run without an OpenAI API key (uses mock translations):
```bash
python main.py
```

Mock translations will be marked with style prefixes like `[FORMAL]`, `[CONV]`, or `[BOT]`.

## Contributing

Contributions are welcome! Please consider:

- Adding support for additional file formats
- Improving translation quality algorithms
- Adding more UI languages
- Performance optimizations
- Additional validation features

## License

This project is provided as-is for educational and practical use. Please ensure you comply with OpenAI's usage policies when using the AI translation features.

## Support

For issues, questions, or feature requests, please:

1. Check the troubleshooting section above
2. Review the configuration settings
3. Ensure all dependencies are properly installed

## Version History

### Version 1.0 (Current)
- Initial release with full feature set
- Support for Copilot Studio localization files
- AI-powered translation with multiple styles
- Comprehensive UI with editing capabilities
- Translation validation and export functionality
- Cost estimation and caching features