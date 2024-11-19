<h1 align="center"> UXAgent: An LLM-Powered Usability Testing Framework for Web Design </h1>

<p align="center">
    <a href="https://arxiv.org/abs/xxxx.xxxx">
        <img src="https://img.shields.io/badge/arXiv-xxxx.xxxx-B31B1B.svg?style=plastic&logo=arxiv" alt="arXiv">
    </a>
    <a href="https://opensource.org/licenses/MIT">
        <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=plastic" alt="License: MIT">
    </a>
</p>

<p align="center">
Yuxuan Lu, Bingsheng Yao, Hansu Gu, Jing Huang, Jessie Wang, Laurence Li, Haiyang Zhang, Qi He, Toby Jia-Jun Li, Dakuo Wang
</p>

<p align="center">
    <img src="/figures/teaser.png" width="100%">
</p>


## Overview
**UXAgent** is a framework that uses Large Language Models (LLMs) as agents to conduct usability testing in web environments. These agents simulate human-like behaviors, allowing UX researchers to:
- Perform early usability evaluations.
- Gather actionable design insights.
- Iterate without immediate reliance on human participants.

The system leverages dual-system reasoning for quick decisions and in-depth analysis, and its **Universal Web Connector** ensures compatibility with any web page. By offering real-time feedback, UXAgent streamlines the design process and improves testing efficiency.


https://github.com/user-attachments/assets/0c5d22a8-4438-402b-8e6c-2151bdf53bf1


---

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:xxx/xxx.git
   ```

2. **Set up the environment:**
   ```bash
   conda env create -f environment.yml -n simulated_web_agent
   conda activate simulated_web_agent
   ```

3. **Install the package:**
   ```bash
   cd simulated_web_agent
   pip install -e .
   ```

4. **Install Chrome & Chromedriver:**
   - Download Chrome and the corresponding [chromedriver](https://googlechromelabs.github.io/chrome-for-testing/#stable).
   - Configure the chromedriver (example commands for Linux and macOS below).

   **Linux:**
   ```bash
   wget https://storage.googleapis.com/chrome-for-testing-public/131.0.6778.85/linux64/chromedriver-linux64.zip
   unzip chromedriver-linux64.zip
   sudo mv chromedriver /usr/bin/chromedriver
   sudo chmod +x /usr/bin/chromedriver
   ```

   **macOS:**
   ```bash
   brew install chromedriver
   xattr -d com.apple.quarantine /opt/homebrew/bin/chromedriver
   ```

   **Verify Installation:**
   ```bash
   chromedriver --version
   ```

5. **Set API keys:**
   Our UXAgent system supports AWS Claude and OpenAI. You only need to set one of them.
   - For AWS Claude:
      - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
   ```bash
   export AWS_ACCESS_KEY_ID=xxx123
   export AWS_SECRET_ACCESS_KEY=xxx123
   export OPENAI_API_KEY=sk-123
   ```

6. **Optional: Enable "headful" mode:**
   By default, Chrome runs in headless mode (no GUI). To view the browser, set the following:
   ```bash
   export HEADLESS=false
   ```

---

## Quick Start

1. **Run the Agent:**
   We provide 1,000 generated persona in `example_data`. Use the following command to test with a persona and save the output:
   ```bash
   python3 -m simulated_web_agent.main --persona "example_data/personas/json/virtual customer 0.json" --output "output"  --llm-provider openai
   ```

2. **Example Persona Format:**
   ```json
   {
       "persona": "Persona: Michael ...",
       "intent": "buy a large, inflatable spider decoration for halloween",
       "age": 42,
       "gender": "male",
       "income": [30001, 94000]
   }
   ```
3. **Example Persona:**
   ```
   Persona: Michael

   Background:
   Michael is a mid-career professional working as a marketing manager at a technology startup in San Francisco. He is passionate about using data-driven strategies to drive growth and innovation for the company.

   Demographics:
   Age: 42
   Gender: Male
   Education: Bachelor's degree in Business Administration
   Profession: Marketing Manager
   Income: $75,000

   Financial Situation:
   Michael has a comfortable income that allows him to maintain a decent standard of living in the expensive San Francisco Bay Area. He is financially responsible, saving a portion of his earnings for retirement and emergencies, while also enjoying occasional leisure activities and travel.

   Shopping Habits:
   Michael prefers to shop online for convenience, but he also enjoys the occasional trip to the mall or specialty stores to browse for new products. He tends to research items thoroughly before making a purchase, looking for quality, functionality, and value. Michael values efficiency and is not influenced by trends or impulse buys.

   Professional Life:
   As a marketing manager, Michael is responsible for developing and implementing marketing strategies to promote the startup's products and services. He collaborates closely with the product, sales, and design teams to ensure a cohesive brand experience. Michael is always looking for ways to optimize marketing campaigns and stay ahead of industry trends.

   Personal Style:
   Michael has a casual, yet professional style. He often wears button-down shirts, chinos, and leather shoes to the office. On weekends, he enjoys wearing comfortable, sporty attire for outdoor activities like hiking or cycling. Michael tends to gravitate towards neutral colors and classic, versatile pieces that can be mixed and matched.

   Intent:
   buy a large, inflatable spider decoration for halloween

   ```
---

## Generating Personas

Use the `persona.py` script to generate virtual customer personas based on configurations.

1. **Example Config (`config.yml`):**
   ```yaml
   output_dir: "output"
   queries_file: "queries.txt"
   total_personas: 200

   age_groups:
     "18-24": 40
     "25-34": 30
     "35-44": 20
     "45-54": 10
   ```

2. **Example Queries (`queries.txt`):**
   ```
   jacket columbia
   smartphone samsung
   laptop apple
   ```

3. **Run the script:**
   ```bash
   python -m simulated_web_agent.main.persona --config-file config.yml
   ```

Generated personas will be saved in the specified `output_dir` as `.json` and `.txt` files.

---

## License
This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
