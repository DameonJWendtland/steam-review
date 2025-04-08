# Steam Review Generator
Steam Review Generator is a Python-based GUI application that helps you generate creative and fun Steam reviews. 
The application is modular and leverages the tkinter library for its user interface.

## Features
- Category Selection:
Customize your review by selecting from a variety of categories (e.g., Graphics, Gameplay, Audio, etc.). Only activated categories are considered.

- Dynamic Tabs:
The app displays only the active (enabled) categories in separate tabs.

- Review Generation:
Generate a formatted review that includes a rating (from 1 to 10) and category details.
The review headers (e.g., for rating and category titles) are customizable via Design Settings.

- File Management:
Save the generated review as a TXT file or copy it directly to your clipboard.

- Options Dialog:
Adjust various settings in the options dialog, which includes three tabs:

- Categories: Toggle the visibility of review categories.

- Design Settings: Set the heading sizes for the review and categories.

 - Help: Open the GitHub issues page for support.

- Rating Recommendation:
The app can calculate a recommended rating based on your selections. A dedicated dialog shows the recommendation, and you can apply it (which updates the slider) or cancel.

## Folder Structure
```bash
project_root/
├── src/
│   ├── main.py               # Entry point that initializes and runs the application.
│   ├── categories.py         # Contains all category definitions.
│   ├── icons/...             # /Window icons.
│   └── gui/
│       ├── app.py            # Main application GUI that integrates all modules.
│       ├── file_manager.py   # Functions for saving and copying reviews.
│       ├── options_dialog.py # Options dialog for modifying category visibility, design settings, etc.
│       ├── rating_calculator.py # Logic to calculate the recommended rating.
│       ├── review_generator.py  # Generates review text based on settings.
│       └── tabs.py           # Manages category tabs.
└── 
```
## Installation

### Installer
Go to [releases](https://github.com/DameonJWendtland/steam-review-generator/releases) and choose the lates one. Download the installer and execute it afterwards.


### Install Python 3:
Make sure you have Python 3 installed on your system.

### Clone the Repository:

```bash
git clone https://github.com/DameonJWendtland/steam-review-generator.git
```
### Navigate to the Project Directory:

```bash
cd steam-review-generator
```

### Install Dependencies:
This project uses *only* built-in Python libraries.

## How to Run
Simply run the main script:

```bash
python src/main.py
```
The application window will open, allowing you to generate and customize your Steam review.

## Usage
### Generate Review:
Click the `Generate Review` button to create the review based on your selected options.

### Save or Copy:
Use the `Save as TXT` button to save the review to a file, or `Copy Review` to copy it to your clipboard.

### Options Dialog:

- Categories: Enable or disable specific categories.

- Design Settings: Adjust the heading sizes for the review and categories.

- Help: Open the GitHub issues page for support.

### Recommend Rating:
Click the `Recommend Rating` button to calculate a recommended rating based on the current selections.
In the recommendation dialog, click Apply to update the slider with the recommended rating, or Cancel to dismiss the dialog.

## Customization
The code is structured modularly for easy maintenance and expansion:

- Category Definitions: Modify or extend the review categories in `src/categories.py`.

- GUI Components: Adjust the look and behavior of the interface in the modules under `src/gui/`.

- Rating Calculation: Change the rating recommendation logic in `src/gui/rating_calculator.py`.


---

## Attribution
Icons were taken here:

<a href="https://www.flaticon.com/de/kostenlose-icons/rezension" title="rezension Icons">bewertung.ico - Flaticon</a>

<a href="https://www.flaticon.com/de/kostenlose-icons/filter" title="filter Icons">optionen.ico - Flaticon</a>

<a href="https://www.flaticon.com/de/kostenlose-icons/auswertung" title="auswertung Icons">checkliste.ico - Flaticon</a>
