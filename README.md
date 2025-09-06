# WQ Vision – AI-Powered Water Quality Testing Kit

![Prototype & Certificates](IMAGES/IMG_0505.PNG)

---

##  Project Overview  
**WQ Vision** is an innovative **AI-powered water quality testing system**, developed under the banner of **SRM Institute of Science and Technology (SRMIST)**. The platform combines computer vision, embedded systems, and machine learning to detect critical water parameters—such as **nitrite, nitrate, chlorine, total hardness, carbonate, and pH levels**—via colorimetric strip analysis.

---

##  Features & Architecture

### 1. Prototype Hardware  
The system includes:
- A **16×2 LCD display** for immediate feedback  
- **ESP32-CAM module**, complete with antenna for wireless image transmission  
- **Lithium-ion battery** and **cooling fan** to ensure stable, standalone operation  
- Efficient packaging for real-world usability  
![Hardware Prototype](IMAGES/IMG_0506.PNG)

---

### 2. AI-Driven Analysis  
- Captures photos of colorimetric strips via the ESP32-CAM  
- Processes images with a **custom AI model** to infer contaminant levels  
- Results are sent via **FastAPI** to both the LCD and the web dashboard  
- Categorizes outcomes as **Safe**, **Confidence**, **Caution**, or **Danger**, with visual confidence indicators  
![AI Model Flow](IMAGES/IMG_0507.PNG)

---

### 3. Web Dashboard  
- Built using **FastAPI** and a lightweight frontend  
- Users can upload images of test strips and receive:
  - Detailed water quality readings (e.g., ppm values)
  - Safety guidance and health impact commentary  
- Includes an intuitive UI for fast assessment  
![Web App Interface](IMAGES/IMG_0508.PNG)

---

### 4. Certificates & Recognition  
This project was awarded **1st place at Protothon 1.0, SRM IST**, for its practical impact and technical innovation.  
![Certificate 1](IMAGES/IMG_0509.PNG)  
![Certificate 2](IMAGES/IMG_7207.HEIC)  
![Certificate 3](IMAGES/IMG_7216.HEIC)  
![Certificate 4](IMAGES/IMG_7222.HEIC)

---

##  Impact & Significance  
WQ Vision showcases the power of integrating **IoT**, **embedded hardware**, and **AI** to create an **affordable, portable, and accurate** water quality evaluation system. It has real-world potential for community use, field diagnostics, and educational outreach in water safety monitoring.

---

##  Tech Stack & Skills  
| Component              | Stack / Tools                           |
|------------------------|------------------------------------------|
| **Embedded System**     | ESP32-CAM, LCD Display, Battery, Fan     |
| **AI Model**            | Custom Computer Vision Pipeline          |
| **Backend API**         | Python, FastAPI                          |
| **Frontend / Dashboard**| HTML/CSS/JS, Lightweight Web Framework   |
| **Deployment**          | Local Server or Cloud Instance           |
| **IoT Integration**     | Wireless Data Transmission               |
| **Safety Classification**| Custom Thresholding & Logic             |

- Hands-on experience with **IoT hardware integration**  
- Development of **computer vision models** for color-based testing  
- Building and deploying **APIs** for real-time data exchange  
- Creating functional **web dashboards** for user interactions  

---

##  Repository Structure

