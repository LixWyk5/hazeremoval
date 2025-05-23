# 🌫️ Single Image Haze Removal Using Dark Channel Prior

This project implements the classic **Single Image Haze Removal** algorithm proposed by **Kaiming He et al.**, using the **Dark Channel Prior (DCP)**. It takes a single hazy image and produces a visually clearer version using atmospheric light estimation, guided filtering, and radiance recovery.

---

## 📁 Directory Structure

```bash
.
├── haze image/                         # Input image folder
│   ├── defog.jpg
│   ├── Hazeimage_1.png
│   ├── Hazeimage_2.png
│   ├── Hazeimage_3.png
│   ├── hazy image.png
│   ├── hazy image_bikes.jpg
│   ├── hazy image_buildings.jpg
│   ├── hazy image_house.jpg
│   ├── hazy image_ny.jpg
│   └── hazy image_roofs.jpg
├── implement.py                        # Main Python script
├── result.jpg                          # Output: side-by-side comparison image
├── requirements.txt                    # Python dependencies
└── README.md                           # Project documentation
```

---

## 🚀 How to Run

1. Clone this repository:

   ```bash
   git clone https://github.com/LixWyk5/hazeremoval.git
   cd hazeremoval
   ```

2. Install required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the script:
   ```bash
   python implement.py
   ```

The script will:

- Load the input image (`Hazeimage_3.png` by default)
- Perform haze removal
- Save a side-by-side comparison to `result.jpg`

---

> You can modify the image path in `implement.py` to test other samples from the `haze image` folder.

---

## ⚙️ Core Algorithm Steps

1. **Dark Channel Calculation** – Estimates haze thickness by taking min across color channels in a local patch.
2. **Atmospheric Light Estimation** – Extracts the brightest pixels from the dark channel to estimate ambient light.
3. **Transmission Map Estimation** – Uses guided filtering to smooth the haze thickness estimation.
4. **Radiance Recovery** – Recovers the haze-free image by inverting the atmospheric scattering model.
5. **Optional Gamma Correction** – Enhances tone contrast if enabled.

---

## ✉ Contact

lixwyk@Outlook.com

---

## 📜 License

This project is open-source under the MIT License.
